import asyncio
from aiogram import Bot, Dispatcher
from config_data.config import Config, load_config
from handlers import user_handlers
from aiogram.fsm.storage.memory import MemoryStorage

async def main():
    config: Config = load_config('.env')

    bot = Bot(token=config.bot.token)
    dp = Dispatcher()

    dp.include_router(user_handlers.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

asyncio.run(main())
