#######################################################################################################################
##################################################### ТОЧКА ВХОДА #####################################################
#######################################################################################################################


import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from config_data.config import Config, Database, load_config
from handlers import (mistakes_handlers as mistakes,
                      admin_handlers as admin,
                      user_handlers as user,
                      start_handlers as start,
                      private_handler as private)

##### ФУНКЦИЯ КОНФИГУРИРОВАНИЯ И ЗАПУСКА БОТА #####
async def main():

    # Загрузка конфигурации бота
    config: Config = load_config('.env')

    # Инициализация бота и диспетчера
    bot = Bot(
        token=config.bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()


    database: Database = config.db
    admin_ids = config.bot.admin_ids

    dp.workflow_data.update({'db_access': database, 'admins': admin_ids})


    # Этот роутер не влияет на функционал бота и добавлен из личных пожеланий
    dp.include_router(private.router)


    # Инициализация всех необходимых роутеров
    dp.include_router(admin.router)
    dp.include_router(start.router)
    dp.include_router(user.router)
    dp.include_router(mistakes.router)

    # Пропуск накопившихся апдейтов и запуск polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

asyncio.run(main())
