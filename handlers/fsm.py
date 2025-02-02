######################################################################################################################
#################################### ФАЙЛ В КОТОРОМ ХРАНЯТСЯ ВСЕ МАШИНЫ СОСТОЯНИЙ ####################################
######################################################################################################################


from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import State, StatesGroup


storage = MemoryStorage()

##### МАШИНА СОСТОЯНИЙ ДЛЯ РАЗЛИЧНЫХ КОМАНД #####
class FSMCommands(StatesGroup):
    fill_name = State()
    fill_feedback = State()


##### МАШИНА СОСТОЯНИЙ ПРИ ПЕРЕМЕЩЕНИИ ПО МЕНЮ #####
class FSMMenu(StatesGroup):
    fill_new_idea = State()
    fill_deleted_idea = State()
    fill_new_group = State()
    fill_password = State()


##### МАШИНА СОСТОЯНИЙ ДЛЯ АДМИНОВ #####
class FSMAdmin(StatesGroup):
    fill_kill_feedback = State()
    fill_new_issue = State()
    fill_solved_issue = State()
    fill_unsolved_issue = State()
    fill_killed_issue = State()


##### МАШИНА СОСТОЯНИЙ ДЛЯ НАХОЖДЕНИЯ В СПИСКЕ МОИХ ГРУПП #####
class FSMMyGroup(StatesGroup):
    fill_group = State()
    fill_user = State()
    fill_gift = State()
    what_do_with_gift = State()
    fill_new_gift = State()
