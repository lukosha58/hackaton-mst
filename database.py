import sqlite3

conn = sqlite3.connect('database.db', check_same_thread=False)
cursor = conn.cursor()


def create_users_table():  # Создание таблицы пользователей
    cursor.execute("""CREATE TABLE IF NOT EXISTS users (user_id INT PRIMARY KEY, username TEXT, fullname TEXT);""")
    conn.commit()


def create_test_result_table():  # Создание таблицы результатов тестирований
    cursor.execute("""CREATE TABLE IF NOT EXISTS test_result (user_id INT, time INT, result INT);""")
    conn.commit()


def create_course_step_table():  # Создание таблицы, содержащей этап курса, на котором остановился пользователь
    cursor.execute("""CREATE TABLE IF NOT EXISTS course_step (user_id INT, step INT);""")
    conn.commit()


def insert_user(user_id: int, username: str, fullname: str):  # Добавление пользователя
    cursor.execute("""INSERT INTO users (user_id, username, fullname) VALUES (?, ?, ?)""",
                   (user_id, username, fullname))
    conn.commit()


def insert_or_replace_result(user_id: int, time, result: int):  # Добавление или замена результата тестирования
    cursor.execute("""REPLACE INTO test_result (user_id, time, result) VALUES (?, ?, ?)""", (user_id, time, result))
    conn.commit()


def insert_or_replace_course_step(user_id: int, step: int):  # Добавление или замена этапа прохождения курса
    cursor.execute("""INSERT INTO course_step (user_id, step) VALUES (?, ?)""", (user_id, step))
    conn.commit()


def get_all_users():  # Получение всех пользователей
    cursor.execute("""SELECT * FROM users """)
    return cursor.fetchall()


def get_user(user_id: int):  # Получение информации о пользователе
    cursor.execute("""SELECT * FROM users WHERE user_id = (?)""", (user_id,))
    return cursor.fetchone()


def get_result(user_id: int):  # Получение информации о результате прохождения теста
    cursor.execute("""SELECT * FROM test_result WHERE user_id = (?)""", (user_id,))
    return cursor.fetchone()


def get_all_results():  # Получение всех результатов прохождения теста
    cursor.execute("""SELECT * FROM test_result """)
    return cursor.fetchall()


def get_course_step(user_id: int):  # Получение информации о этапе курса
    cursor.execute("""SELECT * FROM course_step WHERE user_id = (?)""", (user_id,))
    return cursor.fetchone()
