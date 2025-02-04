from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardMarkup, InlineKeyboardBuilder
from lexicon.lexicon import KEYBOARD_LEXICON, LEXICON
from database import interact_database as data


##### КЛАВИАТУРА С ОДНОЙ КНОПКОЙ "В ГЛАВНОЕ МЕНЮ" #####
def main_menu_button(message: Message|CallbackQuery) -> InlineKeyboardMarkup:
    language = data.user_language(message)
    button = InlineKeyboardButton(text=KEYBOARD_LEXICON['main_menu']['main_menu_button'][language],
                                  callback_data=KEYBOARD_LEXICON['main_menu']['main_menu_button']['callback'])
    return InlineKeyboardMarkup(inline_keyboard=[[button]])


##### КЛАВИАТУРА ГЛАВНОГО МЕНЮ #####
def main_menu_keyboard(message: Message|CallbackQuery) -> InlineKeyboardMarkup:
    language = data.user_language(message)
    kb_builder = InlineKeyboardBuilder()
    main_menu_lexicon = KEYBOARD_LEXICON['main_menu']

    buttons: list[InlineKeyboardButton] = [
        InlineKeyboardButton(text=f"{main_menu_lexicon[i][language]}",
                             callback_data=f"{main_menu_lexicon[i]['callback']}"
                             ) for i in main_menu_lexicon if i != 'main_menu_button'
    ]
    kb_builder.row(*buttons, width=2)
    return kb_builder.as_markup(resize_keyboard=True)


##### КЛАВИАТУРА ПОД СПИСКОМ МОИХ ИДЕЙ #####
def my_list_keyboard(message: Message|CallbackQuery) -> InlineKeyboardMarkup:
    language = data.user_language(message)
    kb_builder = InlineKeyboardBuilder()
    new_gift = KEYBOARD_LEXICON['in_my_list']['new_gift']
    delete_gift = KEYBOARD_LEXICON['in_my_list']['delete_gift']
    width = 1

    buttons: list[InlineKeyboardButton] = [
        InlineKeyboardButton(text=new_gift[language],
                             callback_data=new_gift['callback'])
    ]
    if data.all_my_own_gifts(message) != LEXICON['no_gifts'][language]:
        buttons.append(
            InlineKeyboardButton(text=delete_gift[language],
                                 callback_data=delete_gift['callback'])
        )
        width = 2

    button_main_menu = [
        InlineKeyboardButton(text=KEYBOARD_LEXICON['main_menu']['main_menu_button'][language],
                             callback_data=KEYBOARD_LEXICON['main_menu']['main_menu_button']['callback'])
    ]

    kb_builder.row(*buttons, width=width)
    kb_builder.row(*button_main_menu, width=1)

    return kb_builder.as_markup(resize_keyboard=True)


##### КЛАВИАТУРА ПОД СПИСКОМ ПОЛЬЗОВАТЕЛЕЙ ПО ГРУППАМ (СО СПИСКОМ ГРУПП) #####
def my_groups_keyboard(message: Message|CallbackQuery, not_all=True) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    all_users = data.users_in_groups(message, not_all=not_all)
    language = data.user_language(message)
    buttons = []

    for i in all_users:
        buttons.append(
            InlineKeyboardButton(
                text=data.get_group_name(message, i),
                callback_data=str(i)
            )
        )
    button_main_menu = [
        InlineKeyboardButton(text=KEYBOARD_LEXICON['main_menu']['main_menu_button'][language],
                             callback_data=KEYBOARD_LEXICON['main_menu']['main_menu_button']['callback'])
    ]

    kb_builder.row(*buttons, width=2)
    kb_builder.row(*button_main_menu, width=1)

    return kb_builder.as_markup(resize_keyboard=True)


##### КЛАВИАТУРА ГРУПП ДЛЯ ДОБАВЛЕНИЯ НОВОГО ПОДАРКА #####
def my_groups_for_new_gift_keyboard(
        message: Message|CallbackQuery,
        gift_id,
        is_button_no=False,
        not_all=False) -> InlineKeyboardMarkup:

    kb_builder = InlineKeyboardBuilder()
    group_ids = data.users_in_groups(message, not_all=not_all)
    language = data.user_language(message)
    gift_id = int(gift_id)
    buttons = []

    for group_id in group_ids:
        if not data.is_gift_in_group(int(group_id), int(gift_id)):
            buttons.append(
                InlineKeyboardButton(
                    text=data.get_group_name(message, group_id),
                    callback_data=str(group_id) + '_' + str(gift_id)
                )
            )
    service_buttons = []
    if not is_button_no:
        service_buttons.append(
            InlineKeyboardButton(text=KEYBOARD_LEXICON['main_menu']['main_menu_button'][language],
                                 callback_data=KEYBOARD_LEXICON['main_menu']['main_menu_button']['callback'])
        )
    else:
        service_buttons.append(
            InlineKeyboardButton(text=KEYBOARD_LEXICON['no_button']['no'][language],
                                 callback_data=KEYBOARD_LEXICON['no_button']['no']['callback'])
        )

    kb_builder.row(*buttons, width=2)
    kb_builder.row(*service_buttons, width=1)

    return kb_builder.as_markup(resize_keyboard=True)


