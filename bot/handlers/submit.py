import time
from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from bot.config import Config
from bot.states import Flow
from bot.db import set_gender, get_gender, create_submission, set_submission_caption, get_submission
from bot.keyboards import kb_admin_approval
from bot.utils import is_member

router = Router()

@router.callback_query(F.data.startswith("gender:"))
async def pick_gender(c: CallbackQuery, bot: Bot, state: FSMContext, cfg: Config):
    ok = await is_member(bot, cfg.force_channel_id, c.from_user.id)
    if not ok:
        await c.answer("Join channel dulu ya.", show_alert=True)
        return

    gender = c.data.split(":", 1)[1]  # cewe/cowo
    await set_gender(c.from_user.id, gender)

    await state.set_state(Flow.waiting_media)
    await c.answer("Tersimpan ✅")
    await c.message.answer("Sekarang kirim media (foto/video/dokumen) ya 👇")

@router.message(Flow.waiting_media, F.photo | F.video | F.document)
async def receive_media(m: Message, bot: Bot, state: FSMContext, cfg: Config):
    ok = await is_member(bot, cfg.force_channel_id, m.from_user.id)
    if not ok:
        await m.answer("Kamu harus join channel dulu ya. Klik /start.")
        return

    gender = await get_gender(m.from_user.id)
    if not gender:
        await m.answer("Kamu belum pilih gender. Klik /start.")
        return

    copied = await m.copy_to(chat_id=cfg.storage_channel_id)

    user_caption = (m.caption or "").strip() or None
    sub_id = await create_submission(
        user_id=m.from_user.id,
        gender=gender,
        user_caption=user_caption,
        storage_chat_id=copied.chat.id,
        storage_message_id=copied.message_id,
        created_at=int(time.time())
    )

    await state.update_data(last_sub_id=sub_id)

    if not user_caption:
        await state.set_state(Flow.waiting_caption)
        await m.answer(cfg.ask_caption_text)
        return

    await m.answer("Media kamu sudah masuk antrean approval ✅")
    await notify_admins(bot, cfg, sub_id)

@router.message(Flow.waiting_caption, F.text)
async def receive_caption(m: Message, bot: Bot, state: FSMContext, cfg: Config):
    data = await state.get_data()
    sub_id = data.get("last_sub_id")
    if not sub_id:
        await m.answer("Session tidak ditemukan. Klik /start.")
        await state.clear()
        return

    text = (m.text or "").strip()
    if text.lower() == "/skip":
        text = ""

    await set_submission_caption(sub_id, text if text else None)

    await m.answer("Oke ✅ Media kamu sudah masuk antrean approval.")
    await state.clear()

    await notify_admins(bot, cfg, sub_id)

async def notify_admins(bot: Bot, cfg: Config, sub_id: int):
    row = await get_submission(sub_id)
    if not row:
        return

    _, user_id, gender, user_caption, storage_chat_id, storage_message_id, status, _ = row
    caption_line = user_caption if user_caption else "(tanpa caption)"

    for admin_id in cfg.admin_ids:
        try:
            await bot.copy_message(
                chat_id=admin_id,
                from_chat_id=storage_chat_id,
                message_id=storage_message_id
            )
            await bot.send_message(
                chat_id=admin_id,
                text=(
                    f"🛡️ Approval dibutuhkan\n"
                    f"Submission ID: {sub_id}\n"
                    f"User ID: {user_id}\n"
                    f"Gender: {gender}\n"
                    f"Caption: {caption_line}\n"
                    f"Status: {status}"
                ),
                reply_markup=kb_admin_approval(sub_id)
            )
        except Exception:
            # Admin belum pernah /start bot -> bisa gagal kirim
            pass
