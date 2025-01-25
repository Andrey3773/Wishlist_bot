from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.types import Message
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.fsm.context import FSMContext
from lexicon.lexicon import LEXICON_COMMAND, LEXICON
from database import interact_database as db

# инициализация роутера
router = Router()

storage = MemoryStorage()

class FSM(StatesGroup):
    fill_name = State()

@router.message(Command(commands='start'), StateFilter(default_state))
async def start_command(message: Message, state: FSMContext):
    await message.answer(LEXICON_COMMAND['/start']['ru'])
    await state.set_state(FSM.fill_name)

@router.message(StateFilter(FSM.fill_name), F.text.isalpha())
async def correct_name(message: Message, state: FSMContext):
    await message.answer(LEXICON['correct_name']['ru'])
    db.new_user(message.from_user.id, message.text)
    await state.clear()

@router.message(StateFilter(FSM.fill_name))
async def incorrect_name(message: Message, state: FSMContext):
    await message.answer(LEXICON['incorrect_name']['ru'])
