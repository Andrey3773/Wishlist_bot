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