##### КЛАВИАТУРА ПОД СПИСКОМ ПОДАРКОВ ПО ПОЛЬЗОВАТЕЛЯМ (СО СПИСКОМ ПОЛЬЗОВАТЕЛЕЙ) #####
def under_group_keyboard(message: Message | CallbackQuery) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    all_users = data.users_gifts_in_group(message)
    language = data.user_language(message)
    buttons = []

    for i in all_users:
        if i != message.from_user.id:
            buttons.append(
                InlineKeyboardButton(
                    text=data.get_user_name(i),
                    callback_data=message.data + '_' + str(i)
                )
            )
    service_buttons = [
        InlineKeyboardButton(text=KEYBOARD_LEXICON['group_password']['get_password'][language],
                             callback_data=message.data + '_' +
                                           KEYBOARD_LEXICON['group_password']['get_password']['callback']),
        InlineKeyboardButton(text=KEYBOARD_LEXICON['main_menu']['main_menu_button'][language],
                             callback_data=KEYBOARD_LEXICON['main_menu']['main_menu_button']['callback'])
    ]

    kb_builder.row(*buttons, width=3)
    kb_builder.row(*service_buttons, width=1)

    return kb_builder.as_markup(resize_keyboard=True)


##### КЛАВИАТУРЕ ПОД СПИСКОМ ПОДАРКОВ ВЫБРАННОГО ПОЛЬЗОВАТЕЛЯ (СО СПИСКОМ ПОДАРКОВ) #####
def gifts_by_user_keyboard(message: Message|CallbackQuery) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    all_gifts = data.users_gifts(message)
    language = data.user_language(message)
    buttons = []

    for i in all_gifts:
        buttons.append(
            InlineKeyboardButton(
                text=data.get_gift_name(i),
                callback_data=message.data + '_' + str(i)
            )
        )
    service_buttons = [
        InlineKeyboardButton(text=KEYBOARD_LEXICON['main_menu']['main_menu_button'][language],
                             callback_data=KEYBOARD_LEXICON['main_menu']['main_menu_button']['callback'])
    ]

    kb_builder.row(*buttons, width=3)
    kb_builder.row(*service_buttons, width=2)

    return kb_builder.as_markup(resize_keyboard=True)


##### КЛАВИАТУРА ПОД КАРТОЧКОЙ ПОДАРКА #####
def under_gift_keyboard(callback: Message|CallbackQuery) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()

    gift_id = int(callback.data[callback.data.rfind('_') + 1:])
    giver_id = data.get_giver_id(gift_id)
    language = data.user_language(callback)

    if giver_id == callback.from_user.id:
        buttons = [
            InlineKeyboardButton(
                text=KEYBOARD_LEXICON['under_gift']['free_up_gift'][language],
                callback_data=str(gift_id) + '_' + KEYBOARD_LEXICON['under_gift']['free_up_gift']['callback']
            )
        ]
    elif giver_id == 0:
        buttons = [
            InlineKeyboardButton(
                text=KEYBOARD_LEXICON['under_gift']['take_gift'][language],
                callback_data=str(gift_id) + '_' + KEYBOARD_LEXICON['under_gift']['take_gift']['callback']
            )
        ]
    else:
        buttons = []

    service_buttons = [
        InlineKeyboardButton(text=KEYBOARD_LEXICON['main_menu']['main_menu_button'][language],
                             callback_data=KEYBOARD_LEXICON['main_menu']['main_menu_button']['callback'])
    ]

    kb_builder.row(*buttons)
    kb_builder.row(*service_buttons)

    return kb_builder.as_markup(resize_keyboard=True)


##### ОТДЕЛЬНАЯ КНОПКА НАЗАД #####
def back_button(message: Message|CallbackQuery) -> InlineKeyboardMarkup:
    language = data.user_language(message)
    button = InlineKeyboardButton(text=KEYBOARD_LEXICON['admin_lower']['back'][language],
                                  callback_data=KEYBOARD_LEXICON['admin_lower']['back']['callback'])
    return InlineKeyboardMarkup(inline_keyboard=[[button]])


##### КНОПКА ОК ДЛЯ УВЕДОМЛЕНИЯ О ЧЕМ-ТО СТРАННОМ И УДАЛЕНИЯ ЭТОГО СООБЩЕНИЯ #####
def ok_button(message: Message|CallbackQuery) -> InlineKeyboardMarkup:
    language = data.user_language(message)
    button = InlineKeyboardButton(text=KEYBOARD_LEXICON['ok_button']['ok'][language],
                                  callback_data=KEYBOARD_LEXICON['ok_button']['ok']['callback'])
    return InlineKeyboardMarkup(inline_keyboard=[[button]])
