from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest

async def is_member(bot: Bot, channel_id: int, user_id: int) -> bool:
    try:
        m = await bot.get_chat_member(channel_id, user_id)
        return m.status in ("creator", "administrator", "member", "restricted")
    except TelegramBadRequest:
        return False

async def get_invite_link(bot: Bot, channel_id: int) -> str:
    # untuk channel private; kalau public, kamu bisa hardcode sendiri
    try:
        link = await bot.create_chat_invite_link(channel_id, creates_join_request=False)
        return link.invite_link
    except Exception:
        return "https://t.me/your_force_channel"
