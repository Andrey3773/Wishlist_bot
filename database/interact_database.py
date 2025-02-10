########################################################################################################################
######################## ФАЙЛ, В КОТОРОМ ХРАНЯТСЯ ВСЕ ФУНКЦИИ ДЛЯ ВЗАИМОДЕЙСТВИЯ С БАЗОЙ ДАННЫХ ########################
########################################################################################################################


import sqlite3, string, random
from aiogram.types import Message, CallbackQuery
from lexicon.lexicon import LEXICON, LEXICON_ADMIN, KEYBOARD_LEXICON


##### СОЕДИНЕНИЕ С ФАЙЛОМ, В КОТОРОМ НАХОДИТСЯ БАЗА ДАННЫХ #####
db = sqlite3.connect('database/database.sqlite')
cursor = db.cursor()
cursor.execute('PRAGMA foreign_keys = ON')



############################################### МЕЛКИЕ СЛУЖЕБНЫЕ ФУНКЦИИ ###############################################

##### ВОЗВРАЩАЕТ ЯЗЫК ПОЛЬЗОВАТЕЛЯ #####
def user_language(message: Message|CallbackQuery) -> str:
    user_id = message.from_user.id
    return cursor.execute(f'SELECT language FROM Users WHERE user_id = {user_id}').fetchone()[0]


##### ВОЗВРАЩАЕТ ИМЯ ПОЛЬЗОВАТЕЛЯ #####
def give_name(message: Message|CallbackQuery) -> str:
    user_id = message.from_user.id
    return cursor.execute(f'SELECT user_name FROM Users WHERE user_id = {user_id}').fetchone()[0]


##### ВОЗВРАЩАЕТ USER_NAME ПО ЕГО ID ######
def get_user_name(user_id: int) -> str:
    return cursor.execute(f"SELECT user_name FROM Users WHERE user_id = {user_id}").fetchone()[0]


##### ВОЗВРАЩАЕТ GROUP_NAME ПО ЕE ID ######
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


##### ВОЗВРАЩАЕТ GIVER_ID ПО GIFT_ID #####
def get_giver_id(gift_id: int) -> int:
    return cursor.execute(f"SELECT giver_id  FROM Gifts WHERE gift_id = {gift_id}").fetchone()[0]


##### ВОЗВРАЩАЕТ СЛОВАРЬ ПОЛЬЗОВАТЕЛЕЙ ПО ГРУППАМ #####
def users_in_groups(message: Message|CallbackQuery, not_all=True) -> dict:
    user_id_from_message = message.from_user.id
    all_users = {}

    for group_id in all_accessible_gifts(message):
        if group_id not in all_users:
            all_users[group_id] = []
        for user_id in all_accessible_gifts(message)[group_id]:
            all_users[group_id].append(user_id)

    if not_all:
        all_users.pop(cursor.execute(
            f"SELECT group_id "
            f"FROM Groups "
            f"WHERE password = '{str(user_id_from_message)}'"
        ).fetchone()[0])

    return all_users


##### ВОЗВРАЩАЕТ СЛОВАРЬ ПОДАРКОВ ПО ПОЛЬЗОВАТЕЛЯМ В ВЫБРАННОЙ ГРУППЕ #####
def users_gifts_in_group(message: Message | CallbackQuery) -> dict:
    group_id = int(message.data)
    all_gifts = {}

    for user_id in all_accessible_gifts(message)[group_id]:
        if user_id not in all_gifts:
            all_gifts[user_id] = []
        for gift in all_accessible_gifts(message)[group_id][user_id]:
            all_gifts[user_id].append(gift)

    return all_gifts


##### ВОЗВРАЩАЕТ СПИСОК ПОДАРКОВ ВЫБРАННОГО ПОЛЬЗОВАТЕЛЯ В ВЫБРАННОЙ ГРУППЕ #####
def user_gifts_in_group(message: Message | CallbackQuery) -> list:
    if '_' in str(message.data):
        group_id = int(message.data[:message.data.index('_')])
        user_id = int(message.data[message.data.index('_') + 1:])
    else:
        group_id = int(message.data)
        user_id = message.from_user.id

    gifts = []

    for gift_id in all_accessible_gifts(message)[group_id][user_id]:
        gifts.append(gift_id)

    return gifts


##### ВОЗВРАЩАЕТ ВСЕ ПОДАРКИ ПОЛЬЗОВАТЕЛЯ #####
def all_users_gifts(message: Message|CallbackQuery) -> dict:
    return {row[0]: row[1]
            for row in cursor.execute(
            f"SELECT gift_id, gift_name "
            f"FROM Gifts "
            f"WHERE user_id = {message.from_user.id}"
        ).fetchall()}


