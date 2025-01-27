#######################################################################################################################
##################################################### ТОЧКА ВХОДА #####################################################
#######################################################################################################################


import asyncio
from aiogram import Bot, Dispatcher
from config_data.config import Config, load_config
from handlers import (mistakes_handlers as mistakes,
                      admin_handlers as admin,
                      user_handlers as user,
                      command_handlers as command)

##### ФУНКЦИЯ КОНФИГУРИРОВАНИЯ И ЗАПУСКА БОТА #####
async def main():

    # Загрузка конфигурации бота
    config: Config = load_config('.env')

    # Инициализация бота и диспетчера
    bot = Bot(token=config.bot.token)
    dp = Dispatcher()

    # Инициализация всех необходимых роутеров
    dp.include_router(admin.router)
    dp.include_router(command.router)
    dp.include_router(user.router)
    dp.include_router(mistakes.router)

    # Пропуск накопившихся апдейтов и запуск polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

asyncio.run(main())
