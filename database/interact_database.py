######################################################################################################################
####################### ФАЙЛ, В КОТОРОМ ХРАНЯТСЯ ВСЕ ФУНКЦИИ ДЛЯ ВЗАИМОДЕЙСТВИЯ С БАЗОЙ ДАННЫХ #######################
######################################################################################################################


import sqlite3, string, random
from aiogram.types import Message, CallbackQuery
from lexicon.lexicon import LEXICON


##### СОЕДИНЕНИЕ С ФАЙЛОМ, В КОТОРОМ НАХОДИТСЯ БАЗА ДАННЫХ #####
db = sqlite3.connect('database\database.sqlite')
cursor = db.cursor()



############################################### МЕЛКИЕ СЛУЖЕБНЫЕ ФУНКЦИИ ###############################################

##### ВОЗВРАЩАЕТ USER_NAME ПО ЕГО ID ######
def get_user_name(user_id: int) -> str:
    return cursor.execute(f"SELECT user_name FROM Users WHERE user_id = {user_id}").fetchone()[0]


##### ВОЗВРАЩАЕТ GROUP_NAME ПО ЕГО ID ######
def get_group_name(message: Message|CallbackQuery, group_id: int) -> str:
    user_id = str(message.from_user.id)
    group_name = cursor.execute(f"SELECT group_name FROM Groups WHERE group_id = {group_id}").fetchone()[0]
    if group_name == user_id:
        return LEXICON['my_own_group'][user_language(message)]
    else:
        return group_name


##### ВОЗВРАЩАЕТ GIFT_NAME ПО ЕГО ID ######
def get_gift_name(gift_id: int) -> str:
    return cursor.execute(f"SELECT gift_name FROM Gifts WHERE gift_id = {gift_id}").fetchone()[0]



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
def all_my_own_gifts(message: Message | CallbackQuery) -> str:
    user_id = int(message.from_user.id)
    all_gifts = all_accessible_gifts(message)

    gift_list = ''

    for group_id in all_gifts.keys():
        gift_list += f'<b>{get_group_name(message, group_id)}</b>:\n'
        for gift_id in all_gifts[group_id][user_id]:
            gift_list += '    ' + get_gift_name(gift_id) + '\n'
        gift_list += '\n'


    return gift_list


##### ПРОЕРЯЕТ ЕСТЬ ЛИ У ПОЛЬЗОВАТЕЛЯ ПОДАРОК С ОБЩИМ ДОСТУПОМ С ТАКИМ ИМЕНЕМ #####
def is_user_has_own_gift(message: Message|CallbackQuery) -> bool:
    user_id = message.from_user.id
    gift_name = str(message.text)
    my_own_group_id = cursor.execute(f"SELECT group_id FROM Groups WHERE group_name = '{str(user_id)}'").fetchone()[0]

    return gift_name in [row[0] for row in
                         cursor.execute(
                             f"SELECT gift_name FROM Gifts "
                             f"WHERE group_id = {my_own_group_id} AND user_id = {user_id}"
                         ).fetchall()]


##### ДОБАВЛЯЕТ ПОДАРОК В ОБЩИЙ ДОСТУП #####
def my_own_new_gift(message: Message|CallbackQuery) -> None:
    user_id = message.from_user.id
    gift_name = str(message.text)

    accessible_group_ids = [row[0] for row in
                            cursor.execute(
                                f"SELECT group_id FROM Accesses "
                                f"WHERE user_id = {user_id}"
                            ).fetchall()]
    for group_id in accessible_group_ids:
        cursor.execute(f"INSERT INTO Gifts (group_id, user_id, is_free, gift_name) "
                       f"VALUES (?, ?, ?, ?)", (group_id, user_id, False, gift_name))
        db.commit()


##### УДАЛЕНИЕ ПОДАРКА (ПОЛЬЗОВАТЕЛЬ ОТПРАВЛЯЕТ ЕГО НАЗВАНИЕ) #####
# TODO сделать адекватное удаление, а не просто копипастингом из списка
def delete_my_own_gift(message: Message|CallbackQuery) -> None:
    user_id = message.from_user.id
    gift_name = message.text
    cursor.execute(f"DELETE FROM Gifts WHERE user_id = {user_id} AND gift_name = '{gift_name}'")
    db.commit()



################################################# РАБОТА С ГРУППАМИ  ##################################################

