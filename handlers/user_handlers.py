#######################################################################################################################
################### ФАЙЛ С ХЭНДЛЕРАМИ, ОТВЕЧАЮЩИМИ ЗА ШТАТНУЮ РАБОТУ БОТА С ОБЫЧНЫМИ ПОЛЬЗОВАТЕЛЯМИ ###################
#######################################################################################################################

from aiogram import Router, Bot, F
from aiogram.filters import StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from lexicon.lexicon import LEXICON, KEYBOARD_LEXICON
from database import interact_database as data
from handlers.fsm import FSMCommands, FSMMenu, FSMMyGroup
from config_data.config import Config, load_config
from asyncio import sleep
from keyboards import keyboards as kb
from filters.filters import IsPasswordCorrect


##### ИНИЦИАЛИЗАЦИЯ РОУТЕРА #####
router = Router()


##### ИНИЦИАЛИЗАЦИЯ КОНФИГУРАТОРА, ЧТОБЫ ДОСТАТЬ ИЗ НЕГО БОТА #####
config: Config = load_config('.env')
bot = Bot(token=config.bot.token)


############################################ ОБРАБОТКА КНОПОК ГЛАВНОГО МЕНЮ ############################################

##### ХЭНДЛЕР, ОТЕЧАЮЩИЙ ЗА НАЖАТИЕ КНОПКИ MY LIST #####
@router.callback_query(F.data == KEYBOARD_LEXICON['main_menu']['my_list']['callback'])
async def my_list_button(callback: CallbackQuery, db_access):
    await callback.message.edit_text(text=data.all_my_own_gifts(db_access, callback),
                                     reply_markup=kb.my_list_keyboard(db_access, callback),
                                     parse_mode='HTML')


##### ХЭНДЛЕР, ОТВЕЧАЮЩИЙ ЗА НАЖАТИЕ КНОПКИ MY GROUPS #####
@router.callback_query(F.data == KEYBOARD_LEXICON['main_menu']['my_groups']['callback'])
async def my_groups_button(callback: CallbackQuery, state: FSMContext, db_access):
    data.all_my_groups(db_access, callback)
    await state.set_state(FSMMyGroup.fill_group)
    await callback.message.edit_text(text=data.all_my_groups(db_access, callback) +
                                          LEXICON['choose_group'][data.user_language(db_access, callback)],
                                     reply_markup=kb.groups_keyboard(db_access, callback),
                                     parse_mode='HTML')


##### ХЭНДЛЕР, ОТВЕЧАЮЩИЙ ЗА НАЖАТИЕ КНОПКИ NEW GROUP #####
@router.callback_query(F.data == KEYBOARD_LEXICON['main_menu']['new_group']['callback'])
async def new_group_button(callback: CallbackQuery, state: FSMContext, db_access):
    await state.set_state(FSMMenu.fill_new_group)
    await callback.message.edit_text(text=LEXICON['fill_group_name'][data.user_language(db_access, callback)],
                                     reply_markup=kb.main_menu_button(db_access, callback),
                                     parse_mode='HTML')


##### ХЭНДЛЕР, ОТВЕЧАЮЩИЙ ЗА НАЖАТИЕ КНОПКИ IN GROUP #####
@router.callback_query(F.data == KEYBOARD_LEXICON['main_menu']['in_group']['callback'])
async def in_group_button(callback: CallbackQuery, state: FSMContext, db_access):
    await state.set_state(FSMMenu.fill_password)
    await callback.message.edit_text(text=LEXICON['fill_password'][data.user_language(db_access, callback)],
                                     reply_markup=kb.main_menu_button(db_access, callback),
                                     parse_mode='HTML')


##### ХЭНДЛЕР, ОТВЕЧАЮЩИЙ ЗА НАЖАТИЕ КНОПКИ FEEDBACK #####
@router.callback_query(F.data == KEYBOARD_LEXICON['main_menu']['feedback']['callback'])
async def feedback_button(callback: CallbackQuery, state: FSMContext, db_access):
    await callback.message.edit_text(text=LEXICON['fill_feedback'][data.user_language(db_access, callback)],
                                     reply_markup=kb.main_menu_button(db_access, callback),
                                     parse_mode='HTML')
    await state.set_state(FSMCommands.fill_feedback)



########################################### ОБРАБОТКА КНОПОК МЕНЮ IN MY LIST ###########################################

##### ХЭНДЛЕР, ОТВЕЧАЮЩИЙ ЗА НАЖАТИЕ КНОПКИ NEW GIFT #####
@router.callback_query(F.data == KEYBOARD_LEXICON['in_my_list']['new_gift']['callback'])
async def new_gift_button(callback: CallbackQuery, state: FSMContext, db_access):
    await state.set_state(FSMMenu.fill_new_idea)
    await callback.message.edit_text(text=LEXICON['fill_new_gift'][data.user_language(db_access, callback)],
                                     reply_markup=kb.main_menu_button(db_access, callback),
                                     parse_mode='HTML')


