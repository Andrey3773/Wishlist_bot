######################################################################################################################
####################### ФАЙЛ, В КОТОРОМ ХРАНЯТСЯ ВСЕ ФУНКЦИИ ДЛЯ ВЗАИМОДЕЙСТВИЯ С БАЗОЙ ДАННЫХ #######################
######################################################################################################################


import sqlite3, string, random
from aiogram.types import Message, CallbackQuery
from lexicon.lexicon import LEXICON


##### СОЕДИНЕНИЕ С ФАЙЛОМ, В КОТОРОМ НАХОДИТСЯ БАЗА ДАННЫХ #####
db = sqlite3.connect('database\database.sqlite')
cursor = db.cursor()



############################################### РАБОТА С ПОЛЬЗОВАТЕЛЯМИ ###############################################

##### ПРОВЕРЯЕТ ЗАРЕГЕСТРИРОВАННОСТЬ ПОЛЬЗОВАТЕЛЯ #####
def user_in_data(message: Message|CallbackQuery) -> bool:
    user_id = message.from_user.id
    return user_id in [row[0] for row in cursor.execute('SELECT user_id FROM Users').fetchall()]


##### ЗАНЕСЕНИЕ НОВОГО ПОЛЬЗОВАТЕЛЯ В БАЗУ ДАННЫХ #####
def new_user(message: Message|CallbackQuery, user_name: str) -> None:
    user_id = message.from_user.id
    cursor.execute('SELECT user_id FROM Users')
    if user_id not in [row[0] for row in cursor.fetchall()]:
        cursor.execute('INSERT INTO Users (user_id, user_name, language) VALUES (?, ?, ?)',
                       (user_id, user_name, 'ru')
                       )
        db.commit()
        cursor.execute('INSERT INTO Groups (group_name, password, owner_id) VALUES (?, ?, ?)',
                       (str(user_id), str(user_id), user_id)
                       )
        db.commit()
        group_id = cursor.execute(f"SELECT group_id FROM Groups WHERE group_name = '{str(user_id)}'").fetchone()[0]
        cursor.execute('INSERT INTO Accesses (group_id, user_id) VALUES (?, ?)',
                       (group_id, user_id)
                       )
        db.commit()


##### ВОЗВРАЩАЕТ ИМЯ ПОЛЬЗОВАТЕЛЯ #####
def give_name(message: Message|CallbackQuery) -> str:
    user_id = message.from_user.id
    return cursor.execute(f'SELECT user_name FROM Users WHERE user_id = {user_id}').fetchone()[0]


##### ВОЗВРАЩАЕТ ЯЗЫК ПОЛЬЗОВАТЕЛЯ #####
def user_language(message: Message|CallbackQuery) -> str:
    user_id = message.from_user.id
    return cursor.execute(f'SELECT language FROM Users WHERE user_id = {user_id}').fetchone()[0]


##### ЗАНЕСЕНИЕ НОВОГО ОТЗЫВА В БАЗУ ДАННЫХ #####
def new_feedback(message: Message|CallbackQuery) -> None:
    text = str(message.text)
    cursor.execute(f"INSERT INTO Feedback (feedback_text) VALUES ('{text}')")
    db.commit()



################################################# РАБОТА С ПОДАРКАМИ ##################################################

##### ВОЗВРАЩАЕТ СТРОКУ ВИДА 'group_name_1:\n gift_name_1\n gift_name_2\n\n group_name_1:.... #####
def all_my_gifts(message: Message|CallbackQuery) -> str:
    user_id = message.from_user.id
    gift_list = ''
    result: dict[str: list[str]] = {}

    if cursor.execute(f'SELECT COUNT(user_id)'
                      f'FROM Gifts '
                      f'WHERE user_id = {user_id}').fetchone()[0] > 0:

        group_gifts = [
            [i for i in row] for row in cursor.execute(f"SELECT group_name, gift_name "
                                                       f"FROM Groups "
                                                       f"INNER JOIN Gifts ON Groups.group_id = Gifts.group_id "
                                                       f"WHERE Gifts.user_id = {user_id}").fetchall()
        ]

        for row in group_gifts:
            if row[0] == str(user_id):
                group_name = LEXICON['my_own_group'][user_language(message)]
            else:
                group_name = str(row[0])
            if group_name in result.keys():
                result[group_name].append(str(row[1]))
            else:
                result[group_name] = []
                result[group_name].append(str(row[1]))

        for group in result.keys():
            if group == str(user_id):
                group = LEXICON['my_own_group'][user_language(message)]
            gift_list += f'<b>{group}</b>:\n'
            for gift in result[group]:
                gift_list += f'    {gift}\n'
            gift_list += '\n'

    else:
        gift_list = LEXICON['no_gifts'][user_language(message)]

    return gift_list


