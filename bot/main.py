import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from bot.config import load_config, Config
from bot.db import init_db
from bot.handlers import get_routers

async def main():
    cfg: Config = load_config()
    await init_db()

    bot = Bot(cfg.bot_token)
    dp = Dispatcher(storage=MemoryStorage())

    
    @dp.update.outer_middleware()
    async def cfg_middleware(handler, event, data):
        data["cfg"] = cfg
        return await handler(event, data)

    for r in get_routers():
        dp.include_router(r)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
