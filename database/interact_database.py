import sqlite3
from aiogram.types import Message, CallbackQuery


##### СОЕДИНЕНИЕ С ФАЙЛОМ, В КОТОРОМ НАХОДИТСЯ БАЗА ДАННЫХ #####
db = sqlite3.connect('database\database.sqlite')
cursor = db.cursor()


##### ЗАНЕСЕНИЕ НОВОГО ПОЛЬЗОВАТЕЛЯ В БАЗУ ДАННЫХ #####
def new_user(message: Message|CallbackQuery, user_name: str) -> None:
    user_id = message.from_user.id
    cursor.execute('SELECT user_id FROM Users')
    if user_id not in [row[0] for row in cursor.fetchall()]:
        cursor.execute('INSERT INTO Users (user_id, user_name, language) VALUES (?, ?, ?)',
                       (user_id, user_name, 'ru'))
        db.commit()


##### ИМЯ ПОЛЬЗОВАТЕЛЯ ПО ЕГО ID #####
def give_name(message: Message|CallbackQuery):
    user_id = message.from_user.id
    return cursor.execute(f'SELECT user_name FROM Users WHERE user_id = {user_id}').fetchone()[0]


##### ИСПРАВЛЕНИЕ ОШИБКИ, ОБНАРУЖЕННОЙ ПОЛЬЗОВАТЕЛЕМ #####
def trouble_solved(message: Message|CallbackQuery):
    trouble_id = int(message.text)
    cursor.execute(f'UPDATE Troubles SET solved = True WHERE trouble_id = {trouble_id}')
    db.commit()


##### ЯЗЫК ПОЛЬЗОВАТЕЛЯ ПО ЕГО ID #####
def user_language(message: Message|CallbackQuery):
    user_id = message.from_user.id
    return cursor.execute(f'SELECT language FROM Users WHERE user_id = {user_id}').fetchone()[0]


##### ПРОВЕРЯЕТ ЗАРЕГЕСТРИРОВАННОСТЬ ПОЛЬЗОВАТЕЛЯ #####
def user_in_data(message: Message|CallbackQuery):
    user_id = message.from_user.id
    return user_id in [row[0] for row in cursor.execute('SELECT user_id FROM Users').fetchall()]


##### ВОЗВРАЩАЕТ СТРОКУ ВИДА 'feedback_id. feedback_text \n\n ....' СО ВСЕМИ ОТЗЫВАМИ #####
def all_feedback():
    feedback = ''
    if len(cursor.execute('SELECT * FROM Feedback').fetchall()) > 0:
        for row in cursor.execute('SELECT * FROM Feedback'):
            feedback += str(row[0]) + '. ' + row[1] + '\n\n'
    else:
        feedback = 'Отзывов пока нет'
    return feedback


##### ЗАНЕСЕНИЕ НОВОГО ОТЗЫВА В БАЗУ ДАННЫХ #####
def new_feedback(message: Message|CallbackQuery):
    text = str(message.text)
    cursor.execute(f"INSERT INTO Feedback (feedback_text) VALUES ('{text}')")
    db.commit()

##### ПЕРЕНОСИТ ОТЗЫВ ИЗ ТАБЛИЦЫ С ОТЗЫВАМИ В ТАБЛИЦУ С ПРОБЛЕМАМИ И ПРИСВАИВАЕТ ЕЙ СТАТУС НЕРЕШЕННОЙ #####
def new_trouble(trouble_id: int):
    pass
