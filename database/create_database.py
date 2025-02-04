import sqlite3


##### СОЕДИНЕНИЕ С ФАЙЛОМ, В КОТОРОМ НАХОДИТСЯ БАЗА ДАННЫХ #####
db = sqlite3.connect('database.sqlite')
cursor = db.cursor()
cursor.execute('PRAGMA foreign_keys = ON')


##### СОЗДАНИЕ БАЗЫ ДАННЫХ #####
# Этот скрипт необходим лишь единожды. Его надо запустить перед стартом работы бота
def create_database():
    # Пользователи
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            user_id INTEGER PRIMARY KEY,
            user_name TEXT,
            language TEXT
        )
    ''')

    # Подарки
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Gifts (
            gift_id INTEGER PRIMARY KEY,
            user_id INTEGER,
            giver_id INTEGER DEFAULT 0,
            gift_name TEXT
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
        CREATE TABLE IF NOT EXISTS Group_User (
            group_id INTEGER,
            user_id INTEGER,
            FOREIGN KEY (group_id) REFERENCES Groups(group_id) ON DELETE CASCADE,
            FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
        )
    ''')

    # Составы групп
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Group_Gift (
            group_id INTEGER,
            gift_id INTEGER,
            FOREIGN KEY (group_id) REFERENCES Groups(group_id) ON DELETE CASCADE,
            FOREIGN KEY (gift_id) REFERENCES Gifts(gift_id) ON DELETE CASCADE
        )
    ''')

    # Отзывы
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Feedback (
            feedback_id INTEGER PRIMARY KEY,
            feedback_text TEXT
        )
    ''')

    # Баги
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Issues (
            issue_id INTEGER PRIMARY KEY,
            issue_text TEXT,
            solved BOOL DEFAULT False
        )
    ''')

    db.commit()

create_database()
