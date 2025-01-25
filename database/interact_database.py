import sqlite3

##### СОЗДАНИЕ БАЗЫ ДАННЫХ #####

db = sqlite3.connect('database\database.sqlite')
cursor =db.cursor()

# Создание таблицы для хранения пользователей
cursor.execute('''
CREATE TABLE IF NOT EXISTS Users (
    user_id INTEGER,
    user_name TEXT,
    is_admin BOOL
)
''')
db.commit()

# Создание таблицы для хранения подарков
cursor.execute('''
CREATE TABLE IF NOT EXISTS Gifts (
    gift_id INTEGER,
    group_id INTEGER,
    user_id INTEGER,
    is_free BOOL
)
''')
db.commit()

# Создание таблицы для хранения групп
cursor.execute('''
CREATE TABLE IF NOT EXISTS Groups (
    group_id INTEGER,
    group_name TEXT,
    password TEXT,
    owner_id INTEGER
)
''')
db.commit()

# Создание таблицы для хранения состава групп
cursor.execute('''
CREATE TABLE IF NOT EXISTS Accesses (
    access_id INTEGER,
    group_id INTEGER,
    user_id INTEGER
)
''')
db.commit()


##### Занесение нового пользователя в базу данных #####
def new_user(user_id: int, user_name: str, is_admin=False) -> None:
    cursor.execute('SELECT user_id FROM Users')
    if user_id not in [row[0] for row in cursor.fetchall()]:
        cursor.execute('INSERT INTO Users (user_id, user_name, is_admin) VALUES (?, ?, ?)',
                       (user_id, user_name, is_admin))
        db.commit()

