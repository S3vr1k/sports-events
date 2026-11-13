// Каждая HTML-страница подключает этот файл. В конце выбирается её функция.
const $ = (selector) => document.querySelector(selector);
const params = new URLSearchParams(window.location.search);
let events = [];
let participants = [];

function element(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
}

function link(text, href, className = 'card-link') {
  const node = element('a', className, text);
  node.href = href;
  return node;
}

async function api(path, options = {}) {
  let response;
  try {
    response = await fetch(`/api${path}`, { ...options, signal: AbortSignal.timeout(12000) });
  } catch {
    throw new Error('Не удалось связаться с сервером. Попробуйте ещё раз позже.');
  }
  let data;
  try {
    data = await response.json();
  } catch {
    throw new Error('Сервер временно недоступен. Попробуйте ещё раз.');
  }
  if (!response.ok) {
    throw new Error(typeof data.detail === 'string' ? data.detail : 'Проверьте заполненные поля и попробуйте ещё раз.');
  }
  return data;
}

function showMessage(selector, message, isError = false) {
  const target = $(selector);
  target.textContent = message;
  target.classList.toggle('is-error', isError);
  target.classList.remove('is-success');
}

function retryMessage(selector, error, action) {
  showMessage(selector, error.message, true);
  const button = element('button', 'retry-button', 'Попробовать снова');
  button.type = 'button';
  button.addEventListener('click', action);
  $(selector).append(button);
}

function eventTitle(discipline) {
  return events.find((event) => event.event === discipline)?.title || discipline;
}

async function loadHome() {
  try {
    const [allEvents, allParticipants] = await Promise.all([api('/events'), api('/participants')]);
    $('#event-count').textContent = allEvents.length;
    $('#participant-count').textContent = allParticipants.length;
    showMessage('#home-state', '');
  } catch (error) {
    retryMessage('#home-state', error, loadHome);
  }
}

async function loadEventsPage() {
  showMessage('#events-state', 'Загружаем соревнования…');
  try {
    events = await api('/events');
    const grid = $('#events-grid');
    grid.replaceChildren();
    events.forEach((event) => {
      const card = element('article', 'event-card');
      const bottom = element('div', 'event-card-bottom');
      const discipline = encodeURIComponent(event.event);
      bottom.append(
        link('Подробнее', `/event.html?discipline=${discipline}`),
        link('Регистрация', `/registration.html?discipline=${discipline}`)
      );
      card.append(element('h2', '', event.title), element('p', 'event-description', event.description));
      card.append(element('p', 'event-location', event.location), bottom);
      grid.append(card);
    });
    if (!events.some((event) => event.event === 'chess')) {
      const planned = element('article', 'event-card planned');
      planned.append(element('h2', '', 'Шахматы'));
      planned.append(element('p', 'event-description', 'Шахматный турнир. Условия проведения уточняются.'));
      planned.append(element('span', 'planned-label', 'Регистрация пока не открыта'));
      grid.append(planned);
    }
    showMessage('#events-state', events.length ? '' : 'Организатор пока не добавил соревнования.');
  } catch (error) {
    retryMessage('#events-state', error, loadEventsPage);
  }
}

async function loadEventPage() {
  const discipline = params.get('discipline');
  if (!discipline) {
    showMessage('#event-state', 'Соревнование не выбрано. Перейдите к списку соревнований.', true);
    return;
  }
  showMessage('#event-state', 'Загружаем данные…');
  try {
    const event = await api(`/events/${encodeURIComponent(discipline)}`);
    document.title = `${event.title} — Школа №2051`;
    $('#event-title').textContent = event.title;
    $('#event-description').textContent = event.description;
    $('#event-location').textContent = event.location;
    $('#event-register').href = `/registration.html?discipline=${encodeURIComponent(discipline)}`;
    $('#event-content').hidden = false;
    showMessage('#event-state', '');
    await loadEventParticipants(discipline);
  } catch (error) {
    retryMessage('#event-state', error, loadEventPage);
  }
}

async function loadEventParticipants(discipline) {
  showMessage('#event-participants-state', 'Загружаем участников…');
  try {
    const people = await api(`/events/${encodeURIComponent(discipline)}/participants`);
    $('#event-participants-list').replaceChildren();
    people.forEach((person) => {
      const item = element('li');
      item.append(link(person.name, `/participant.html?id=${person.id}`, 'person-button'));
      $('#event-participants-list').append(item);
    });
    showMessage('#event-participants-state', people.length ? `Регистраций: ${people.length}` : 'Пока нет зарегистрированных участников.');
  } catch (error) {
    retryMessage('#event-participants-state', error, () => loadEventParticipants(discipline));
  }
}

function renderParticipants() {
  const query = $('#participant-search').value.trim().toLocaleLowerCase('ru');
  const discipline = $('#discipline-filter').value;
  const people = participants.filter((person) =>
    person.name.toLocaleLowerCase('ru').includes(query) && (!discipline || person.discipline === discipline)
  );
  const body = $('#participants-body');
  body.replaceChildren();
  people.forEach((person) => {
    const row = element('tr');
    const nameCell = element('td');
    nameCell.append(link(person.name, `/participant.html?id=${person.id}`, 'person-button'));
    nameCell.append(element('span', 'person-number', `Регистрация №${person.id}`));
    const disciplineCell = element('td', '', eventTitle(person.discipline));
    const actionCell = element('td');
    actionCell.append(link('Подробнее', `/participant.html?id=${person.id}`));
    row.append(nameCell, disciplineCell, actionCell);
    body.append(row);
  });
  if (!people.length) {
    const row = element('tr');
    const cell = element('td', '', participants.length ? 'По этому запросу участники не найдены.' : 'Пока нет зарегистрированных участников.');
    cell.colSpan = 3;
    row.append(cell);
    body.append(row);
  }
  $('#participants-caption').textContent = `Показано регистраций: ${people.length} из ${participants.length}`;
}

