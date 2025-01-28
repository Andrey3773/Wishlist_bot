#######################################################################################################################
###################################### ФАЙЛ СО ВСЕМИ ПОЛЬЗОВАТЕЛЬСКИМИ ФИЛЬТРАМИ ######################################
#######################################################################################################################


from aiogram.filters import BaseFilter
from aiogram.types import Message
from database import interact_database as data
from emoji import demojize



##### ФИЛЬТР, ПРОВЕРЯЮЩИЙ ПОЛЬЗОАТЕЛЯ НА АДМИНКУ #####
class IsAdmin(BaseFilter):
    def __init__(self, admins):
        self.admins = admins

    async def __call__(self, message: Message):
        return message.from_user.id in self.admins


##### ФИЛЬТР, ЧТОБЫ ЛОВИТЬ УЖЕ ЗАРЕГИСТРИРОВАННЫХ ПОЛЬЗОВАТЕЛЕЙ #####
class IsUserInData(BaseFilter):
    async def __call__(self, message: Message):
        return data.user_in_data(message)


##### ФИЛЬТР, ПРОЕРЯЮЩИЙ КОРРЕКТНОСТЬ ИМЕНИ ПОЛЬЗОВАТЕЛЯ #####
class IsNameCorrect(BaseFilter):
    async def __call__(self, message: Message):
        flag = True
        text = message.text
        if text is None:
            return False
        for i in text:
            if not (i.isalpha() or (demojize(i).count(':') == 2) or i == ' '):
                flag = False
        if text.count(' ') > 1:
            flag = False
        return flag


##### ФИЛЬТР, ПРОВЕРЯЮЩИЙ КОРРЕКТНОСТЬ УДАЛЯЕМОЙ ИДЕИ ДЛЯ ПОДАРКА #####
class IsDeletedIdeaCorrect(BaseFilter):
    async def __call__(self, message: Message):
        if message.text is not None:
            return message.text in data.all_my_gifts(message)
        else:
            return False
