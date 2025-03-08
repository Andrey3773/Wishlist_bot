#######################################################################################################################
############################# ФАЙЛ С ХЭНДЛЕРАМИ, ОТВЕЧАЮЩИМИ ЗА ВЗАИМОДЕЙСТВИЕ С АДМИНАМИ #############################
#######################################################################################################################


from aiogram import Router, Bot, F
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from config_data.config import Config, load_config
from filters.filters import IsAdmin, IsUserInData
from lexicon.lexicon import LEXICON_ADMIN, KEYBOARD_LEXICON, LEXICON
from database.interact_database import user_language
from handlers.fsm import FSMCommands, FSMAdmin
from database import interact_database as data
from asyncio import sleep
from keyboards import keyboards as kb, admin_keyboards as admin_kb


##### ИНИЦИАЛИЗАЦИЯ РОУТЕРА #####
router = Router()


##### ИНИЦИАЛИЗАЦИЯ КОНФИГУРАТОРА, ЧТОБЫ ДОСТАТЬ ИЗ НЕГО БОТА #####
config: Config = load_config('.env')
bot = Bot(token=config.bot.token)


##### ИНИЦИАЛИЗАЦИЯ КОНФИГУРАТОРА, ЧТОБЫ ДОСТАТЬ ИЗ НЕГО СПИСОК АДМИНОВ #####
admins_config: Config = load_config('.env')



################################################## РАБОТА С КОМАНДАМИ ##################################################

##### ХЭНДЛЕР, ОТВЕЧАЮЩИЙ ЗА ОБРАБОТКУ ПОВТОРНОГО ВЫЗОВА КОМАНДЫ START ОТ АДМИНОВ ######
@router.message(Command(commands='start'), IsUserInData(), IsAdmin(admins_config.bot.admin_ids))
async def admin_start_again(message: Message, db_access):
    sent_message = await message.answer(LEXICON_ADMIN['/start_again'][user_language(db_access, message)])
    await sleep(5)
    await message.delete()
    await bot.delete_message(chat_id=message.chat.id,
                             message_id=sent_message.message_id)


##### ХЭНДЛЕР, ОТВЕЧАЮЩИЙ ЗА КОМАНДУ START В ШТАТНОМ РЕЖИМЕ ДЛЯ АДМИНОВ #####
@router.message(Command(commands='start'), IsAdmin(admins_config.bot.admin_ids))
async def start_command(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_ADMIN['/start']['ru'],
                         parse_mode='HTML')
    await state.set_state(FSMCommands.fill_name)


##### ХЭНДЛЕР, ОТЕЧАЮЩИЙ ЗА ВЫВОД ФИДБЭКА ПОЛЬЗОАТЕЛЕЙ ДЛЯ АДМИНОВ #####
@router.message(Command(commands='feedback'), IsAdmin(admins_config.bot.admin_ids))
async def give_feedback(message: Message, db_access):
    await message.answer(text=data.all_feedback(db_access, message),
                         reply_markup=admin_kb.admin_feedback_keyboard(db_access, message),
                         parse_mode='HTML')


##### ХЭНДЛЕР, ОТВЕЧАЮЩИЙ ЗА ВЫЗОВ КОМАНДЫ HELP, А ТАКЖЕ ГЛАВНОГО МЕНЮ #####
@router.message(Command(commands='help'), IsAdmin(admins_config.bot.admin_ids))
async def command_help(message: Message, state: FSMContext, db_access):
    await state.clear()
    data.all_accessible_gifts(db_access, message)
    await message.answer(text=LEXICON_ADMIN['/help'][data.user_language(db_access, message)])
    await message.answer(text=LEXICON['main_menu'][data.user_language(db_access, message)],
                         reply_markup=kb.main_menu_keyboard(db_access, message),
                         parse_mode='HTML')



################################################### РАБОТА С ОТЗЫВАМИ ##################################################

