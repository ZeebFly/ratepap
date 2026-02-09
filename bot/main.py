import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from bot.config import load_config, Config
from bot.db import init_db
from bot.handlers import get_routers
from bot.runtime_config import load_runtime_config

async def main():
    base_cfg: Config = load_config()
    await init_db()

    bot = Bot(base_cfg.bot_token)
    dp = Dispatcher(storage=MemoryStorage())

    # inject cfg (env + db overrides) untuk setiap update
    @dp.update.outer_middleware()
    async def cfg_middleware(handler, event, data):
        runtime_cfg = await load_runtime_config(base_cfg)
        data["cfg"] = runtime_cfg
        return await handler(event, data)

    for r in get_routers():
        dp.include_router(r)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