##### ВОЗВРАЩАЕТ СПИСОК ID ОТЗЫВОВ #####
def feedback_list() -> list:
    return [row[0] for row in cursor.execute("SELECT feedback_id FROM Feedback").fetchall()]


##### ВОЗВРАЩАЕТ СПИСОК ID ПРОБЛЕМ #####
def issue_list() -> list:
    return [row[0] for row in cursor.execute("SELECT issue_id FROM Issues").fetchall()]



############################# ФОРМИРОВАНИЕ НУЖНОГО ТЕКСТА СООБЩЕНИЯ, ЕСЛИ ОН ЗАВИСИТ ОТ БД #############################

##### ВОЗВРАЩАЕТ ВСЕ ПОДАРКИ ПОЛЬЗОВАТЕЛЯ ПО ГРУППАМ #####
def all_my_own_gifts(message: Message|CallbackQuery) -> str:
    user_id = int(message.from_user.id)
    all_gifts = all_accessible_gifts(message)

    gift_list = ''

    for group_id in all_gifts.keys():
        gift_list += f'<b>{get_group_name(message, group_id)}</b>:\n'
        for gift_id in all_gifts[group_id][user_id]:
            gift_list += '    ' + get_gift_name(gift_id) + '\t\n'
        gift_list += '\t\n'

    if gift_list == f"<b>{LEXICON['my_own_group'][user_language(message)]}</b>:\n\t\n":
        gift_list = LEXICON['no_gifts'][user_language(message)]

    return gift_list


##### ВОЗВРАЩАЕТ ВСЕ ГРУППЫ ПОЛЬЗОВАТЕЛЯ С ИХ СОСТАВАМИ #####
def all_my_groups(message: Message | CallbackQuery) -> str:
    all_users = users_in_groups(message)
    user_list = ''

    for group_id in all_users.keys():
        user_list += f'<b>{get_group_name(message, group_id)}</b>:\n'
        for user_id in all_users[group_id]:
            user_list += f'    {get_user_name(user_id)}\n'
        user_list += '\n'

    return user_list


##### ВОЗВРАЩАЕТ ВСЕХ ПОЛЬЗОВАТЕЛЕЙ ВЫБРАННОЙ ГРУППЫ С ИХ ПОДАРКАМИ #####
def all_users_in_group(message: Message | CallbackQuery) -> str:
    all_gifts = users_gifts_in_group(message)
    group_id = int(message.data)
    gift_list = f"<u><b>{get_group_name(message, group_id).upper()}</b></u>\n\n"

    for user_id in all_gifts.keys():
        gift_list += f'<b>{get_user_name(user_id)}</b>:\n'

        for gift_id in all_gifts[user_id]:
            gift_list += f'    {get_gift_name(gift_id)}\n'
        gift_list += '\n'

    return gift_list


##### ВОЗВРАЩАЕТ СПИСОК ПОДАРКОВ ВЫБРАННОГО ПОЛЬЗОВАТЕЛЯ В ВЫБРАННОЙ ГРУППЕ С ИХ СТАТУСОМ #####
def all_gifts_by_user_in_group(message: Message|CallbackQuery, status=False) -> str:
    user_id = int(message.data[message.data.index('_') + 1:])
    all_gifts = user_gifts_in_group(message)
    gifts = f"<u><b>{get_user_name(user_id).upper()}</b></u>" + '\n\n'

    if status:
        for gift in all_gifts:

            if cursor.execute(f"SELECT giver_id "
                              f"FROM Gifts "
                              f"WHERE gift_id = {gift}").fetchone()[0] == message.from_user.id:
                is_free = LEXICON['you_giver'][user_language(message)]

            elif cursor.execute(f"SELECT giver_id "
                              f"FROM Gifts "
                              f"WHERE gift_id = {gift}").fetchone()[0] != 0:
                is_free = LEXICON['not_free_gift'][user_language(message)]

            else:
                is_free = '     '

            gifts += f"{is_free}{get_gift_name(gift)}\n"
    else:
        for gift in all_gifts:
            gifts += f"{get_gift_name(gift)}\n"

    return gifts


