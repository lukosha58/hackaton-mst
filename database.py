import sqlite3

conn = sqlite3.connect('database.db', check_same_thread=False)
cursor = conn.cursor()


def create_users_table():  # Создание таблицы пользователей
    cursor.execute("""CREATE TABLE IF NOT EXISTS users (user_id INT PRIMARY KEY, username TEXT, fullname TEXT)""")
    conn.commit()


def create_test_result_table():  # Создание таблицы результатов тестирований
    cursor.execute("""CREATE TABLE IF NOT EXISTS test_result (user_id BOOLEAN, time BOOLEAN, result BOOLEAN, 
                    finish_first_test BOOLEAN, finish_test_public_place BOOLEAN, finish_phishing_test BOOLEAN,
                    finish_social_test BOOLEAN, finish_osint_test BOOLEAN, finish_pass_test BOOLEAN, 
                    finish_phys_test BOOLEAN, finish_qr_test BOOLEAN)""")
    conn.commit()


def create_course_step_table():  # Создание таблицы, содержащей этап курса, на котором остановился пользователь
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS course_step (user_id INT, theme_0 BOOLEAN, theme_1 BOOLEAN, theme_2 BOOLEAN, theme_3 BOOLEAN, 
        theme_4 BOOLEAN, theme_5 BOOLEAN, theme_6 BOOLEAN, theme_7 BOOLEAN)""")
    conn.commit()


def insert_user(user_id: int, username: str, fullname: str):  # Добавление пользователя
    cursor.execute("""INSERT INTO users (user_id, username, fullname) VALUES (?, ?, ?)""",
                   (user_id, username, fullname))
    conn.commit()


def insert_or_replace_result(user_id: int, time, result: int):  # Добавление или замена результата тестирования
    cursor.execute("""REPLACE INTO test_result (user_id, time, result) VALUES (?, ?, ?)""", (user_id, time, result))
    conn.commit()


def insert_course_step(theme_num, user_id: int,
                       theme_val: int):  # Добавление или замена этапа прохождения курса
    sql_text = """REPLACE INTO course_step (user_id, theme_{}) VALUES (?, ?)""".format(theme_num)
    cursor.execute(sql_text, (user_id, theme_val))
    conn.commit()


def update_course_step(theme_num, user_id: int,
                       theme_val: int):  # Добавление или замена этапа прохождения курса
    sql_text = """UPDATE course_step SET theme_{} = ? WHERE user_id = ?""".format(theme_num)
    cursor.execute(sql_text, (theme_val, user_id))
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
