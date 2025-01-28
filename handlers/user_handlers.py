#######################################################################################################################
################### ФАЙЛ С ХЭНДЛЕРАМИ, ОТВЕЧАЮЩИМИ ЗА ШТАТНУЮ РАБОТУ БОТА С ОБЫЧНЫМИ ПОЛЬЗОВАТЕЛЯМИ ###################
#######################################################################################################################

from aiogram import Router, Bot, F
from aiogram.filters import StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from lexicon.lexicon import LEXICON, LEXICON_COMMAND
from database import interact_database as data
from handlers.fsm import FSMCommands
from config_data.config import Config, load_config
from asyncio import sleep
from keyboards.keyboards import main_menu_button, main_menu


##### ИНИЦИАЛИЗАЦИЯ РОУТЕРА #####
router = Router()


##### ИНИЦИАЛИЗАЦИЯ КОНФИГУРАТОРА, ЧТОБЫ ДОСТАТЬ ИЗ НЕГО БОТА #####
config: Config = load_config('.env')
bot = Bot(token=config.bot.token)


##### ХЭНДЛЕР, ОТВЕЧАЮЩИЙ ЗА ПРИНЯТИЕ ОТЗЫВА #####
@router.message(StateFilter(FSMCommands.fill_feedback), F.text)
async def take_feedback(message: Message, state: FSMContext):
    sent_message = await message.answer(text=LEXICON['correct_feedback'][data.user_language(message)])
    data.new_feedback(message)
    await state.clear()
    await sleep(10)
    await message.delete()
    await bot.delete_message(chat_id=message.chat.id, message_id=sent_message.message_id)


##### ХЭНДЛЕР, ОТВЕЧАЮЩИЙ ЗА ОБРАБОТКУ НАЖАТИЯ КНОПКИ ГЛАВНОЕ МЕНЮ #####
@router.callback_query(F.data == 'main_menu_pressed')
async def main_menu_pressed(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text(text=LEXICON['main_menu'][data.user_language(callback)],
                                     reply_markup=main_menu(data.user_language(callback)))


##### ХЭНДЛЕР, ОТВЕЧАЮЩИЙ ЗА КОМАНДУ FEEDBACK В ШТАТНОМ РЕЖИМЕ ДЛЯ ОБЫЧНЫХ ПОЛЬЗОВАТЕЛЕЙ #####
@router.callback_query(F.data == 'feedback')
async def feedback_command(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON_COMMAND['/feedback'][data.user_language(callback)],
                                     reply_markup=main_menu_button(data.user_language(callback)))
    await state.set_state(FSMCommands.fill_feedback)