##### ПРОЕРЯЕТ, ЕСТЬ ЛИ У ПОЛЬЗОВАТЕЛЯ ГРУППА С ТАКИМ НАЗВАНИЕМ #####
def is_user_has_group(message: Message|CallbackQuery) -> bool:
    group_name = str(message.text)
    user_id = int(message.from_user.id)
    return group_name in [row[0] for row in cursor.execute(
        f"SELECT group_name FROM Groups "
        f"INNER JOIN Accesses "
        f"ON Groups.group_id = Accesses.group_id "
        f"WHERE user_id = {user_id}"
    ).fetchall()]


##### СОЗДАЁТ НОВУЮ ГРУППУ #####
def new_group(message: Message|CallbackQuery) -> None:
    group_name = str(message.text)
    owner_id = int(message.from_user.id)

    while True:
        group_password = ''.join(
            random.choice(string.ascii_letters + string.digits)
            for _ in range(16)
        )
        if not(group_password in [i[0] for i in cursor.execute('SELECT password FROM Groups').fetchall()]):
            break

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

    my_own_group_id = cursor.execute(f"SELECT group_id FROM Groups WHERE group_name = '{str(owner_id)}'").fetchone()[0]
    group_id = cursor.execute(f"SELECT group_id FROM Groups WHERE password = '{group_password}'").fetchone()[0]

    for_everyone_gifts = [
        row for row in
        cursor.execute(
            f"SELECT is_free, gift_name "
            f"FROM Gifts "
            f"WHERE user_id = {owner_id} AND group_id = {my_own_group_id}"
        ).fetchall()
    ]
    for row in for_everyone_gifts:
        cursor.execute(f"INSERT INTO Gifts (group_id, user_id, is_free, gift_name) "
                       f"VALUES (?, ?, ?, ?)", (group_id, owner_id, row[0], row[1]))
        db.commit()


##### ПРОВЕРЯЕТ КОРРЕКТНОСТЬ ПАРОЛЯ #####
def is_password_correct(message: Message|CallbackQuery) -> bool:
    password = str(message.text)
    if password in [row[0] for row in cursor.execute("SELECT password FROM Groups").fetchall()]:
        return True
    else:
        return False


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

    my_own_group_id = cursor.execute(f"SELECT group_id FROM Groups WHERE group_name = '{str(user_id)}'").fetchone()[0]
    for_everyone_gifts = [
        row for row in
        cursor.execute(
            f"SELECT is_free, gift_name "
            f"FROM Gifts "
            f"WHERE user_id = {user_id} AND group_id = {my_own_group_id}"
        ).fetchall()
    ]
    for row in for_everyone_gifts:
        cursor.execute(f"INSERT INTO Gifts (group_id, user_id, is_free, gift_name) "
                       f"VALUES (?, ?, ?, ?)", (group_id, user_id, row[0], row[1]))
        db.commit()


##### ВОЗВРАЩАЕТ ПАРОЛЬ ОТ ГРУППЫ #####
def give_group_password(message: Message|CallbackQuery) -> str:
    pass


##### ВОЗВРАЩАЕТ СЛОВАРЬ ВИДА {'group_name': {'user_name': [gift_name, ....], ....}, ....} #####
def all_accessible_gifts(message: Message|CallbackQuery):
    user_id_from_message = int(message.from_user.id)
    result: dict[int, dict[int, list[int]]] = {}

    accessible_group_ids = [
        row[0] for row in
        cursor.execute(
            f"SELECT group_id "
            f"FROM Accesses "
            f"WHERE user_id = {user_id_from_message}"
        ).fetchall()
    ]

    for group_id in accessible_group_ids:

        users_in_group = [
            row[0] for row in
            cursor.execute(
                f"SELECT user_id "
                f"FROM Accesses "
                f"WHERE group_id = {group_id}"
            ).fetchall()
        ]

        if not(group_id in result.keys()):
            result[group_id] = {}

        for user_id in users_in_group:

            users_gifts = [
                row[0] for row in
                cursor.execute(
                    f"SELECT gift_id FROM Gifts WHERE group_id = {group_id} AND user_id = {user_id}"
                ).fetchall()
            ]

            if not(user_id in result[group_id].keys()):
                result[group_id][user_id] = []

            for gift_id in users_gifts:
                result[group_id][user_id].append(gift_id)

    return result

# result[group_name][user_name].append(gift)




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
