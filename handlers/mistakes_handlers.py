######################################################################################################################
############## ФАЙЛ С ХЭНДЛЕРАМИ, ОТВЕЧАЮЩИМИ ЗА ОБРАБОТКУ НЕКОРРЕТНЫХ ДЕЙСТВИЙ СО СТОРОНЫ ПОЛЬЗОВАТЕЛЯ ##############
######################################################################################################################


from aiogram import Router, Bot
from aiogram.filters import StateFilter
from aiogram.types import Message
from lexicon.lexicon import WRONG_LEXICON
from handlers.fsm import FSMCommands
from config_data.config import Config, load_config
from asyncio import sleep


##### ИНИЦИАЛИЗАЦИЯ РОУТЕРА #####
router = Router()


##### ИНИЦИАЛИЗАЦИЯ КОНФИГУРАТОРА, ЧТОБЫ ДОСТАТЬ ИЗ НЕГО БОТА #####
config: Config = load_config('.env')
bot = Bot(token=config.bot.token)


##### ХЭНДЛЕР ОТВЕЧАЮЩИЙ ЗА НЕКОРРЕКТНУЮ РЕГИСТРАЦИЮ #####
@router.message(StateFilter(FSMCommands.fill_name))
async def incorrect_registration(message: Message):
    sent_message = await message.answer(WRONG_LEXICON['incorrect_registration']['ru'])
    await sleep(60)
    await message.delete()
    await bot.delete_message(chat_id=message.chat.id, message_id=sent_message.message_id)


##### ХЭНДЛЕР, ОТВЕЧАЮЩИЙ ЗА НЕКОРРЕКТНО ВВЕДЕННЫЙ ОТЗЫВ #####
@router.message(StateFilter(FSMCommands.fill_feedback))
async def incorrect_feedback(message: Message):
    sent_message = await message.answer(WRONG_LEXICON['incorrect_feedback']['ru'])
    await sleep(60)
    await message.delete()
    await bot.delete_message(chat_id=message.chat.id, message_id=sent_message.message_id)


##### ХЭНДЛЕР, ОТВЕЧАЮЩИЙ ЗА ВСЕ НЕПРЕДУСМОТРЕННЫЕ ДЕЙСТВИЯ ПОЛЬЗОВАТЕЛЯ #####
@router.message()
async def other_messages(message: Message):
    sent_message = await message.answer(WRONG_LEXICON['other']['ru'])
    await sleep(60)
    await message.delete()
    await bot.delete_message(chat_id=message.chat.id, message_id=sent_message.message_id)