##### ХЭНДЛЕР, ОТВЕЧАЮЩИЙ ЗА НАЖАТИЕ КНОПКИ СДЕЛАТЬ БАГОМ #####
@router.callback_query(F.data == KEYBOARD_LEXICON['admin']['make_issue']['callback'])
async def make_issue_button(callback: CallbackQuery, state: FSMContext, db_access):
    await state.set_state(FSMAdmin.fill_new_issue)
    await callback.message.edit_text(text=data.all_feedback(db_access, callback) +
                                          LEXICON_ADMIN['fill_make_issue'][data.user_language(db_access, callback)],
                                     reply_markup=admin_kb.admin_feedback_list_keyboard(db_access, callback),
                                     parse_mode='HTML')


##### ХЭНДЛЕР, ОТВЕЧАЮЩИЙ ЗА НАЗНАЧЕНИЕ ОТЗЫВА БАГОМ #####
@router.callback_query(F.data.isdigit(), StateFilter(FSMAdmin.fill_new_issue))
async def new_issue_handler(callback: CallbackQuery, state: FSMContext, db_access):
    await state.clear()
    data.new_issue(db_access, callback)
    await callback.message.edit_text(text=LEXICON_ADMIN['make_issue'][user_language(db_access, callback)],
                                     reply_markup=kb.back_button(db_access, callback),
                                     parse_mode='HTML')


##### ХЭНДЛЕР, ОТВЕЧАЮЩИЙ ЗА НАЖАТИЕ КНОПКИ УДАЛИТЬ ОТЗЫВ #####
@router.callback_query(F.data == KEYBOARD_LEXICON['admin']['kill_feedback']['callback'])
async def kill_feedback_button(callback: CallbackQuery, state: FSMContext, db_access):
    await state.set_state(FSMAdmin.fill_kill_feedback)
    await callback.message.edit_text(text=data.all_feedback(db_access, callback) +
                                          LEXICON_ADMIN['fill_kill_feedback'][data.user_language(db_access, callback)],
                                     reply_markup=admin_kb.admin_feedback_list_keyboard(db_access, callback),
                                     parse_mode='HTML')


##### ХЭНДЛЕР, ОТВЕЧАЮЩИЙ ЗА УДАЛЕНИЕ ОТЗЫВА #####
@router.callback_query(F.data.isdigit(), StateFilter(FSMAdmin.fill_kill_feedback))
async def kill_feedback_handler(callback: CallbackQuery, state: FSMContext, db_access):
    await state.clear()
    data.kill_feedback(db_access, callback)
    await callback.message.edit_text(text=LEXICON_ADMIN['kill_feedback'][user_language(db_access, callback)],
                                     reply_markup=kb.back_button(db_access, callback),
                                     parse_mode='HTML')



#################################################### РАБОТА С БАГАМИ ###################################################

##### ХЭНДЛЕР, ОТВЕЧАЮЩИЙ ЗА НАЖАТИЕ КНОПКИ ПОСМОТРЕТЬ ПРОБЛЕМЫ #####
@router.callback_query(F.data == KEYBOARD_LEXICON['admin']['see_issues']['callback'])
async def see_issue_button(callback: CallbackQuery, db_access):
    await callback.message.edit_text(text=LEXICON_ADMIN['issues'][data.user_language(db_access, callback)] +
                                          data.all_issues(db_access, callback),
                                     reply_markup=admin_kb.admin_solve_issue(db_access, callback),
                                     parse_mode='HTML')


##### ХЭНДЛЕР, ОТВЕЧАЮЩИЙ ЗА НАЖАТИЕ КНОПКИ РЕШИТЬ ПРОБЛЕМУ #####
@router.callback_query(F.data == KEYBOARD_LEXICON['admin_in_issues']['solve_issue']['callback'])
async def solve_issue_button(callback: CallbackQuery, state: FSMContext, db_access):
    await state.set_state(FSMAdmin.fill_solved_issue)
    await callback.message.edit_text(text=data.all_issues(db_access, callback) +
                                     LEXICON_ADMIN['choose_issue'][data.user_language(db_access, callback)],
                                     reply_markup=admin_kb.admin_issues_keyboard(db_access, callback),
                                     parse_mode='HTML')