##### ВОЗВРАЩАЕТ СООБЩЕНИЕ С КАРТОЧКОЙ ПОДАРКА #####
def what_to_do_with_gift(callback: CallbackQuery) -> str:
    gift_id = int(callback.data[callback.data.rfind('_') + 1:])
    giver_id = get_giver_id(gift_id)
    gift_name = get_gift_name(gift_id)

    if callback.from_user.id == giver_id:
        return f"<b>{gift_name.upper()}</b>\n\n" + LEXICON['free_up_gift'][user_language(callback)]
    elif giver_id == 0:
        return f"<b>{gift_name.upper()}</b>\n\n" + LEXICON['take_gift'][user_language(callback)]
    else:
        return f"<b>{gift_name.upper()}</b>\n\n" + LEXICON['taken_gift'][user_language(callback)]


##### ВОЗВРАЩАЕТ СПИСОК ОТЗЫВОВ #####
def all_feedback(message: Message | CallbackQuery) -> str:
    feedback = ''

    if len(cursor.execute('SELECT * FROM Feedback').fetchall()) > 0:
        for row in cursor.execute('SELECT * FROM Feedback'):
            feedback += str(row[0]) + '. ' + row[1] + '\n\n'
    else:
        feedback = LEXICON_ADMIN['no_feedback'][user_language(message)]

    return feedback


##### ВОЗВРАЩАЕТ СПИСОК БАГОВ #####
def all_issues(message: Message | CallbackQuery) -> str:
    issues = ''

    if len(cursor.execute('SELECT * FROM Issues').fetchall()) > 0:
        for row in cursor.execute('SELECT * FROM Issues').fetchall():
            if row[2]:
                issues += LEXICON_ADMIN['clothed_issue'][user_language(message)]
            else:
                issues += LEXICON_ADMIN['issue'][user_language(message)]
            issues += str(row[0]) + '. ' + row[1] + '\n\n'
    else:
        issues = LEXICON_ADMIN['no_issue'][user_language(message)]

    return issues



############################################### РАБОТА С ПОЛЬЗОВАТЕЛЯМИ ################################################

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
        group_id = cursor.execute(f"SELECT group_id FROM Groups WHERE password = '{str(user_id)}'").fetchone()[0]
        cursor.execute('INSERT INTO Group_User (group_id, user_id) VALUES (?, ?)',
                       (group_id, int(user_id))
                       )
        db.commit()



################################################# РАБОТА С ПОДАРКАМИ ##################################################

##### ПРОЕРЯЕТ ЕСТЬ ЛИ У ПОЛЬЗОВАТЕЛЯ ПОДАРОК С ТАКИМ ИМЕНЕМ #####
def is_user_has_gift(message: Message|CallbackQuery) -> bool:
    user_id = message.from_user.id
    gift_name = str(message.text)

    return gift_name in [row[0] for row in
                         cursor.execute(
                             f"SELECT gift_name FROM Gifts "
                             f"WHERE user_id = {user_id}"
                         ).fetchall()]


##### ПРОВЕРЯЕТ, ЕСТЬ ЛИ ЗАДАННЫЙ ПОДАРОК В ЗАДАННОЙ ГРУППЕ #####
def is_gift_in_group(group_id: int, gift_id: int) -> bool:
    return [group_id, gift_id] in [
        [row[0], row[1]]
        for row in cursor.execute(
            f"SELECT group_id, gift_id FROM Group_Gift "
            f"WHERE gift_id = {gift_id}"
        ).fetchall()
    ]


##### СОЗДАЕТ НОВЫЙ ПОДАРОК, ПОКА НЕ ПРИВЯЗАННЫЙ НИ К ОДНОЙ ГРУППЕ, ВОЗВРАЩАЕТ ЕГО ID #####
def create_new_gift(message: Message|CallbackQuery) -> int:
    gift_name = str(message.text)
    user_id = int(message.from_user.id)

    gift_id = cursor.execute(
        f"INSERT INTO Gifts (user_id, gift_name) "
        f"VALUES ({user_id}, '{gift_name}') "
        f"RETURNING gift_id"
    ).fetchone()[0]

    db.commit()

    return gift_id


