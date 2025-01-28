#######################################################################################################################
################################# ФАЙЛ С ХЭНДЛЕРАМИ, ОТВЕЧАЮЩИМИ ЗА ОБРАБОТКУ КОММАНД #################################
#######################################################################################################################


from aiogram import Router, Bot
from aiogram.filters import Command, StateFilter
from aiogram.types import Message
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext
from lexicon.lexicon import LEXICON_COMMAND, LEXICON
from database import interact_database as data
from handlers.fsm import FSMCommands
from filters.filters import IsUserInData, IsNameCorrect
from config_data.config import Config, load_config
from asyncio import sleep
from keyboards.keyboards import main_menu_keyboard


##### ИНИЦИАЛИЗАЦИЯ РОУТЕРА #####
router = Router()


##### ИНИЦИАЛИЗАЦИЯ КОНФИГУРАТОРА, ЧТОБЫ ДОСТАТЬ ИЗ НЕГО БОТА #####
config: Config = load_config('.env')
bot = Bot(token=config.bot.token)


##### ХЭНДЛЕР, ОТВЕЧАЮЩИЙ ЗА ПОТОРНЫЙ ВЫЗОВ КОМАНДЫ START #####
@router.message(Command(commands='start'), IsUserInData())
async def repeat_start_command(message: Message):
    sent_message = await message.answer(text=LEXICON_COMMAND['/start_again'][data.user_language(message)],
                                        parse_mode='HTML')

    await sleep(10)
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


##### ХЭНДЛЕР ОТЕЧАЮЩИЙ ЗА УСПЕШНУЮ РЕГИСТРАЦИЮ #####
@router.message(StateFilter(FSMCommands.fill_name), IsNameCorrect())
async def correct_registration(message: Message, state: FSMContext):
    data.new_user(message, message.text)
    await message.answer(LEXICON['correct_registration'][data.user_language(message)][0] +
                         data.give_name(message) +
                         LEXICON['correct_registration'][data.user_language(message)][1])
    await state.clear()
    await message.answer(text=LEXICON['help'][data.user_language(message)])
    await message.answer(text=LEXICON['main_menu'][data.user_language(message)],
                         reply_markup=main_menu_keyboard(data.user_language(message)))
