from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery

from bot.config import Config
from bot.db import get_submission, set_submission_status
from bot.keyboards import deep_link
from bot.caption_builder import build_rate_post_caption

router = Router()

def _is_admin(cfg: Config, user_id: int) -> bool:
    return user_id in set(cfg.admin_ids)

@router.callback_query(F.data.startswith("admin:"))
async def admin_action(c: CallbackQuery, bot: Bot, cfg: Config):
    if not _is_admin(cfg, c.from_user.id):
        await c.answer("Bukan admin.", show_alert=True)
        return

    parts = c.data.split(":")
    if len(parts) != 3:
        await c.answer("Format tidak valid.", show_alert=True)
        return

    action, sub_id_str = parts[1], parts[2]
    try:
        sub_id = int(sub_id_str)
    except ValueError:
        await c.answer("ID tidak valid.", show_alert=True)
        return

    row = await get_submission(sub_id)
    if not row:
        await c.answer("Submission tidak ditemukan.", show_alert=True)
        return

    _, user_id, gender, user_caption, storage_chat_id, storage_message_id, status, _ = row
    if status != "pending":
        await c.answer(f"Sudah diproses ({status}).", show_alert=True)
        return

    if action == "reject":
        await set_submission_status(sub_id, "rejected")
        await c.answer("Rejected ✅")
        try:
            await bot.send_message(user_id, "Maaf, PAP kamu ditolak admin ❌")
        except Exception:
            pass
        return

    if action == "approve":
        await set_submission_status(sub_id, "approved")
        await c.answer("Approved ✅")

        link = deep_link(cfg.bot_username, sub_id)
        post_text = build_rate_post_caption(cfg, gender=gender, user_caption=user_caption, link=link)

        # Kirim poster + caption (tanpa inline button supaya komentar muncul)
        if cfg.poster_photo:
            await bot.send_photo(
                chat_id=cfg.rate_channel_id,
                photo=cfg.poster_photo,
                caption=post_text
            )
        else:
            await bot.send_message(
                chat_id=cfg.rate_channel_id,
                text=post_text
            )

        try:
            await bot.send_message(user_id, "PAP kamu sudah di-approve ✅ dan diposting ke channel Rate.")
        except Exception:
            pass
        return

    await c.answer("Aksi tidak dikenal.", show_alert=True)
