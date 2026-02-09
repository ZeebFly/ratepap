from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.filters import CommandStart

from bot.config import Config
from bot.db import get_submission
from bot.utils import is_member, get_invite_link
from bot.keyboards import kb_force_join

router = Router()

@router.message(CommandStart(deep_link=True))
async def deeplink(m: Message, bot: Bot, cfg: Config):
    # /start pap_<id>
    args = m.text.split(maxsplit=1)
    payload = args[1] if len(args) > 1 else ""

    if not payload.startswith("pap_"):
        return  # /start biasa ditangani handler start.py

    ok = await is_member(bot, cfg.force_channel_id, m.from_user.id)
    if not ok:
        join_url = await get_invite_link(bot, cfg.force_channel_id)
        await m.answer(
            "Untuk lihat PAP, kamu wajib join channel dulu ya 👇",
            reply_markup=kb_force_join(join_url)
        )
        return

    try:
        sub_id = int(payload.replace("pap_", "").strip())
    except ValueError:
        await m.answer("Link tidak valid.")
        return

    row = await get_submission(sub_id)
    if not row:
        await m.answer("Konten tidak ditemukan / sudah dihapus.")
        return

    _, _, _, _, storage_chat_id, storage_message_id, status, _ = row
    if status != "approved":
        await m.answer("Konten belum tersedia.")
        return

    await bot.copy_message(
        chat_id=m.chat.id,
        from_chat_id=storage_chat_id,
        message_id=storage_message_id
    )
