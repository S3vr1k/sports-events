from fastapi import FastAPI, HTTPException
import os

import psycopg #PostgreSQL
from psycopg.rows import dict_row

app = FastAPI()

#ПОДКЛЮЧЕНИЕ
def get_connection():
    return psycopg.connect(
        host = os.environ["DB_HOST"],
        port = os.environ["DB_PORT"],
        dbname = os.environ["DB_NAME"],
        user = os.environ["DB_USER"],
        password = os.environ["DB_PASSWORD"],
        row_factory = dict_row
    )

#ГЛАВНАЯ СТРАНИЦА
@app.get("/")
def root():
    return {"Это официальный сайт, посвящённый спортивному фестивалю Школы №2051\n"\
        "Изучите все дисциплины и обязательно примите в них участие\n"\
        "P.S: type /events"}

#СОБЫТИЯ
@app.get("/events")
def get_events():
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT event, title, description, location FROM events"
            )
            return cursor.fetchall()

#ИНФОРМАЦИЯ О СОБЫТИИ
@app.get("/events/{discipline}")
def get_event_info(discipline: str):
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT event, title, description, location FROM events
                WHERE event = %s;
                """, (discipline,)
            )
            event = cursor.fetchone()
    
    if event is None:
        raise HTTPException(
            status_code = 404,
            detail = "Дисциплина не найдена"
        )
    
    return event

#ИНФОРМАЦИЯ ОБ УЧАСТНИКАХ ДИСЦИПЛИНЫ
@app.get("/events/{discipline}/participants")
def get_participants_discipline(discipline: str):
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT event FROM events WHERE event = %s",
                (discipline,)
            )

            if cursor.fetchone() is None:
                raise HTTPException(
                    status_code=404,
                    detail="Дисциплина не найдена"
                )

            cursor.execute(
                """
                SELECT id, name, discipline FROM participants
                WHERE discipline = %s;
                """, (discipline,)
            )
            result = cursor.fetchall()
    
    if result is None:
        raise HTTPException(
            status_code = 404,
            detail = "Дисциплина не найдена"
        )
    
    return result

#СПИСОК ВСЕХ УЧАСТНИКОВ
@app.get("/participants")
def get_participants_all():
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT id, name, discipline FROM participants"
            )
            return cursor.fetchall()

#КОНКРЕТНЫЙ УЧАСТНИК
@app.get("/participants/{participant_id}")
def get_participant(participant_id: int):
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, name, discipline FROM participants
                WHERE id = %s;
                """, (participant_id,)
            )

            result = cursor.fetchone()

    if result is None:
        raise HTTPException(
                status_code = 404,
                detail = "Такого участника нет"
        )
    return result

#ЗАПИСЬ НА ДИСЦИПЛИНУ
@app.post("/events/{discipline}/register")
def register_participants(discipline: str, name: str):
    name = name.strip()

    if not name:
        raise HTTPException(
            status_code = 422,
            detail = "Укажите ФИО участника"
        )

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT event FROM events WHERE event = %s", (discipline,)
            )

            if cursor.fetchone() is None:
                raise HTTPException(
                status_code=404,
                detail="Дисциплина не найдена"
            )

            cursor.execute(
                """
                INSERT INTO participants(name, discipline)
                VALUES(%s, %s)
                RETURNING id, name, discipline;
                """, (name, discipline)
            )
            result = cursor.fetchone()

    if result is None:
        raise HTTPException(
            status_code = 404,
            detail = "Ошибочный ввод данных"
        )
    return result

#УДАЛЕНИЕ РЕГИСТРАЦИИ
@app.delete("/participants/{participant_id}")
def delete_participant(participant_id: int):

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM participants
                WHERE id = %s
                RETURNING id, name, discipline;
                """, (participant_id,)
            )

            result = cursor.fetchone()

    if result is None:
        raise HTTPException(
            status_code = 404,
            detail = "Такого участника нет"
        )
    
    return result
