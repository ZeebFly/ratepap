from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from bot.config import Config
from bot.keyboards import kb_force_join, kb_main
from bot.utils import is_member, get_invite_link
from bot.db import get_submission

router = Router()


async def _send_menu_start(bot: Bot, cfg: Config, m: Message, state: FSMContext):
    await state.clear()

    ok = await is_member(bot, cfg.force_channel_id, m.from_user.id)
    if not ok:
        join_url = await get_invite_link(bot, cfg.force_channel_id)
        caption = cfg.welcome_text + "\n\n➡️ Kamu harus join dulu untuk lanjut."
        if cfg.start_photo:
            await m.answer_photo(photo=cfg.start_photo, caption=caption, reply_markup=kb_force_join(join_url))
        else:
            await m.answer(caption, reply_markup=kb_force_join(join_url))
        return

    caption = cfg.welcome_text + "\n\nPilih gender dulu ya 👇"
    if cfg.start_photo:
        await m.answer_photo(photo=cfg.start_photo, caption=caption, reply_markup=kb_main(cfg.donate_url))
    else:
        await m.answer(caption, reply_markup=kb_main(cfg.donate_url))


async def _handle_deeplink_view(bot: Bot, cfg: Config, m: Message, payload: str):
    # payload format: pap_<id>
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


@router.message(CommandStart())
async def start_cmd(m: Message, bot: Bot, state: FSMContext, cfg: Config):
    # Tangkap payload manual biar gak pernah ketabrak router lain
    parts = (m.text or "").split(maxsplit=1)
    payload = parts[1] if len(parts) > 1 else ""

    if payload.startswith("pap_"):
        await _handle_deeplink_view(bot, cfg, m, payload)
        return

    await _send_menu_start(bot, cfg, m, state)


@router.callback_query(F.data == "check_join")
async def check_join(c: CallbackQuery, bot: Bot, state: FSMContext, cfg: Config):
    ok = await is_member(bot, cfg.force_channel_id, c.from_user.id)
    if not ok:
        await c.answer("Kamu belum join. Join dulu ya.", show_alert=True)
        return

    await c.answer("Sudah join ✅")
    try:
        await c.message.edit_reply_markup(reply_markup=kb_main(cfg.donate_url))
    except Exception:
        await c.message.answer("Pilih gender dulu ya 👇", reply_markup=kb_main(cfg.donate_url))