##### ДОБАВЛЯЕТ ПОДАРОК В ВЫБРАННУЮ ГРУППУ #####
def add_new_gift_in_group(message: Message|CallbackQuery) -> None:
    user_id = message.from_user.id
    gift_id = int(message.data[message.data.rfind('_') + 1:])
    chosen_group_id = int(message.data[:message.data.rfind('_')])

    if get_group_name(message, chosen_group_id) == LEXICON['my_own_group'][user_language(message)]:
        accessible_group_ids = [row[0] for row in
                                cursor.execute(
                                    f"SELECT group_id FROM Group_User "
                                    f"WHERE user_id = {user_id}"
                                ).fetchall()]

        for group_id in accessible_group_ids:

            if not is_gift_in_group(group_id, gift_id):
                cursor.execute(f"INSERT INTO Group_Gift (group_id, gift_id) "
                               f"VALUES (?, ?)", (group_id, gift_id))
                db.commit()
    else:
        if not is_gift_in_group(chosen_group_id, gift_id):
            cursor.execute(f"INSERT INTO Group_Gift (group_id, gift_id) "
                           f"VALUES (?, ?)", (chosen_group_id, gift_id))
            db.commit()


##### ЗАНЯТЬ ВЫБРАННЫЙ ПОДАРОК #####
def take_gift(callback: CallbackQuery) -> None:
    digit_data = callback.data[:-len(KEYBOARD_LEXICON['under_gift']['take_gift']['callback'])]
    gift_id = int(digit_data[:digit_data.rfind('_')])
    cursor.execute(f"UPDATE Gifts SET giver_id = {callback.from_user.id} WHERE gift_id = {gift_id}")
    db.commit()


##### ОСВОБОДИТЬ ВЫБРАННЫЙ ПОДАРОК #####
def free_up_gift(callback: CallbackQuery) -> None:
    digit_data = callback.data[:-len(KEYBOARD_LEXICON['under_gift']['free_up_gift']['callback'])]
    gift_id = int(digit_data[:digit_data.rfind('_')])

    cursor.execute(f"UPDATE Gifts SET giver_id = 0 WHERE gift_id = {gift_id}")
    db.commit()


##### УДАЛЕНИЕ ПОДАРКА ПО КНОПКЕ #####
def delete_gift(message: Message|CallbackQuery) -> None:
    gift_id = int(message.data[message.data.rfind('_') + 1:])
    group_id = int(message.data[:message.data.rfind('_')])
    user_id = str(message.from_user.id)

    if group_id == int(cursor.execute(f"SELECT group_id FROM Groups WHERE password = {user_id}").fetchone()[0]):
        cursor.execute(f"DELETE FROM Gifts WHERE gift_id = {gift_id}")
        db.commit()
    else:
        cursor.execute(f"DELETE FROM Group_Gift WHERE group_id = {group_id} AND gift_id = {gift_id}")
        db.commit()

        if len(cursor.execute(f"SELECT * FROM Group_Gift WHERE gift_id = {gift_id}").fetchall()) == 0:
            cursor.execute(f"DELETE FROM Gifts WHERE gift_id = {gift_id}")
            db.commit()



################################################# РАБОТА С ГРУППАМИ  ##################################################