async function loadParticipantsPage() {
  const button = $('#refresh-participants');
  button.disabled = true;
  showMessage('#participants-state', 'Загружаем участников…');
  try {
    [events, participants] = await Promise.all([api('/events'), api('/participants')]);
    const filter = $('#discipline-filter');
    const previous = filter.value || params.get('discipline') || '';
    filter.replaceChildren(new Option('Все дисциплины', ''));
    events.forEach((event) => filter.add(new Option(event.title, event.event)));
    filter.value = previous;
    renderParticipants();
    showMessage('#participants-state', '');
  } catch (error) {
    retryMessage('#participants-state', error, loadParticipantsPage);
  } finally {
    button.disabled = false;
  }
}

async function loadParticipantPage() {
  const id = params.get('id');
  if (!id || !/^\d+$/.test(id)) {
    showMessage('#participant-state', 'Укажите корректный номер участника. Перейдите к общему списку.', true);
    return;
  }
  showMessage('#participant-state', 'Загружаем данные…');
  try {
    const person = await api(`/participants/${id}`);
    const event = await api(`/events/${encodeURIComponent(person.discipline)}`);
    document.title = `${person.name} — Школа №2051`;
    $('#participant-title').textContent = person.name;
    $('#participant-id').textContent = `№${person.id}`;
    $('#participant-event').textContent = event.title;
    $('#participant-event').href = `/event.html?discipline=${encodeURIComponent(person.discipline)}`;
    $('#participant-location').textContent = event.location;
    $('#participant-content').hidden = false;
    const button = $('#cancel-registration');
    button.disabled = false;
    button.onclick = async () => {
      if (!window.confirm(`Отменить регистрацию «${person.name}» на «${event.title}»?`)) return;
      button.disabled = true;
      try {
        await api(`/participants/${person.id}`, { method: 'DELETE' });
        $('#participant-content').hidden = true;
        showMessage('#participant-state', 'Регистрация отменена. Вы можете вернуться к списку участников.');
      } catch (error) {
        showMessage('#participant-state', error.message, true);
        button.disabled = false;
      }
    };
    showMessage('#participant-state', '');
  } catch (error) {
    $('#participant-content').hidden = true;
    retryMessage('#participant-state', error, loadParticipantPage);
  }
}

async function loadRegistrationPage() {
  showMessage('#registration-state', 'Загружаем дисциплины…');
  try {
    events = await api('/events');
    const select = $('#registration-discipline');
    select.replaceChildren(new Option('Выберите дисциплину', ''));
    events.forEach((event) => select.add(new Option(event.title, event.event)));
    const discipline = params.get('discipline');
    if (events.some((event) => event.event === discipline)) select.value = discipline;
    select.disabled = events.length === 0;
    $('#registration-submit').disabled = events.length === 0;
    showMessage('#registration-state', events.length ? '' : 'Регистрация пока недоступна: соревнования ещё не добавлены.');
  } catch (error) {
    retryMessage('#registration-state', error, loadRegistrationPage);
  }
}

async function registerParticipant(event) {
  event.preventDefault();
  const name = $('#full-name').value.trim();
  const discipline = $('#registration-discipline').value;
  $('#registration-result').hidden = true;
  if (!name || name.length >= 200 || !discipline) {
    showMessage('#registration-message', 'Укажите ФИО от 1 до 199 символов и выберите дисциплину.', true);
    return;
  }
  const button = $('#registration-submit');
  button.disabled = true;
  button.textContent = 'Регистрируем…';
  showMessage('#registration-message', '');
  try {
    const query = new URLSearchParams({ name });
    const person = await api(`/events/${encodeURIComponent(discipline)}/register?${query}`, { method: 'POST' });
    $('#registration-form').reset();
    showMessage('#registration-message', `Участник ${person.name} зарегистрирован на «${eventTitle(person.discipline)}». Номер регистрации: ${person.id}.`);
    $('#registration-message').classList.add('is-success');
    $('#registered-participant').href = `/participant.html?id=${person.id}`;
    $('#registration-result').hidden = false;
  } catch (error) {
    showMessage('#registration-message', error.message, true);
  } finally {
    button.disabled = false;
    button.textContent = 'Зарегистрироваться';
  }
}

// Запускаем только код текущей страницы, не обращаясь к чужим элементам.
switch (document.body.dataset.page) {
  case 'home':
    loadHome();
    break;
  case 'events':
    loadEventsPage();
    break;
  case 'event':
    loadEventPage();
    break;
  case 'participants':
    $('#participant-search').addEventListener('input', renderParticipants);
    $('#discipline-filter').addEventListener('change', renderParticipants);
    $('#refresh-participants').addEventListener('click', loadParticipantsPage);
    loadParticipantsPage();
    break;
  case 'participant':
    loadParticipantPage();
    break;
  case 'registration':
    $('#registration-form').addEventListener('submit', registerParticipant);
    loadRegistrationPage();
    break;
}
