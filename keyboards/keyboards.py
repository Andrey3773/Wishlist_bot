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

    buttons.append(
        InlineKeyboardButton(text=KEYBOARD_LEXICON['main_menu']['main_menu_button'][language],
                             callback_data=KEYBOARD_LEXICON['main_menu']['main_menu_button']['callback'])
    )

    kb_builder.row(*buttons, width=width)

    return kb_builder.as_markup(resize_keyboard=True)


##### КЛАВИАТУРА ПОД СПИСКОМ ПОЛЬЗОВАТЕЛЕЙ ПО ГРУППАМ #####
def my_groups_keyboard(message: Message|CallbackQuery) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    all_users = data.users_in_groups(message)
    buttons = []

    for i in all_users:
        buttons.append(
            InlineKeyboardButton(
                text=data.get_group_name(message, i),
                callback_data=str(i)
            )
        )
    buttons.append(InlineKeyboardButton(text=KEYBOARD_LEXICON['main_menu']['main_menu_button'][data.user_language(message)],
                                  callback_data=KEYBOARD_LEXICON['main_menu']['main_menu_button']['callback']))

    kb_builder.row(*buttons, width=1)

    return kb_builder.as_markup(resize_keyboard=True)


##### КЛАВИАТУРА ДЛЯ АДМИНОВ ПРИ ОТЗЫВАХ #####
def admin_feedback_keyboard(message: Message|CallbackQuery) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    buttons = []
    language = data.user_language(message)

    for i in KEYBOARD_LEXICON['admin']:
        buttons.append(
            InlineKeyboardButton(
                text=KEYBOARD_LEXICON['admin'][i][language],
                callback_data=KEYBOARD_LEXICON['admin'][i]['callback']
            )
        )
    kb_builder.row(*buttons, width=2)
    return kb_builder.as_markup()


##### КЛАВИАТУРА ДЛЯ АДМИНОВ ПОД СПИСКОМ ПРОБЛЕМ #####
def admin_issues_keyboard(message: Message|CallbackQuery):
    kb_builder = InlineKeyboardBuilder()
    language = data.user_language(message)

    buttons = [
        InlineKeyboardButton(text=str(i), callback_data=str(i)) for i in data.issue_list()
    ]

    button_back = [
        InlineKeyboardButton(
            text=KEYBOARD_LEXICON['admin_lower']['back'][language],
            callback_data=KEYBOARD_LEXICON['admin_lower']['back']['callback']
        )
    ]

    kb_builder.row(*buttons, width=5)
    kb_builder.row(*button_back, width=1)

    return kb_builder.as_markup()


##### КЛАВИАТУРА ДЛЯ АДМИНОВ ПОД СПИСКОМ ОТЗЫВОВ #####
def admin_feedbacks_keyboard(message: Message | CallbackQuery) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    language = data.user_language(message)

    buttons = [
        InlineKeyboardButton(text=str(i), callback_data=str(i)) for i in data.feedback_list()
    ]

    button_back = [
            InlineKeyboardButton(
                text=KEYBOARD_LEXICON['admin_lower']['back'][language],
                callback_data=KEYBOARD_LEXICON['admin_lower']['back']['callback']
            )
    ]

    kb_builder.row(*buttons, width=5)
    kb_builder.row(*button_back, width=1)

    return kb_builder.as_markup()


##### КЛАВИАТУРА ДЛЯ ВЫБОРА ЧЕ ДЕЛАТЬ С ПРОБЛЕМОЙ #####
def admin_solve_issue(message: Message|CallbackQuery) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    buttons = []
    language = data.user_language(message)

    for i in KEYBOARD_LEXICON['admin_in_issues']:
        buttons.append(
            InlineKeyboardButton(
                text=KEYBOARD_LEXICON['admin_in_issues'][i][language],
                callback_data=KEYBOARD_LEXICON['admin_in_issues'][i]['callback']
            )
        )

    buttons.append(InlineKeyboardButton(text=KEYBOARD_LEXICON['admin_lower']['back'][language],
                                        callback_data=KEYBOARD_LEXICON['admin_lower']['back']['callback']))

    kb_builder.row(*buttons, width=3)
    return kb_builder.as_markup()


##### ОТДЕЛЬНАЯ КНОПКА НАЗАД #####
def back_button(message: Message|CallbackQuery) -> InlineKeyboardMarkup:
    language = data.user_language(message)
    button = InlineKeyboardButton(text=KEYBOARD_LEXICON['admin_lower']['back'][language],
                                  callback_data=KEYBOARD_LEXICON['admin_lower']['back']['callback'])
    return InlineKeyboardMarkup(inline_keyboard=[[button]])


