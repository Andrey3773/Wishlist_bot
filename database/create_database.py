import sqlite3


##### СОЕДИНЕНИЕ С ФАЙЛОМ, В КОТОРОМ НАХОДИТСЯ БАЗА ДАННЫХ #####
db = sqlite3.connect('database.sqlite')
cursor = db.cursor()


##### СОЗДАНИЕ БАЗЫ ДАННЫХ #####
# Этот скрипт необходим лишь единожды. Его надо запустить перед стартом работы бота
def create_database():
    # Пользователи
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users (
        user_id INTEGER,
        user_name TEXT,
        language TEXT
    )
    ''')

    # Подарки
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Gifts (
        gift_id INTEGER PRIMARY KEY,
        group_id INTEGER,
        user_id INTEGER,
        is_free BOOL
    )
    ''')

    # Группы
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Groups (
        group_id INTEGER PRIMARY KEY,
        group_name TEXT,
        password TEXT,
        owner_id INTEGER
    )
    ''')

    # Составы групп
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Accesses (
        access_id INTEGER PRIMARY KEY,
        group_id INTEGER,
        user_id INTEGER
    )
    ''')

    # Отзывы
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Feedback (
        feedback_id INTEGER PRIMARY KEY,
        feedback_text TEXT
    )
    ''')

    # Проблемы
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Troubles (
        trouble_id INTEGER PRIMARY KEY,
        trouble_text TEXT,
        solved BOOL
    )
    ''')

    db.commit()

create_database()
