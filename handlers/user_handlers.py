#######################################################################################################################
################### ФАЙЛ С ХЭНДЛЕРАМИ, ОТВЕЧАЮЩИМИ ЗА ШТАТНУЮ РАБОТУ БОТА С ОБЫЧНЫМИ ПОЛЬЗОВАТЕЛЯМИ ###################
#######################################################################################################################
from gc import callbacks

from aiogram import Router, Bot, F
from aiogram.filters import StateFilter
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from lexicon.lexicon import LEXICON, LEXICON_COMMAND
from database import interact_database as data
from handlers.fsm import FSMCommands
from filters.filters import IsNameCorrect
from config_data.config import Config, load_config
from asyncio import sleep
from keyboards.keyboards import main_menu_button


##### ИНИЦИАЛИЗАЦИЯ РОУТЕРА #####
router = Router()


##### ИНИЦИАЛИЗАЦИЯ КОНФИГУРАТОРА, ЧТОБЫ ДОСТАТЬ ИЗ НЕГО БОТА #####
config: Config = load_config('.env')
bot = Bot(token=config.bot.token)


##### ХЭНДЛЕР ОТЕЧАЮЩИЙ ЗА УСПЕШНУЮ РЕГИСТРАЦИЮ #####
@router.message(StateFilter(FSMCommands.fill_name), IsNameCorrect())
async def correct_registration(message: Message, state: FSMContext):
    data.new_user(message.from_user.id, message.text)
    await message.answer(LEXICON['correct_registration'][data.user_language(message.from_user.id)][0] +
                         data.give_name(int(message.from_user.id)) +
                         LEXICON['correct_registration'][data.user_language(message.from_user.id)][1])
    await state.clear()
    await sleep(0.5)
    await message.answer(LEXICON_COMMAND['/help'][data.user_language(message.from_user.id)])


##### ХЭНДЛЕР, ОТВЕЧАЮЩИЙ ЗА ПРИНЯТИЕ ОТЗЫВА #####
@router.message(StateFilter(FSMCommands.fill_feedback), F.text)
async def take_feedback(message: Message, state: FSMContext):
    await message.answer(text=LEXICON['correct_feedback'][data.user_language(message.from_user.id)],
                         reply_markup=main_menu_button(data.user_language(message.from_user.id)))
    data.new_feedback(str(message.text))
    await state.clear()
    await sleep(5)
    await message.delete()
