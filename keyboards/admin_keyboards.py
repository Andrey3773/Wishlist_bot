from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardMarkup, InlineKeyboardBuilder

from config_data.config import Database
from lexicon.lexicon import KEYBOARD_LEXICON
from database import interact_database as data


##### КЛАВИАТУРА ДЛЯ ВЫБОРА ЧТО ДЕЛАТЬ С ОТЗЫВОМ #####
def admin_feedback_keyboard(db_access: Database, message: Message|CallbackQuery) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    buttons = []
    language = data.user_language(db_access, message)

    for i in KEYBOARD_LEXICON['admin']:
        buttons.append(
            InlineKeyboardButton(
                text=KEYBOARD_LEXICON['admin'][i][language],
                callback_data=KEYBOARD_LEXICON['admin'][i]['callback']
            )
        )

    kb_builder.row(*buttons, width=2)

    return kb_builder.as_markup()


##### КЛАВИАТУРА ДЛЯ АДМИНОВ ПОД СПИСКОМ БАГОВ #####
def admin_issues_keyboard(db_access: Database, message: Message|CallbackQuery):
    kb_builder = InlineKeyboardBuilder()
    language = data.user_language(db_access, message)

    buttons = [
        InlineKeyboardButton(text=str(i), callback_data=str(i)) for i in data.issue_list(db_access)
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
def admin_feedback_list_keyboard(db_access: Database, message: Message | CallbackQuery) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    language = data.user_language(db_access, message)

    buttons = [
        InlineKeyboardButton(text=str(i), callback_data=str(i)) for i in data.feedback_list(db_access)
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


##### КЛАВИАТУРА ДЛЯ ВЫБОРА ЧТО ДЕЛАТЬ С БАГОМ #####
def admin_solve_issue(db_access: Database, message: Message|CallbackQuery) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    buttons = []
    language = data.user_language(db_access, message)

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
