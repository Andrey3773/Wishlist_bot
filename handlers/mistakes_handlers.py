######################################################################################################################
############## ФАЙЛ С ХЭНДЛЕРАМИ, ОТВЕЧАЮЩИМИ ЗА ОБРАБОТКУ НЕКОРРЕТНЫХ ДЕЙСТВИЙ СО СТОРОНЫ ПОЛЬЗОВАТЕЛЯ ##############
######################################################################################################################


from aiogram import Router, Bot
from aiogram.filters import StateFilter, Command
from aiogram.types import Message
from lexicon.lexicon import WRONG_LEXICON, LEXICON
from handlers.fsm import FSMCommands
from aiogram.fsm.context import FSMContext
from config_data.config import Config, load_config
from asyncio import sleep
from database import interact_database as data
from keyboards.keyboards import main_menu


##### ИНИЦИАЛИЗАЦИЯ РОУТЕРА #####
router = Router()


##### ИНИЦИАЛИЗАЦИЯ КОНФИГУРАТОРА, ЧТОБЫ ДОСТАТЬ ИЗ НЕГО БОТА #####
config: Config = load_config('.env')
bot = Bot(token=config.bot.token)


##### ХЭНДЛЕР ОТВЕЧАЮЩИЙ ЗА НЕКОРРЕКТНУЮ РЕГИСТРАЦИЮ #####
@router.message(StateFilter(FSMCommands.fill_name))
async def incorrect_registration(message: Message):
    sent_message = await message.answer(WRONG_LEXICON['incorrect_registration']['ru'])
    await sleep(10)
    await message.delete()
    await bot.delete_message(chat_id=message.chat.id, message_id=sent_message.message_id)


##### ХЭНДЛЕР, ОТВЕЧАЮЩИЙ ЗА НЕКОРРЕКТНО ВВЕДЕННЫЙ ОТЗЫВ #####
@router.message(StateFilter(FSMCommands.fill_feedback))
async def incorrect_feedback(message: Message):
    sent_message = await message.answer(WRONG_LEXICON['incorrect_feedback']['ru'])
    await sleep(10)
    await message.delete()
    await bot.delete_message(chat_id=message.chat.id, message_id=sent_message.message_id)


##### НА СЛУЧАЙ, ЕСЛИ ПОЛЬЗОВАТЕЛЬ ИДИОТ И УДАЛИЛ МЕНЮ #####
@router.message(Command(commands='help'))
async def command_help(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(text=LEXICON['help'][data.user_language(message)])
    await message.answer(text=LEXICON['main_menu'][data.user_language(message)],
                                     reply_markup=main_menu(data.user_language(message)))


##### ХЭНДЛЕР, ОТВЕЧАЮЩИЙ ЗА ВСЕ НЕПРЕДУСМОТРЕННЫЕ ДЕЙСТВИЯ ПОЛЬЗОВАТЕЛЯ #####
@router.message()
async def other_messages(message: Message):
    sent_message = await message.answer(WRONG_LEXICON['other']['ru'])
    await sleep(10)
    await message.delete()
    await bot.delete_message(chat_id=message.chat.id, message_id=sent_message.message_id)