##### ДОБАВЛЯЕТ ПОДАРОК БЕЗ ГРУППЫ (В ОБЩИЙ ДОСТУП) #####
def my_own_new_gift(message: Message|CallbackQuery) -> None:
    user_id = message.from_user.id
    gift_name = str(message.text)
    my_own_group_id = cursor.execute(f"SELECT group_id FROM Groups WHERE group_name = '{str(user_id)}'").fetchone()[0]
    cursor.execute(f"INSERT INTO Gifts (group_id, user_id, is_free, gift_name) "
                   f"VALUES (?, ?, ?, ?)", (my_own_group_id, user_id, False, gift_name))
    db.commit()


##### УДАЛЕНИЕ ПОДАРКА (ПОЛЬЗОВАТЕЛЬ ОТПРАВЛЯЕТ ЕГО НАЗВАНИЕ) #####
# TODO сделать адекватное удаление, а не просто копипастингом из списка
def delete_my_own_gift(message: Message|CallbackQuery) -> None:
    user_id = message.from_user.id
    gift_name = message.text
    cursor.execute(f"DELETE FROM Gifts WHERE user_id = {user_id} AND gift_name = '{gift_name}'")
    db.commit()



################################################# РАБОТА С ГРУППАМИ  ##################################################

##### СОЗДАЁТ НОВУЮ ГРУППУ #####
def new_group(message: Message|CallbackQuery) -> None:
    group_name = str(message.text)
    while True:
        group_password = ''.join(
            random.choice(string.ascii_letters + string.digits)
            for _ in range(16)
        )
        if not(group_password in [i[0] for i in cursor.execute('SELECT password FROM Groups').fetchall()]):
            break

    owner_id = int(message.from_user.id)
    cursor.execute(
        f"INSERT INTO Groups (group_name, password, owner_id) VALUES (?, ?, ?)",
        (group_name, group_password, owner_id)
    )
    db.commit()
    cursor.execute(
        f"INSERT INTO Accesses (group_id, user_id) VALUES (?, ?)",
        (cursor.execute(
            f"SELECT group_id FROM Groups WHERE password = '{group_password}'"
        ).fetchone()[0], owner_id)
    )
    db.commit()


##### ПРОЕРЯЕТ, ЕСТЬ ЛИ ПОЛЬЗОАТЕЛЬ В ГРУППЕ #####
def is_user_in_group(message: Message) -> bool:
    password = str(message.text)
    user_id = int(message.from_user.id)
    group_id = cursor.execute(f"SELECT group_id FROM Groups WHERE password = '{password}'").fetchone()[0]

    return [group_id, user_id] in [[row[0], row[1]] for row in
                                cursor.execute(
                                    f"SELECT group_id, user_id FROM Accesses"
                                ).fetchall()]


##### ДОБАВЛЯЕТ ПОЛЬЗОВАТЕЛЯ В ГРУППУ, ПАРОЛЬ К КОТОРОЙ ОН ВВЕЛ #####
def add_user_in_group(message: Message) -> None:
    password = str(message.text)
    user_id = int(message.from_user.id)
    group_id = cursor.execute(f"SELECT group_id FROM Groups WHERE password = '{password}'").fetchone()[0]

    cursor.execute(
        f"INSERT INTO Accesses (group_id, user_id) VALUES (?, ?)",
        (group_id, user_id)
    )
    db.commit()


##### ВОЗВРАЩАЕТ ПАРОЛЬ ОТ ГРУППЫ #####
def give_group_password(message: Message|CallbackQuery) -> str:
    pass



################################################## РАБОТА С ОТЗЫВАМИ ##################################################

##### ИСПРАВЛЕНИЕ ОШИБКИ, ОБНАРУЖЕННОЙ ПОЛЬЗОВАТЕЛЕМ #####
def trouble_solved(message: Message|CallbackQuery) -> None:
    trouble_id = int(message.text)
    cursor.execute(f'UPDATE Troubles SET solved = True WHERE trouble_id = {trouble_id}')
    db.commit()


##### ВОЗВРАЩАЕТ СТРОКУ ВИДА 'feedback_id. feedback_text \n\n ....' СО ВСЕМИ ОТЗЫВАМИ #####
def all_feedback() -> str:
    feedback = ''
    if len(cursor.execute('SELECT * FROM Feedback').fetchall()) > 0:
        for row in cursor.execute('SELECT * FROM Feedback'):
            feedback += str(row[0]) + '. ' + row[1] + '\n\n'
    else:
        feedback = 'Отзывов пока нет'
    return feedback


##### ПЕРЕНОСИТ ОТЗЫВ ИЗ ТАБЛИЦЫ С ОТЗЫВАМИ В ТАБЛИЦУ С ПРОБЛЕМАМИ И ПРИСВАИВАЕТ ЕЙ СТАТУС НЕРЕШЕННОЙ #####
def new_trouble(trouble_id: int) -> None:
    pass
