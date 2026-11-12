from fastapi import FastAPI, HTTPException

app = FastAPI()

participants = [
    {
        "id": 1,
        "name": "Иванов Александр Сергеевич",
        "discipline": "running"
    },
    {
        "id": 2,
        "name": "Петрова Мария Андреевна",
        "discipline": "running"
    },
    {
        "id": 3,
        "name": "Смирнов Артём Дмитриевич",
        "discipline": "running"
    },
    {
        "id": 4,
        "name": "Кузнецов Максим Игоревич",
        "discipline": "pushups"
    },
    {
        "id": 5,
        "name": "Соколова Анна Павловна",
        "discipline": "pushups"
    },
    {
        "id": 6,
        "name": "Попов Дмитрий Алексеевич",
        "discipline": "pushups"
    },
    {
        "id": 7,
        "name": "Волков Никита Романович",
        "discipline": "pullups"
    },
    {
        "id": 8,
        "name": "Морозова Дарья Олеговна",
        "discipline": "pullups"
    },
    {
        "id": 9,
        "name": "Новиков Михаил Денисович",
        "discipline": "pullups"
    },
    {
        "id": 10,
        "name": "Фёдорова София Максимовна",
        "discipline": "flexibility"
    },
    {
        "id": 11,
        "name": "Лебедев Егор Владимирович",
        "discipline": "flexibility"
    },
    {
        "id": 12,
        "name": "Орлова Полина Викторовна",
        "discipline": "flexibility"
    },
    {
        "id": 13,
        "name": "Семёнов Кирилл Антонович",
        "discipline": "jumps"
    },
    {
        "id": 14,
        "name": "Павлова Анастасия Ильинична",
        "discipline": "jumps"
    },
    {
        "id": 15,
        "name": "Белов Андрей Николаевич",
        "discipline": "jumps"
    }
]
events = [
    {
        "event": "running",
        "title": "Бег на 3 километра",
        "description": "Соревнование по бегу на длинную дистанцию",
        "location": "Школьный стадион",
    },
    {
        "event": "pushups",
        "title": "Отжимания",
        "description": "Соревнование по отжиманиям",
        "location": "Спортивный зал",
    },
    {
        "event": "pullups",
        "title": "Подтягивания",
        "description": "Соревнование по подтягиваниям",
        "location": "Спортивный зал",
    },
    {
        "event": "flexibility",
        "title": "Гибкость",
        "description": "Соревнование по растяжке",
        "location": "Спортивный зал",
    },
    {
        "event": "jumps",
        "title": "Прыжки в длину",
        "description": "Соревнование по прыжкам",
        "location": "Школьный стадион",
    }
]

#ГЛАВНАЯ СТРАНИЦА
@app.get("/")
def root():
    return {"Это официальный сайт, посвящённый спортивному фестивалю Школы №2051\n"\
        "Изучите все дисциплины и обязательно примите в них участие\n"\
        "P.S: type /events"}

#СОБЫТИЯ
@app.get("/events")
def get_events():
    return events

#ИНФОРМАЦИЯ О СОБЫТИИ
@app.get("/events/{discipline}")
def get_event_info(discipline: str):
    for event in events:
        if event["event"] == discipline:
            return event
    
    raise HTTPException(
        status_code=404,
        detail="Дисциплина не найдена"
    )

#ИНФОРМАЦИЯ ОБ УЧАСТНИКАХ ДИСЦИПЛИНЫ
@app.get("/events/{discipline}/participants")
def get_participants_discipline(discipline: str):
    exists = any (
        event for event in events
        if event["event"] == discipline
    )

    if not exists:
        raise HTTPException(
            status_code=404,
            detail="Дисциплина не найдена"
        )

    return [
        person for person in participants if person["discipline"] == discipline
    ]

#СПИСОК ВСЕХ УЧАСТНИКОВ
@app.get("/participants")
def get_participants_all():
    return participants

#КОНКРЕТНЫЙ УЧАСТНИК
@app.get("/participants/{participant_id}")
def get_participant(participant_id: int):
    for person in participants:
        if person["id"] == participant_id:
            return person
    raise HTTPException(
            status_code=404,
            detail="Такого участника нет"
        )

#ЗАПИСЬ НА ДИСЦИПЛИНУ
@app.post("/events/{discipline}/register")
def register_participants(discipline: str, name: str):
    next_id = max((person["id"] for person in participants), default = 0) + 1

    exists = any (
        event for event in events
        if event["event"] == discipline
    )

    if not exists:
        raise HTTPException(
            status_code=404,
            detail="Дисциплина не найдена"
        )
    
    name = name.strip()

    if not name:
        raise HTTPException(
            status_code=422,
            detail="Укажите ФИО участника"
        )

    participant = {
        "id" : next_id,
        "name" : name,
        "discipline" : discipline
    }

    participants.append(participant)

    return participant

# УДАЛЕНИЕ РЕГИСТРАЦИИ
@app.delete("/participants/{participant_id}")
def delete_participant(participant_id: int):
    
    for index, person in enumerate(participants):
        if person["id"] == participant_id:
            deleted_person = participants.pop(index)

            return {
                "message": "Участник удалён",
                "participant": deleted_person
            }

    raise HTTPException(
        status_code=404,
        detail="Такого участника нет"
    )
