#######################################################################################################################
################################# ФАЙЛ С ХЭНДЛЕРАМИ, ОТВЕЧАЮЩИМИ ЗА ОБРАБОТКУ КОММАНД #################################
#######################################################################################################################


from aiogram import Router, Bot
from aiogram.filters import Command, StateFilter
from aiogram.types import Message
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext
from lexicon.lexicon import LEXICON_COMMAND
from database import interact_database as data
from handlers.fsm import FSMCommands
from filters.filters import IsUserInData
from config_data.config import Config, load_config
from asyncio import sleep


##### ИНИЦИАЛИЗАЦИЯ РОУТЕРА #####
router = Router()


##### ИНИЦИАЛИЗАЦИЯ КОНФИГУРАТОРА, ЧТОБЫ ДОСТАТЬ ИЗ НЕГО БОТА #####
config: Config = load_config('.env')
bot = Bot(token=config.bot.token)


##### ХЭНДЛЕР, ОТВЕЧАЮЩИЙ ЗА ПОТОРНЫЙ ВЫЗОВ КОМАНДЫ START #####
@router.message(Command(commands='start'), IsUserInData())
async def repeat_start_command(message: Message):
    sent_message = await message.answer(text=LEXICON_COMMAND['/start_again'][data.user_language(message.from_user.id)],
                                        parse_mode='HTML')

    await sleep(60)
    await message.delete()
    await bot.delete_message(chat_id=message.chat.id, message_id=sent_message.message_id)


##### ХЭНДЛЕР, ОТВЕЧАЮЩИЙ ЗА КОМАНДУ START В ШТАТНОМ РЕЖИМЕ ДЛЯ ОБЫЧНЫХ ПОЛЬЗОВАТЕЛЕЙ #####
@router.message(Command(commands='start'), StateFilter(default_state))
async def start_command(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_COMMAND['/start']['ru'][0] +
                         str(message.from_user.first_name) +
                         LEXICON_COMMAND['/start']['ru'][1],
                         parse_mode='HTML')
    await state.set_state(FSMCommands.fill_name)



##### ХЭНДЛЕР, ОТВЕЧАЮЩИЙ ЗА КОМАНДУ HELP В ШТАТНОМ РЕЖИМЕ ДЛЯ ОБЫЧНЫХ ПОЛЬЗОВАТЕЛЕЙ #####
@router.message(Command(commands='help'))
async def help_command(message: Message):
    sent_message = await message.answer(LEXICON_COMMAND['/help'][data.user_language(message.from_user.id)])

    await sleep(60)
    await message.delete()
    await bot.delete_message(chat_id=message.chat.id, message_id=sent_message.message_id)


##### ХЭНДЛЕР, ОТВЕЧАЮЩИЙ ЗА КОМАНДУ FEEDBACK В ШТАТНОМ РЕЖИМЕ ДЛЯ ОБЫЧНЫХ ПОЛЬЗОВАТЕЛЕЙ #####
@router.message(Command(commands='feedback'))
async def feedback_command(message: Message, state: FSMContext):
    sent_message = await message.answer(LEXICON_COMMAND['/feedback'][data.user_language(message.from_user.id)])
    await state.set_state(FSMCommands.fill_feedback)

    await sleep(30)
    await message.delete()
    await bot.delete_message(chat_id=message.chat.id, message_id=sent_message.message_id)
