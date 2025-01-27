#######################################################################################################################
############################# ФАЙЛ С ХЭНДЛЕРАМИ, ОТВЕЧАЮЩИМИ ЗА ВЗАИМОДЕЙСТВИЕ С АДМИНАМИ #############################
#######################################################################################################################
from tracemalloc import Frame

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from config_data.config import Config, load_config
from filters.filters import IsAdmin, IsUserInData
from lexicon.lexicon import LEXICON_ADMIN
from database.interact_database import user_language
from handlers.fsm import FSMCommands


##### ИНИЦИАЛИЗАЦИЯ РОУТЕРА #####
router = Router()

##### ИНИЦИАЛИЗАЦИЯ КОНФИГУРАТОРА, ЧТОБЫ ДОСТАТЬ ИЗ НЕГО СПИСОК АДМИНОВ #####
admins_config: Config = load_config('.env')


##### ХЭНДЛЕР, ОТВЕЧАЮЩИЙ ЗА ОБРАБОТКУ ПОВТОРНОГО ВЫЗОВА КОМАНДЫ START ОТ АДМИНОВ ######
@router.message(Command(commands='start'), IsUserInData(), IsAdmin(admins_config.bot.admins))
async def admin_start_again(message: Message):
    await message.answer(LEXICON_ADMIN['/start_again'][user_language(message.from_user.id)])


##### ХЭНДЛЕР, ОТВЕЧАЮЩИЙ ЗА КОМАНДУ START В ШТАТНОМ РЕЖИМЕ ДЛЯ АДМИНОВ #####
@router.message(Command(commands='start'), IsAdmin(admins_config.bot.admins))
async def start_command(message: Message, state: FSMContext):
    await message.answer(LEXICON_ADMIN['/start']['ru'])
    await state.set_state(FSMCommands.fill_name)


##### ХЭНДЛЕР, ОТЕЧАЮЩИЙ ЗА ВЫВОД ФИДБЭКА ПОЛЬЗОАТЕЛЕЙ ДЛЯ АДМИНОВ #####
@router.message(Command(commands='feedback'), IsAdmin(admins_config.bot.admins))
async def give_feedback(message: Message):
    await message.answer(LEXICON_ADMIN['/feedback'][user_language(message.from_user.id)])
