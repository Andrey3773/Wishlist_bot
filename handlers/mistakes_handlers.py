######################################################################################################################
############## ФАЙЛ С ХЭНДЛЕРАМИ, ОТВЕЧАЮЩИМИ ЗА ОБРАБОТКУ НЕКОРРЕТНЫХ ДЕЙСТВИЙ СО СТОРОНЫ ПОЛЬЗОВАТЕЛЯ ##############
######################################################################################################################


from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.types import Message
from lexicon.lexicon import WRONG_LEXICON
from handlers.fsm import FSMCommands
from database import interact_database as data


##### ИНИЦИАЛИЗАЦИЯ РОУТЕРА #####
router = Router()


##### ХЭНДЛЕР ОТВЕЧАЮЩИЙ ЗА НЕКОРРЕКТНУЮ РЕГИСТРАЦИЮ #####
@router.message(StateFilter(FSMCommands.fill_name))
async def incorrect_registration(message: Message):
    await message.answer(WRONG_LEXICON['incorrect_registration']['ru'])


##### ХЭНДЛЕР, ОТВЕЧАЮЩИЙ ЗА ВСЕ НЕПРЕДУСМОТРЕННЫЕ ДЕЙСТВИЯ ПОЛЬЗОВАТЕЛЯ #####
@router.message()
async def other_messages(message: Message):
    await message.answer(WRONG_LEXICON['other']['ru'])
