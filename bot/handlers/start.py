from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from bot.config import Config
from bot.keyboards import kb_force_join, kb_main
from bot.utils import is_member, get_invite_link

router = Router()

async def send_start_screen(bot: Bot, cfg: Config, m: Message, state: FSMContext):
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

@router.message(CommandStart(deep_link=False))
async def start_cmd(m: Message, bot: Bot, state: FSMContext, cfg: Config):
    await send_start_screen(bot, cfg, m, state)

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