##### ПРОЕРЯЕТ, ЕСТЬ ЛИ ПОЛЬЗОВАТЕЛЬ В ГРУППЕ С НАЗВАНИЕМ, КОТОРОЕ ПЫТАЕТСЯ СОЗДАТЬ #####
def is_user_has_group(message: Message|CallbackQuery) -> bool:
    group_name = str(message.text)
    user_id = int(message.from_user.id)

    return group_name in [row[0] for row in cursor.execute(
        f"SELECT group_name FROM Groups "
        f"INNER JOIN Group_User "
        f"ON Groups.group_id = Group_User.group_id "
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
        f"INSERT INTO Group_User (group_id, user_id) VALUES (?, ?)",
        (cursor.execute(
            f"SELECT group_id FROM Groups WHERE password = '{group_password}'"
        ).fetchone()[0], owner_id)
    )
    db.commit()

    my_own_group_id = cursor.execute(f"SELECT group_id FROM Groups WHERE password = '{str(owner_id)}'").fetchone()[0]
    group_id = cursor.execute(f"SELECT group_id FROM Groups WHERE password = '{group_password}'").fetchone()[0]

    for_everyone_gifts = [
        row[0] for row in
        cursor.execute(
            f"SELECT Gifts.gift_id "
            f"FROM Gifts INNER JOIN Group_Gift ON Gifts.gift_id = Group_Gift.gift_id "
            f"WHERE user_id = {owner_id} AND group_id = {my_own_group_id}"
        ).fetchall()
    ]
    for gift_id in for_everyone_gifts:
        cursor.execute(f"INSERT INTO Group_Gift (group_id, gift_id) "
                       f"VALUES (?, ?)", (group_id, gift_id))
        db.commit()


##### ПРОЕРЯЕТ, ЕСТЬ ЛИ ПОЛЬЗОАТЕЛЬ В ГРУППЕ, В КОТОРУЮ ПЫТАЕТСЯ ВСТУПИТЬ #####
def is_user_in_group(message: Message) -> bool:
    password = str(message.text)
    user_id = int(message.from_user.id)
    group_id = cursor.execute(f"SELECT group_id FROM Groups WHERE password = '{password}'").fetchone()[0]

    return [group_id, user_id] in [[row[0], row[1]] for row in
                                cursor.execute(
                                    f"SELECT group_id, user_id FROM Group_User"
                                ).fetchall()]


##### ПРОВЕРЯЕТ, ЕСТЬ ЛИ У ПОЛЬЗОВАТЕЛЯ ГРУППА С ТАКИМ ЖЕ НАЗВАНИЕМ, КАК ТА, В КОТОРУЮ ПЫТАЕТСЯ ВСТУПИТЬ #####
def is_user_has_same_group(message: Message|CallbackQuery) -> bool:
    password = str(message.text)
    user_id = int(message.from_user.id)
    group_name = cursor.execute(f"SELECT group_name FROM Groups WHERE password = '{password}'").fetchone()[0]

    return group_name in [row[0] for row in cursor.execute(f"SELECT group_name "
                                                           f"FROM Groups "
                                                           f"INNER JOIN Group_User "
                                                           f"ON Groups.group_id = Group_User.group_id "
                                                           f"WHERE user_id = {user_id}")]


##### ВОЗВРАЩАЕТ ПАРОЛЬ ОТ ГРУППЫ #####
def get_password(message: Message | CallbackQuery) -> str:
    group_id = message.data[:message.data.index('_')]
    password = cursor.execute(f"SELECT password FROM Groups WHERE group_id = {group_id}").fetchone()[0]

    return f"<code>{password}</code>"


##### ПРОВЕРЯЕТ КОРРЕКТНОСТЬ ПАРОЛЯ #####
def is_password_correct(message: Message | CallbackQuery) -> bool:
    password = str(message.text)
    if password in [row[0] for row in cursor.execute("SELECT password FROM Groups").fetchall()]:
        return True
    else:
        return False


##### ДОБАВЛЯЕТ ПОЛЬЗОВАТЕЛЯ В ГРУППУ, ПАРОЛЬ К КОТОРОЙ ОН ВВЕЛ #####
def add_user_in_group(message: Message) -> None:
    password = str(message.text)
    user_id = int(message.from_user.id)
    group_id = cursor.execute(f"SELECT group_id FROM Groups WHERE password = '{password}'").fetchone()[0]

    cursor.execute(
        f"INSERT INTO Group_User (group_id, user_id) VALUES (?, ?)",
        (group_id, user_id)
    )
    db.commit()

    my_own_group_id = cursor.execute(f"SELECT group_id FROM Groups WHERE password = '{str(user_id)}'").fetchone()[0]
    for_everyone_gift_ids = [
        row[0] for row in
        cursor.execute(
            f"SELECT Gifts.gift_id "
            f"FROM Gifts "
            f"INNER JOIN Group_Gift "
            f"ON Group_Gift.gift_id = Gifts.gift_id "
            f"WHERE group_id = {my_own_group_id}"
        ).fetchall()
    ]

    for gift_id in for_everyone_gift_ids:
        cursor.execute(f"INSERT INTO Group_Gift (group_id, gift_id) "
                       f"VALUES (?, ?)", (group_id, gift_id))
        db.commit()


##### ПРОВЕРЯЕТ, ЯВЛЯЕТСЯ ЛИ ПОЛЬЗОВАТЕЛЬ ВЛАДЕЛЬЦЕМ ВЫБРАННОЙ ГРУППЫ #####
def user_is_owner(callback: CallbackQuery) -> bool:
    group_id = int(callback.data)
    user_id = callback.from_user.id

    return user_id == cursor.execute(f"SELECT owner_id FROM Groups WHERE group_id == {group_id}").fetchone()[0]


##### УДАЛЯЕТ ВЫБРАННУЮ ГРУППУ #####
def kill_group(callback: Message|CallbackQuery) -> None:
    group_id = int(callback.data[:callback.data.find('_')])

    gifts_in_group = [
        row[0] for row in cursor.execute(
            f"SELECT gift_id "
            f"FROM Group_Gift "
            f"WHERE group_id = {group_id}"
        ).fetchall()
    ]

    cursor.execute(f"DELETE FROM Groups WHERE group_id = {group_id}")
    db.commit()

    for gift_id in gifts_in_group:
        if len(cursor.execute(f"SELECT group_id FROM Group_gift WHERE gift_id = {gift_id}").fetchall()) == 0:
            cursor.execute(f"DELETE FROM Gifts WHERE gift_id = {gift_id}")
            db.commit()


##### ВОЗВРАЩАЕТ СЛОВАРЬ ВИДА {'group_id': {'user_id': [gift_id, ....], ....}, ....} #####
def all_accessible_gifts(message: Message|CallbackQuery) -> dict:
    user_id_from_message = int(message.from_user.id)
    result: dict[int, dict[int, list[int]]] = {}

    accessible_group_ids = [
        row[0] for row in
        cursor.execute(
            f"SELECT group_id "
            f"FROM Group_User "
            f"WHERE user_id = {user_id_from_message}"
        ).fetchall()
    ]

    for group_id in accessible_group_ids:

        users_in_group = [
            row[0] for row in
            cursor.execute(
                f"SELECT user_id "
                f"FROM Group_User "
                f"WHERE group_id = {group_id}"
            ).fetchall()
        ]

        if not(group_id in result.keys()):
            result[group_id] = {}

        for user_id in users_in_group:

            gifts_from_user = [
                row[0] for row in
                cursor.execute(
                    f"SELECT Gifts.gift_id "
                    f"FROM Group_Gift "
                    f"INNER JOIN Gifts "
                    f"ON Group_Gift.gift_id = Gifts.gift_id "
                    f"WHERE Group_Gift.group_id = {group_id} AND Gifts.user_id = {user_id}"
                ).fetchall()
            ]

            if not(user_id in result[group_id].keys()):
                result[group_id][user_id] = []

            for gift_id in gifts_from_user:
                result[group_id][user_id].append(gift_id)

    return result



################################################## РАБОТА С ОТЗЫВАМИ ##################################################

##### ЗАНЕСЕНИЕ НОВОГО ОТЗЫВА В БАЗУ ДАННЫХ #####
def new_feedback(message: Message|CallbackQuery) -> None:
    text = str(message.text)

    cursor.execute(f"INSERT INTO Feedback (feedback_text) VALUES ('{text}')")
    db.commit()


##### УДАЛЯЕТ ОТЗЫВ ПО ЕГО ID #####
def kill_feedback(callback: Message|CallbackQuery) -> None:
    feedback_id = int(callback.data)

    cursor.execute(f"DELETE FROM Feedback WHERE feedback_id = {feedback_id}")
    db.commit()


##### ПЕРЕНОСИТ ОТЗЫВ ИЗ ТАБЛИЦЫ С ОТЗЫВАМИ В ТАБЛИЦУ С ПРОБЛЕМАМИ И ПРИСВАИВАЕТ ЕЙ СТАТУС НЕРЕШЕННОЙ #####
def new_issue(callback: Message | CallbackQuery) -> None:
    feedback_id = int(callback.data)

    feedback_text = cursor.execute(f"SELECT feedback_text "
                                   f"FROM Feedback "
                                   f"WHERE feedback_id = {feedback_id}").fetchone()[0]

    cursor.execute(f"INSERT INTO Issues (issue_text) VALUES ('{feedback_text}')")
    db.commit()
    cursor.execute(f"DELETE FROM Feedback WHERE feedback_id = {feedback_id}")
    db.commit()


##### ИСПРАВЛЕНИЕ ПРОБЛЕМЫ, ОБНАРУЖЕННОЙ ПОЛЬЗОВАТЕЛЕМ #####
def solve_issue(callback: Message|CallbackQuery) -> None:
    trouble_id = int(callback.data)

    cursor.execute(f'UPDATE Issues SET solved = True WHERE issue_id = {trouble_id}')
    db.commit()


##### ДЕЛАЕТ ПРОБЛЕМУ СНОВА АКТУАЛЬНОЙ #####
def not_solve_issue(callback: Message|CallbackQuery) -> None:
    trouble_id = int(callback.data)

    cursor.execute(f'UPDATE Issues SET solved = False WHERE issue_id = {trouble_id}')
    db.commit()


##### УДАЛЯЕТ ПРОБЛЕМУ ПО ЕЕ ID #####
def kill_issue(callback: Message|CallbackQuery) -> None:
    feedback_id = int(callback.data)

    cursor.execute(f"DELETE FROM Issues WHERE issue_id = {feedback_id}")
    db.commit()
