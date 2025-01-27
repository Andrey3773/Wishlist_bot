#######################################################################################################################
################### ФАЙЛ С ХЭНДЛЕРАМИ, ОТВЕЧАЮЩИМИ ЗА ШТАТНУЮ РАБОТУ БОТА С ОБЫЧНЫМИ ПОЛЬЗОВАТЕЛЯМИ ###################
#######################################################################################################################

from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from lexicon.lexicon import LEXICON
from database import interact_database as data
from handlers.fsm import FSMCommands
from filters.filters import IsNameCorrect


##### ИНИЦИАЛИЗАЦИЯ РОУТЕРА #####
router = Router()


##### ХЭНДЛЕР ОТЕЧАЮЩИЙ ЗА УСПЕШНУЮ РЕГИСТРАЦИЮ #####
@router.message(StateFilter(FSMCommands.fill_name), IsNameCorrect())
async def correct_registration(message: Message, state: FSMContext):
    data.new_user(message.from_user.id, message.text)
    await message.answer(LEXICON['correct_registration'][data.user_language(message.from_user.id)][0] +
                         data.give_name(int(message.from_user.id)) +
                         LEXICON['correct_registration'][data.user_language(message.from_user.id)][1])
    await state.clear()


