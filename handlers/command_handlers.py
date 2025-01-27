#######################################################################################################################
################################# ФАЙЛ С ХЭНДЛЕРАМИ, ОТВЕЧАЮЩИМИ ЗА ОБРАБОТКУ КОММАНД #################################
#######################################################################################################################


from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.types import Message
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext
from lexicon.lexicon import LEXICON_COMMAND
from database import interact_database as data
from handlers.fsm import FSMCommands
from filters.filters import IsUserInData


##### ИНИЦИАЛИЗАЦИЯ РОУТЕРА #####
router = Router()


##### ХЭНДЛЕР, ОТВЕЧАЮЩИЙ ЗА ПОТОРНЫЙ ВЫЗОВ КОМАНДЫ START #####
@router.message(Command(commands='start'), IsUserInData())
async def repeat_start_command(message: Message):
    await message.answer(text=LEXICON_COMMAND['/start_again'][data.user_language(message.from_user.id)],
                         parse_mode='HTML')


##### ХЭНДЛЕР, ОТВЕЧАЮЩИЙ ЗА КОМАНДУ START В ШТАТНОМ РЕЖИМЕ ДЛЯ ОБЫЧНЫХ ПОЛЬЗОВАТЕЛЕЙ #####
@router.message(Command(commands='start'), StateFilter(default_state))
async def start_command(message: Message, state: FSMContext):
    await message.answer(LEXICON_COMMAND['/start']['ru'][0] +
                         str(message.from_user.first_name) +
                         LEXICON_COMMAND['/start']['ru'][1],
                         parse_mode='HTML')
    await state.set_state(FSMCommands.fill_name)


##### ХЭНДЛЕР, ОТВЕЧАЮЩИЙ ЗА КОМАНДУ HELP В ШТАТНОМ РЕЖИМЕ ДЛЯ ОБЫЧНЫХ ПОЛЬЗОВАТЕЛЕЙ #####
@router.message(Command(commands='help'))
async def help_command(message: Message):
    await message.answer(LEXICON_COMMAND['/help'][data.user_language(message.from_user.id)])
