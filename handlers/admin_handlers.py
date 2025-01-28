#######################################################################################################################
############################# ФАЙЛ С ХЭНДЛЕРАМИ, ОТВЕЧАЮЩИМИ ЗА ВЗАИМОДЕЙСТВИЕ С АДМИНАМИ #############################
#######################################################################################################################


from aiogram import Router, Bot
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from config_data.config import Config, load_config
from filters.filters import IsAdmin, IsUserInData
from lexicon.lexicon import LEXICON_ADMIN
from database.interact_database import user_language
from handlers.fsm import FSMCommands
from database import interact_database as data
from asyncio import sleep



##### ИНИЦИАЛИЗАЦИЯ РОУТЕРА #####
router = Router()


##### ИНИЦИАЛИЗАЦИЯ КОНФИГУРАТОРА, ЧТОБЫ ДОСТАТЬ ИЗ НЕГО БОТА #####
config: Config = load_config('.env')
bot = Bot(token=config.bot.token)


##### ИНИЦИАЛИЗАЦИЯ КОНФИГУРАТОРА, ЧТОБЫ ДОСТАТЬ ИЗ НЕГО СПИСОК АДМИНОВ #####
admins_config: Config = load_config('.env')


##### ХЭНДЛЕР, ОТВЕЧАЮЩИЙ ЗА ОБРАБОТКУ ПОВТОРНОГО ВЫЗОВА КОМАНДЫ START ОТ АДМИНОВ ######
@router.message(Command(commands='start'), IsUserInData(), IsAdmin(admins_config.bot.admins))
async def admin_start_again(message: Message):
    sent_message = await message.answer(LEXICON_ADMIN['/start_again'][user_language(message)])
    await sleep(60)
    await message.delete()
    await bot.delete_message(chat_id=message.chat.id, message_id=sent_message.message_id)


##### ХЭНДЛЕР, ОТВЕЧАЮЩИЙ ЗА КОМАНДУ START В ШТАТНОМ РЕЖИМЕ ДЛЯ АДМИНОВ #####
@router.message(Command(commands='start'), IsAdmin(admins_config.bot.admins))
async def start_command(message: Message, state: FSMContext):
    await message.answer(LEXICON_ADMIN['/start']['ru'])
    await state.set_state(FSMCommands.fill_name)


##### ХЭНДЛЕР, ОТЕЧАЮЩИЙ ЗА ВЫВОД ФИДБЭКА ПОЛЬЗОАТЕЛЕЙ ДЛЯ АДМИНОВ #####
@router.message(Command(commands='feedback'), IsAdmin(admins_config.bot.admins))
async def give_feedback(message: Message):
    sent_message = await message.answer(data.all_feedback())
    await sleep(60)
    await message.delete()
    await bot.delete_message(chat_id=message.chat.id, message_id=sent_message.message_id)