##### ХЭНДЛЕР, ОТВЕЧАЮЩИЙ ЗА ПРИНЯТИЕ НОВОЙ ИДЕИ ДЛЯ ПОДАРКА #####
@router.message(StateFilter(FSMMenu.fill_new_idea), F.text)
async def take_new_gift_idea(message: Message, db_access):
    if not(data.is_user_has_gift(db_access, message)):
        gift_id = data.create_new_gift(db_access, message)
        await message.answer(text=LEXICON['correct_new_gift_idea'][data.user_language(db_access, message)],
                             reply_markup=kb.groups_for_new_gift_keyboard(db_access, message, gift_id),
                             parse_mode='HTML')
        await message.delete()
    else:
        text = LEXICON['user_already_has_gift'][data.user_language(db_access, message)]
        await message.answer(text=text[0] + str(message.text) + text[1],
                             reply_markup=kb.ok_button(db_access, message),
                             parse_mode='HTML')
        await message.delete()


##### ХЭНДЛЕР, ОТВЕЧАЮЩИЙ ЗА ВЫБОР ГРУППЫ ДЛЯ НОВОГО ПОДАРКА #####
@router.callback_query(F.data.replace('_', '').isdigit(), StateFilter(FSMMenu.fill_new_idea))
async def take_group_for_new_gift(callback: CallbackQuery, db_access):
    data.add_new_gift_in_group(db_access, callback)
    if callback.message.text == LEXICON['one_more_group'][data.user_language(db_access, callback)]:

        await callback.message.edit_reply_markup(
            reply_markup=kb.groups_for_new_gift_keyboard(
                db_access,
                callback,
                int(callback.data[callback.data.rfind('_') + 1:]),
                is_button_no=True
            ),
            parse_mode='HTML'
        )
    else:
        await callback.message.edit_text(
            text=LEXICON['one_more_group'][data.user_language(db_access, callback)],
            reply_markup=kb.groups_for_new_gift_keyboard(
                db_access,
                callback,
                int(callback.data[callback.data.rfind('_') + 1:]),
                is_button_no=True
            ),
            parse_mode='HTML'
        )


