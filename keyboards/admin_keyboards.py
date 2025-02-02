from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardMarkup, InlineKeyboardBuilder
from lexicon.lexicon import KEYBOARD_LEXICON
from database import interact_database as data


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