##### ХЭНДЛЕР, ОТВЕЧАЮЩИЙ ЗА РЕШЕНИЕ ПРОБЛЕМЫ #####
@router.callback_query(F.data.isdigit(), StateFilter(FSMAdmin.fill_solved_issue))
async def solve_issue_handler(callback: CallbackQuery, state: FSMContext, db_access):
    await state.clear()
    data.solve_issue(db_access, callback)
    await callback.message.edit_text(text=LEXICON_ADMIN['solve_issue'][data.user_language(db_access, callback)],
                                     reply_markup=kb.back_button(db_access, callback),
                                     parse_mode='HTML')


##### ХЭНДЛЕР, ОТВЕЧАЮЩИЙ ЗА НАЖАТИЕ КНОПКИ ОТКРЫТЬ ПРОБЛЕМУ #####
@router.callback_query(F.data == KEYBOARD_LEXICON['admin_in_issues']['not_solve_issue']['callback'])
async def solve_issue_button(callback: CallbackQuery, state: FSMContext, db_access):
    await state.set_state(FSMAdmin.fill_unsolved_issue)
    await callback.message.edit_text(text=data.all_issues(db_access, callback) +
                                     LEXICON_ADMIN['choose_issue'][data.user_language(db_access, callback)],
                                     reply_markup=admin_kb.admin_issues_keyboard(db_access, callback),
                                     parse_mode='HTML')


##### ХЭНДЛЕР, ОТВЕЧАЮЩИЙ ЗА ОТКРЫТИЕ ПРОБЛЕМЫ #####
@router.callback_query(F.data.isdigit(), StateFilter(FSMAdmin.fill_unsolved_issue))
async def not_solve_issue_handler(callback: CallbackQuery, state: FSMContext, db_access):
    await state.clear()
    data.not_solve_issue(db_access, callback)
    await callback.message.edit_text(text=LEXICON_ADMIN['make_issue'][user_language(db_access, callback)],
                                     reply_markup=kb.back_button(db_access, callback),
                                     parse_mode='HTML')


##### ХЭНДЛЕР, ОТВЕЧАЮЩИЙ ЗА НАЖАТИЕ КНОПКИ УДАЛИТЬ ПРОБЛЕМУ #####
@router.callback_query(F.data == KEYBOARD_LEXICON['admin_in_issues']['kill_issue']['callback'])
async def solve_issue_button(callback: CallbackQuery, state: FSMContext, db_access):
    await state.set_state(FSMAdmin.fill_killed_issue)
    await callback.message.edit_text(text=data.all_issues(db_access, callback) +
                                     LEXICON_ADMIN['choose_issue'][data.user_language(db_access, callback)],
                                     reply_markup=admin_kb.admin_issues_keyboard(db_access, callback),
                                     parse_mode='HTML')


##### ХЭНДЛЕР, ОТВЕЧАЮЩИЙ ЗА УДАЛЕНИЕ ПРОБЛЕМЫ #####
@router.callback_query(F.data.isdigit(), StateFilter(FSMAdmin.fill_killed_issue))
async def kill_issue_handler(callback: CallbackQuery, state: FSMContext, db_access):
    await state.clear()
    data.kill_issue(db_access, callback)
    await callback.message.edit_text(text=LEXICON_ADMIN['kill_issue'][user_language(db_access, callback)],
                                     reply_markup=kb.back_button(db_access, callback),
                                     parse_mode='HTML')



################################################### СЛУЖЕБНЫЕ КНОПКИ ###################################################

##### ХЭНДЛЕР, ОТВЕЧАЮЩИЙ ЗА НАЖАТИЕ КНОПКИ НАЗАД #####
@router.callback_query(F.data == KEYBOARD_LEXICON['admin_lower']['back']['callback'])
async def back_button(callback: CallbackQuery, state: FSMContext, db_access):
    await state.clear()
    await callback.message.edit_text(text=data.all_feedback(db_access, callback),
                                     reply_markup=admin_kb.admin_feedback_keyboard(db_access, callback),
                                     parse_mode='HTML')
