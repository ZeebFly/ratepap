from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from bot.config import Config
from bot.keyboards import kb_force_join, kb_main
from bot.utils import is_member, get_invite_link
from bot.db import get_submission

router = Router()


async def send_not_joined(bot: Bot, cfg: Config, m: Message):
    join_url = await get_invite_link(bot, cfg.force_channel_id)

    if cfg.start_photo:
        await m.answer_photo(
            photo=cfg.start_photo,
            caption=cfg.not_join_text,
            reply_markup=kb_force_join(join_url)
        )
    else:
        await m.answer(cfg.not_join_text, reply_markup=kb_force_join(join_url))


async def send_joined_menu(cfg: Config, m: Message, state: FSMContext):
    await state.clear()
    if cfg.start_photo:
        await m.answer_photo(
            photo=cfg.start_photo,
            caption=cfg.joined_text,
            reply_markup=kb_main()
        )
    else:
        await m.answer(cfg.joined_text, reply_markup=kb_main())


async def handle_deeplink_view(bot: Bot, cfg: Config, m: Message, payload: str):
    ok = await is_member(bot, cfg.force_channel_id, m.from_user.id)
    if not ok:
        await send_not_joined(bot, cfg, m)
        return

    try:
        sub_id = int(payload.replace("pap_", "").strip())
    except ValueError:
        await m.answer("Link tidak valid.")
        return

    row = await get_submission(sub_id)
    if not row:
        await m.answer("Konten tidak ditemukan.")
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
    parts = (m.text or "").split(maxsplit=1)
    payload = parts[1] if len(parts) > 1 else ""

    if payload.startswith("pap_"):
        await handle_deeplink_view(bot, cfg, m, payload)
        return

    ok = await is_member(bot, cfg.force_channel_id, m.from_user.id)
    if not ok:
        await send_not_joined(bot, cfg, m)
        return

    await send_joined_menu(cfg, m, state)


@router.callback_query(F.data == "check_join")
async def check_join(c: CallbackQuery, bot: Bot, state: FSMContext, cfg: Config):
    ok = await is_member(bot, cfg.force_channel_id, c.from_user.id)
    if not ok:
        await c.answer("Kamu belum join.", show_alert=True)
        await send_not_joined(bot, cfg, c.message)
        return

    await c.answer("Sudah join ✅")
    await c.message.answer(cfg.joined_text, reply_markup=kb_main())
    await state.clear()
