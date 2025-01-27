import sqlite3


##### СОЕДИНЕНИЕ С ФАЙЛОМ, В КОТОРОМ НАХОДИТСЯ БАЗА ДАННЫХ #####
db = sqlite3.connect('database\database.sqlite')
cursor = db.cursor()


##### ЗАНЕСЕНИЕ НОВОГО ПОЛЬЗОВАТЕЛЯ В БАЗУ ДАННЫХ #####
def new_user(user_id: int, user_name: str) -> None:
    cursor.execute('SELECT user_id FROM Users')
    if user_id not in [row[0] for row in cursor.fetchall()]:
        cursor.execute('INSERT INTO Users (user_id, user_name, language) VALUES (?, ?, ?)',
                       (user_id, user_name, 'ru'))
        db.commit()


##### ИМЯ ПОЛЬЗОВАТЕЛЯ ПО ЕГО ID #####
def give_name(user_id: int):
    return cursor.execute(f'SELECT user_name FROM Users WHERE user_id = {user_id}').fetchone()[0]


##### ИСПРАВЛЕНИЕ ОШИБКИ, ОБНАРУЖЕННОЙ ПОЛЬЗОВАТЕЛЕМ #####
def trouble_solved(trouble_id: int):
    cursor.execute(f'UPDATE Troubles SET solved = True WHERE trouble_id = {trouble_id}')


##### НАЗНАЧЕНИЕ ПОЛЬЗОВАТЕЛЯ АДМИНОМ #####
def make_admin(user_id: int):
    cursor.execute(f'UPDATE Users SET is_admin = True Where user_id = {user_id}')


##### ЯЗЫК ПОЛЬЗОВАТЕЛЯ ПО ЕГО ID #####
def user_language(user_id: int):
    return cursor.execute(f'SELECT language FROM Users WHERE user_id = {user_id}').fetchone()[0]


##### ПРОВЕРЯЕТ ЗАРЕГЕСТРИРОВАННОСТЬ ПОЛЬЗОВАТЕЛЯ #####
def user_in_data(user_id: int):
    return user_id in [row[0] for row in cursor.execute('SELECT user_id FROM Users').fetchall()]
