#######################################################################################################################
################### ФАЙЛ С ХЭНДЛЕРАМИ, ОТВЕЧАЮЩИМИ ЗА ШТАТНУЮ РАБОТУ БОТА С ОБЫЧНЫМИ ПОЛЬЗОВАТЕЛЯМИ ###################
#######################################################################################################################

from aiogram import Router, Bot, F
from aiogram.filters import StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from lexicon.lexicon import LEXICON, KEYBOARD_LEXICON
from database import interact_database as data
from handlers.fsm import FSMCommands, FSMMenu
from config_data.config import Config, load_config
from asyncio import sleep
from keyboards import keyboards as kb
from filters.filters import IsDeletedIdeaCorrect


##### ИНИЦИАЛИЗАЦИЯ РОУТЕРА #####
router = Router()


##### ИНИЦИАЛИЗАЦИЯ КОНФИГУРАТОРА, ЧТОБЫ ДОСТАТЬ ИЗ НЕГО БОТА #####
config: Config = load_config('.env')
bot = Bot(token=config.bot.token)


############################################ ОБРАБОТКА КНОПОК ГЛАВНОГО МЕНЮ ############################################

##### ХЭНДЛЕР, ОТВЕЧАЮЩИЙ ЗА ОБРАБОТКУ НАЖАТИЯ КНОПКИ MAIN MENU #####
@router.callback_query(F.data == KEYBOARD_LEXICON['main_menu_button']['callback'])
async def main_menu_button(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text(text=LEXICON['main_menu'][data.user_language(callback)],
                                     reply_markup=kb.main_menu_keyboard(data.user_language(callback)))


##### ХЭНДЛЕР, ОТЕЧАЮЩИЙ ЗА НАЖАТИЕ КНОПКИ MY LIST #####
@router.callback_query(F.data == KEYBOARD_LEXICON['main_menu']['callback']['my_list'])
async def my_list_button(callback: CallbackQuery):
    await callback.message.edit_text(text=data.all_my_gifts(callback),
                                     reply_markup=kb.my_list_keyboard(data.user_language(callback), callback),
                                     parse_mode='HTML')


##### ХЭНДЛЕР, ОТВЕЧАЮЩИЙ ЗА НАЖАТИЕ КНОПКИ NEW GROUP #####
@router.callback_query(F.data == KEYBOARD_LEXICON['main_menu']['callback']['new_group'])
async def new_group_button(callback: CallbackQuery, state: FSMContext):
    await state.set_state(FSMMenu.fill_new_group)
    await callback.message.edit_text(text=LEXICON['fill_group_name'][data.user_language(callback)],
                                     reply_markup=kb.main_menu_button(data.user_language(callback)))


##### ХЭНДЛЕР, ОТВЕЧАЮЩИЙ ЗА НАЖАТИЕ КНОПКИ IN GROUP #####
@router.callback_query(F.data == KEYBOARD_LEXICON['main_menu']['callback']['in_group'])
async def in_group_button(callback: CallbackQuery, state: FSMContext):
    await state.set_state(FSMMenu.fill_password)
    await callback.message.edit_text(text=LEXICON['fill_password'][data.user_language(callback)],
                                     reply_markup=kb.main_menu_button(data.user_language(callback)))


##### ХЭНДЛЕР, ОТВЕЧАЮЩИЙ ЗА НАЖАТИЕ КНОПКИ FEEDBACK #####
@router.callback_query(F.data == KEYBOARD_LEXICON['main_menu']['callback']['feedback'])
async def feedback_button(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON['fill_feedback'][data.user_language(callback)],
        reply_markup=kb.main_menu_button(data.user_language(callback)))
    await state.set_state(FSMCommands.fill_feedback)



######################################### ОБРАБОТКА КНОПОК МЕНЮ НИЖНИХ УРОВНЕЙ #########################################

##### ХЭНДЛЕР, ОТВЕЧАЮЩИЙ ЗА НАЖАТИЕ КНОПКИ NEW GIFT IN MY LIST #####
@router.callback_query(F.data == KEYBOARD_LEXICON['new_gift']['callback'])
async def new_gift_button(callback: CallbackQuery, state: FSMContext):
    await state.set_state(FSMMenu.fill_new_idea)
    await callback.message.edit_text(text=LEXICON['fill_new_gift'][data.user_language(callback)],
                                     reply_markup=kb.main_menu_button(data.user_language(callback)))


##### ХЭНДЛЕР, ОТВЕЧАЮЩИЙ ЗА НАЖАТИЕ КНОПКИ DELETE GIFT #####
@router.callback_query(F.data == KEYBOARD_LEXICON['delete_gift']['callback'])
async def delete_gift_button(callback: CallbackQuery, state: FSMContext):
    await state.set_state(FSMMenu.fill_deleted_idea)
    await callback.message.edit_text(text=data.all_my_gifts(callback) +
                                          '\n\n' +
                                          LEXICON['fill_deleted_gift'][data.user_language(callback)],
                                     reply_markup=kb.main_menu_button(data.user_language(callback)),
                                     parse_mode='HTML')



############################################ ОБРАБОТКА ВВОДИМОЙ ИНФОРМАЦИИ ############################################

##### ХЭНДЛЕР, ОТВЕЧАЮЩИЙ ЗА ПРИНЯТИЕ ОТЗЫВА #####
@router.message(StateFilter(FSMCommands.fill_feedback), F.text)
async def take_feedback(message: Message, state: FSMContext):
    sent_message = await message.answer(text=LEXICON['correct_feedback'][data.user_language(message)])
    data.new_feedback(message)
    await state.clear()
    await sleep(10)
    await message.delete()
    await bot.delete_message(chat_id=message.chat.id, message_id=sent_message.message_id)


##### ХЭНДЛЕР, ОТВЕЧАЮЩИЙ ЗА ПРИНЯТИЕ НОВОЙ ИДЕИ ДЛЯ ПОДАРКА #####
@router.message(StateFilter(FSMMenu.fill_new_idea), F.text)
async def take_new_gift_idea(message: Message, state: FSMContext):
    sent_message = await message.answer(text=LEXICON['correct_new_gift_idea'][data.user_language(message)])
    data.my_own_new_gift(message)
    await state.clear()
    await sleep(5)
    await message.delete()
    await bot.delete_message(chat_id=message.chat.id, message_id=sent_message.message_id)


##### ХЭНДЛЕР, ОТВЕЧАЮЩИЙ ЗА КОРРЕТНО ВВЕДЕННУЮ ИДЕЮ ДЛЯ УДАЛЕНИЯ #####
@router.message(StateFilter(FSMMenu.fill_deleted_idea), IsDeletedIdeaCorrect())
async def take_deleted_idea(message: Message, state: FSMContext):
    sent_message = await message.answer(text=LEXICON['correct_deleted_gift'][data.user_language(message)])
    data.delete_my_own_gift(message)
    await state.clear()
    await sleep(5)
    await message.delete()
    await bot.delete_message(chat_id=message.chat.id, message_id=sent_message.message_id)


##### ХЭНДЛЕР, ОТВЕЧАЮЩИЙ ЗА ПРИНЯТИЕ НАЗВАНИЯ НОВОЙ ГРУППЫ #####
@router.message(StateFilter(FSMMenu.fill_new_group), F.text)
async def take_new_gift_idea(message: Message, state: FSMContext):
    sent_message = await message.answer(text=LEXICON['correct_new_group'][data.user_language(message)])
    data.new_group(message)
    await state.clear()
    await sleep(5)
    await message.delete()
    await bot.delete_message(chat_id=message.chat.id, message_id=sent_message.message_id)


##### ХЭНДЛЕР, ОТВЕЧАЮЩИЙ ЗА ПРИНЯТИЕ ПАРОЛЯ ДЛЯ ГРУППЫ #####
@router.message(StateFilter(FSMMenu.fill_password), F.text)
async def take_password_for_group(message: Message, state: FSMContext):
    if not(data.is_user_in_group(message)):
        text = LEXICON['correct_password'][data.user_language(message)]
        data.add_user_in_group(message)
    else:
        text = LEXICON['user_already_in_group'][data.user_language(message)]
    sent_message = await message.answer(text=text)
    await state.clear()
    await sleep(5)
    await message.delete()
    await bot.delete_message(chat_id=message.chat.id, message_id=sent_message.message_id)
