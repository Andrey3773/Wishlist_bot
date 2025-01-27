from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from lexicon.lexicon import KEYBOARD_LEXICON


def main_menu_button(language: str) -> InlineKeyboardMarkup:
    button = InlineKeyboardButton(text=KEYBOARD_LEXICON['main_menu'][language],
                                  callback_data='main_menu_pressed')
    return InlineKeyboardMarkup(inline_keyboard=[[button]])