##### ХЭНДЛЕР, ОТВЕЧАЮЩИЙ ЗА НАЖАТИЕ КНОПКИ НЕТ НА ВОПРОС ДОБАВИТЬ ЛИ ЕГО ЕЩЕ В ОДНУ ГРУППУ #####
@router.callback_query(F.data == KEYBOARD_LEXICON['no_button']['no']['callback'], StateFilter(FSMMenu.fill_new_idea))
async def no_button(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.clear()


##### ХЭНДЛЕР, ОТВЕЧАЮЩИЙ ЗА НАЖАТИЕ КНОПКИ DELETE GIFT #####
@router.callback_query(F.data == KEYBOARD_LEXICON['in_my_list']['delete_gift']['callback'])
async def delete_gift_button(callback: CallbackQuery, state: FSMContext, db_access):
    await state.set_state(FSMMenu.fill_group_for_delete_idea)
    await callback.message.edit_text(text=data.all_my_own_gifts(db_access, callback) +
                                      '\n\n' +
                                          LEXICON['fill_group_for_delete_idea'][data.user_language(db_access, callback)],
                                     reply_markup=kb.groups_keyboard(db_access, callback, not_all=False),
                                     parse_mode='HTML')


##### ХЭНДЛЕР, ОТВЕЧАЮЩИЙ ЗА ВЫБОР ГРУППЫ, ИЗ КОТОРОЙ НАДО УДАЛИТЬ ПОДАРОК #####
@router.callback_query(F.data.replace('_', '').isdigit(), StateFilter(FSMMenu.fill_group_for_delete_idea))
async def group_for_delete_gift_button(callback: CallbackQuery, state: FSMContext, db_access):
    await state.set_state(FSMMenu.fill_deleted_idea)
    await callback.message.edit_text(text=LEXICON['fill_delete_idea'][data.user_language(db_access, callback)],
                                     reply_markup=kb.gifts_keyboard(db_access, callback),
                                     parse_mode='HTML')


##### ХЭНДЛЕР, ОТВЕЧАЮЩИЙ ЗА ВЫБОР ПОДАРКА, КОТОРЫЙ НАДО УДАЛИТЬ #####
@router.callback_query(F.data.replace('_', '').isdigit(), StateFilter(FSMMenu.fill_deleted_idea))
async def group_for_delete_gift_button(callback: CallbackQuery, state: FSMContext, db_access):
    await state.clear()
    await callback.message.edit_text(text=LEXICON['correct_deleted_gift'][data.user_language(db_access, callback)],
                                     reply_markup=kb.main_menu_button(db_access, callback),
                                     parse_mode='HTML')
    data.delete_gift(db_access, callback)



########################################## ОБРАБОТКА КНОПОК МЕНЮ IN MY GROUPS ##########################################

##### ХЭНДЛЕР, ОТВЕЧАЮЩИЙ ЗА НАЖАТИЕ КНОПКИ С НАЗВАНИЕМ ГРУППЫ #####
@router.callback_query(F.data.isdigit(), StateFilter(FSMMyGroup.fill_group))
async def group_button(callback: CallbackQuery, state: FSMContext, db_access):
    await state.set_state(FSMMyGroup.fill_user)
    await callback.message.edit_text(text=data.all_users_in_group(db_access, callback) +
                                     LEXICON['choose_user'][data.user_language(db_access, callback)],
                                     reply_markup=kb.users_keyboard(db_access, callback),
                                     parse_mode='HTML')


##### ХЭНДЛЕР, ОТВЕЧАЮЩИЙ ЗА КНОПКУ ПАРОЛЬ #####
@router.callback_query(F.data[-len(KEYBOARD_LEXICON['group_password']['get_password']['callback']):] ==
                       KEYBOARD_LEXICON['group_password']['get_password']['callback'])
async def get_password_button(callback: CallbackQuery, db_access):
    await callback.message.edit_text(text=data.get_password(db_access, callback),
                                     reply_markup=kb.main_menu_button(db_access, callback),
                                     parse_mode='HTML')


##### ХЭНДЛЕР, ОТВЕЧАЮЩИЙ ЗА КНОПКУ УДАЛИТЬ ГРУППУ #####
@router.callback_query(F.data[-len(KEYBOARD_LEXICON['kill_group']['kill_group']['callback']):] ==
                       KEYBOARD_LEXICON['kill_group']['kill_group']['callback'])
async def kill_group_button(callback: CallbackQuery, db_access):
    await callback.message.edit_text(text=LEXICON['approve_delete_group'][data.user_language(db_access, callback)],
                                     reply_markup=kb.approve_delete_group(db_access, callback),
                                     parse_mode='HTML')


##### ХЭНДЛЕР, ОТВЕЧАЮЩИЙ ЗА КНОПКУ ПОДТВЕРЖДЕНИЯ УДАЛЕНИЯ ГРУППЫ #####
@router.callback_query(F.data[-len(KEYBOARD_LEXICON['kill_group']['approve_kill_group']['callback']):] ==
                       KEYBOARD_LEXICON['kill_group']['approve_kill_group']['callback'])
async def kill_group_button(callback: CallbackQuery, db_access):
    data.kill_group(db_access, callback)
    await callback.message.edit_text(text=LEXICON['kill_group'][data.user_language(db_access, callback)],
                                     reply_markup=kb.main_menu_button(db_access, callback),
                                     parse_mode='HTML')


##### ХЭНДЛЕР, ОТВЕЧАЮЩИЙ ЗА НАЖАТИЕ КНОПКИ С ИМЕНЕНЕМ ПОЛЬЗОВАТЕЛЯ #####
@router.callback_query(F.data.replace('_', '').isdigit(), StateFilter(FSMMyGroup.fill_user))
async def user_button(callback: CallbackQuery, state: FSMContext, db_access):
    await state.set_state(FSMMyGroup.fill_gift)
    if callback.data[callback.data.find('_') + 1:] == str(callback.from_user.id):
        await callback.message.edit_text(text=data.all_gifts_by_user_in_group(db_access, callback) +
                                              LEXICON['choose_gift'][data.user_language(db_access, callback)],
                                         reply_markup=kb.gifts_keyboard(db_access, callback),
                                         parse_mode='HTML')
    else:
        await callback.message.edit_text(text=data.all_gifts_by_user_in_group(db_access, callback, status=True) +
                                         LEXICON['choose_gift'][data.user_language(db_access, callback)],
                                         reply_markup=kb.gifts_keyboard(db_access, callback),
                                         parse_mode='HTML')


##### ХЭНДЛЕР, ОТВЕЧАЮЩИЙ ЗА НАЖАТИЕ КНОПКИ С НАЗВАНИЕМ ПОДАРКА #####
@router.callback_query(F.data.replace('_', '').isdigit(), StateFilter(FSMMyGroup.fill_gift))
async def gift_button(callback: CallbackQuery, state: FSMContext, db_access):
    await state.set_state(FSMMyGroup.what_do_with_gift)
    await callback.message.edit_text(text=data.what_to_do_with_gift(db_access, callback),
                                     reply_markup=kb.under_gift_keyboard(db_access, callback),
                                     parse_mode='HTML')


##### ХЭНДЛЕР, ОТВЕЧАЮЩИЙ ЗА НАЖАТИЕ КНОПКИ ЗАНЯТЬ ПОДАРОК #####
@router.callback_query(F.data[-len(KEYBOARD_LEXICON['under_gift']['take_gift']['callback']):] ==
                       KEYBOARD_LEXICON['under_gift']['take_gift']['callback'])
async def take_gift(callback: CallbackQuery, db_access):
    await callback.message.edit_text(text=LEXICON['gift_is_taken'][data.user_language(db_access, callback)],
                                     reply_markup=kb.main_menu_button(db_access, callback),
                                     parse_mode='HTML')
    data.take_gift(db_access, callback)


##### ХЭНДЛЕР, ОТВЕЧАЮЩИЙ ЗА НАЖАТИЕ КНОПКИ ОСВОБОДИТЬ ПОДАРОК #####
@router.callback_query(F.data[-len(KEYBOARD_LEXICON['under_gift']['free_up_gift']['callback']):] ==
                       KEYBOARD_LEXICON['under_gift']['free_up_gift']['callback'])
async def free_up_gift(callback: CallbackQuery, db_access):
    await callback.message.edit_text(text=LEXICON['gift_is_free'][data.user_language(db_access, callback)],
                                     reply_markup=kb.main_menu_button(db_access, callback),
                                     parse_mode='HTML')
    data.free_up_gift(db_access, callback)



############################################ ОБРАБОТКА ВВОДИМОЙ ИНФОРМАЦИИ #############################################

##### ХЭНДЛЕР, ОТВЕЧАЮЩИЙ ЗА ПРИНЯТИЕ ОТЗЫВА #####
@router.message(StateFilter(FSMCommands.fill_feedback), F.text)
async def take_feedback(message: Message, state: FSMContext, db_access):
    sent_message = await message.answer(text=LEXICON['correct_feedback'][data.user_language(db_access, message)],
                                        parse_mode='HTML')
    data.new_feedback(db_access, message)
    await state.clear()
    await sleep(10)
    await message.delete()
    await bot.delete_message(chat_id=message.chat.id, message_id=sent_message.message_id)


##### ХЭНДЛЕР, ОТВЕЧАЮЩИЙ ЗА ПРИНЯТИЕ НАЗВАНИЯ НОВОЙ ГРУППЫ #####
@router.message(StateFilter(FSMMenu.fill_new_group), F.text)
async def take_new_group(message: Message, state: FSMContext, db_access):
    if not(data.is_user_has_group(db_access, message)):
        text = LEXICON['correct_new_group'][data.user_language(db_access, message)]
        data.new_group(db_access, message)
        await state.clear()
    else:
        text = LEXICON['user_already_has_group'][data.user_language(db_access, message)]
    sent_message = await message.answer(text=text,
                                        parse_mode='HTML')
    await sleep(5)
    await message.delete()
    await bot.delete_message(chat_id=message.chat.id, message_id=sent_message.message_id)


##### ХЭНДЛЕР, ОТВЕЧАЮЩИЙ ЗА ПРИНЯТИЕ ПАРОЛЯ ДЛЯ ГРУППЫ #####
@router.message(StateFilter(FSMMenu.fill_password), IsPasswordCorrect())
async def take_password_for_group(message: Message, state: FSMContext, db_access):
    if data.is_user_in_group(db_access, message):
        text = LEXICON['user_already_in_group'][data.user_language(db_access, message)]
    elif data.is_user_has_same_group(db_access, message):
        text = LEXICON['user_already_has_same_group'][data.user_language(db_access, message)]
    else:
        text = LEXICON['correct_password'][data.user_language(db_access, message)]
        data.add_user_in_group(db_access, message)
        await state.clear()
    sent_message = await message.answer(text=text,
                                        parse_mode='HTML')
    await sleep(5)
    await message.delete()
    await bot.delete_message(chat_id=message.chat.id, message_id=sent_message.message_id)



################################################### СЛУЖЕБНЫЕ КНОПКИ ###################################################

##### ХЭНДЛЕР, ОТВЕЧАЮЩИЙ ЗА ОБРАБОТКУ НАЖАТИЯ КНОПКИ MAIN MENU #####
@router.callback_query(F.data == KEYBOARD_LEXICON['main_menu']['main_menu_button']['callback'])
async def main_menu_button(callback: CallbackQuery, state: FSMContext, db_access):
    await state.clear()
    await callback.message.edit_text(text=LEXICON['main_menu'][data.user_language(db_access, callback)],
                                     reply_markup=kb.main_menu_keyboard(db_access, callback),
                                     parse_mode='HTML')


##### ХЭНДЛЕР, ОТВЕЧАЮЩИЙ ЗА НАЖАТИЕ КНОПКИ ОК #####
@router.callback_query(F.data == KEYBOARD_LEXICON['ok_button']['ok']['callback'])
async def ok_button(callback: CallbackQuery):
    await callback.message.delete()
