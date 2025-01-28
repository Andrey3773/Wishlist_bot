from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardMarkup, InlineKeyboardBuilder
from lexicon.lexicon import KEYBOARD_LEXICON


##### КЛАВИАТУРА С ОДНОЙ КНОПКОЙ "В ГЛАВНОЕ МЕНЮ" #####
def main_menu_button(language: str) -> InlineKeyboardMarkup:
    button = InlineKeyboardButton(text=KEYBOARD_LEXICON['main_menu_button'][language],
                                  callback_data='main_menu_pressed')
    return InlineKeyboardMarkup(inline_keyboard=[[button]])


##### КЛАВИАТУРА ГЛАВНОГО МЕНЮ #####
def main_menu(language: str) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    main_menu_lexicon = KEYBOARD_LEXICON['main_menu']

    buttons: list[InlineKeyboardButton] = [
        InlineKeyboardButton(text=f"{main_menu_lexicon[language][i]}",
                             callback_data=f"{main_menu_lexicon['callback'][i]}"
                             ) for i in range(len(main_menu_lexicon[language]))
    ]
    kb_builder.row(*buttons, width=2)
    return kb_builder.as_markup(resize_keyboard=True)

