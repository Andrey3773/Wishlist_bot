from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardMarkup, InlineKeyboardBuilder
from lexicon.lexicon import KEYBOARD_LEXICON, LEXICON
from database.interact_database import all_my_gifts


##### КЛАВИАТУРА С ОДНОЙ КНОПКОЙ "В ГЛАВНОЕ МЕНЮ" #####
def main_menu_button(language: str) -> InlineKeyboardMarkup:
    button = InlineKeyboardButton(text=KEYBOARD_LEXICON['main_menu_button'][language],
                                  callback_data=KEYBOARD_LEXICON['main_menu_button']['callback'])
    return InlineKeyboardMarkup(inline_keyboard=[[button]])


##### КЛАВИАТУРА ГЛАВНОГО МЕНЮ #####
def main_menu_keyboard(language: str) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    main_menu_lexicon = KEYBOARD_LEXICON['main_menu']

    buttons: list[InlineKeyboardButton] = [
        InlineKeyboardButton(text=f"{main_menu_lexicon[language][i]}",
                             callback_data=f"{main_menu_lexicon['callback'][i]}"
                             ) for i in main_menu_lexicon[language]
    ]
    kb_builder.row(*buttons, width=2)
    return kb_builder.as_markup(resize_keyboard=True)


##### КЛАВИАТУРА ПОД СПИСКОМ МОИХ ИДЕЙ #####
def my_list_keyboard(language: str, message: Message|CallbackQuery) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    new_gift = KEYBOARD_LEXICON['new_gift']
    delete_gift = KEYBOARD_LEXICON['delete_gift']
    width = 1

    buttons: list[InlineKeyboardButton] = [
        InlineKeyboardButton(text=new_gift[language],
                             callback_data=new_gift['callback'])
    ]
    if all_my_gifts(message) != LEXICON['no_gifts'][language]:
        buttons.append(
            InlineKeyboardButton(text=delete_gift[language],
                                 callback_data=delete_gift['callback'])
        )
        width = 2

    buttons.append(
        InlineKeyboardButton(text=KEYBOARD_LEXICON['main_menu_button'][language],
                             callback_data=KEYBOARD_LEXICON['main_menu_button']['callback'])
    )

    kb_builder.row(*buttons, width=width)

    return kb_builder.as_markup(resize_keyboard=True)
