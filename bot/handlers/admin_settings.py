from aiogram import Router, F, Bot
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from bot.config import Config
from bot.db import set_setting, get_all_settings

router = Router()

class AdminSet(StatesGroup):
    waiting_value = State()
    waiting_image = State()

def is_admin(cfg: Config, user_id: int) -> bool:
    return user_id in set(cfg.admin_ids)

@router.message(Command("cancel"))
async def cancel(m: Message, state: FSMContext, cfg: Config):
    if not is_admin(cfg, m.from_user.id):
        return
    await state.clear()
    await m.answer("Dibatalkan ✅")

@router.message(Command("showsettings"))
async def show_settings(m: Message, cfg: Config):
    if not is_admin(cfg, m.from_user.id):
        return
    s = await get_all_settings()
    lines = ["⚙️ Settings aktif (DB overrides):"]
    if not s:
        lines.append("(kosong) — pakai .env semua")
    else:
        for k in sorted(s.keys()):
            lines.append(f"- {k} = {s[k]}")
    await m.answer("\n".join(lines))

@router.message(Command("setforce"))
async def set_force(m: Message, state: FSMContext, cfg: Config):
    if not is_admin(cfg, m.from_user.id):
        return
    await state.update_data(key="force_channel_id")
    await state.set_state(AdminSet.waiting_value)
    await m.answer("Kirim FORCE_CHANNEL_ID baru (format -100...):")

@router.message(Command("setrate"))
async def set_rate(m: Message, state: FSMContext, cfg: Config):
    if not is_admin(cfg, m.from_user.id):
        return
    await state.update_data(key="rate_channel_id")
    await state.set_state(AdminSet.waiting_value)
    await m.answer("Kirim RATE_CHANNEL_ID baru (format -100...):")

@router.message(Command("setstorage"))
async def set_storage(m: Message, state: FSMContext, cfg: Config):
    if not is_admin(cfg, m.from_user.id):
        return
    await state.update_data(key="storage_channel_id")
    await state.set_state(AdminSet.waiting_value)
    await m.answer("Kirim STORAGE_CHANNEL_ID baru (format -100...):")

@router.message(Command("setimg"))
async def set_img(m: Message, state: FSMContext, cfg: Config):
    if not is_admin(cfg, m.from_user.id):
        return

    parts = (m.text or "").split(maxsplit=1)
    arg = parts[1].strip().lower() if len(parts) > 1 else ""

    if arg not in ("start", "poster"):
        await m.answer("Format: /setimg start  atau  /setimg poster")
        return

    key = "start_photo" if arg == "start" else "poster_photo"
    await state.update_data(key=key)
    await state.set_state(AdminSet.waiting_image)
    await m.answer(f"Kirim foto untuk {arg} sekarang (sebagai photo).")

@router.message(Command("setmsg"))
async def set_msg(m: Message, state: FSMContext, cfg: Config):
    if not is_admin(cfg, m.from_user.id):
        return

    parts = (m.text or "").split(maxsplit=1)
    arg = parts[1].strip().lower() if len(parts) > 1 else ""

    mapping = {
        "not_join": "not_join_text",
        "joined": "joined_text",
        "ask_caption": "ask_caption_text",
        "rate_prompt": "rate_prompt_text",
        "post_title": "post_title",
        "mention": "rate_channel_mention",
    }
    if arg not in mapping:
        await m.answer(
            "Format:\n"
            "/setmsg not_join\n"
            "/setmsg joined\n"
            "/setmsg ask_caption\n"
            "/setmsg rate_prompt\n"
            "/setmsg post_title\n"
            "/setmsg mention\n\n"
            "Lalu kirim teksnya. (Gunakan enter biasa; atau tulis \\n kalau dari .env style)"
        )
        return

    await state.update_data(key=mapping[arg])
    await state.set_state(AdminSet.waiting_value)
    await m.answer(f"Kirim teks baru untuk {arg} sekarang.\nKetik /cancel untuk batal.")

@router.message(AdminSet.waiting_value, F.text)
async def receive_value(m: Message, state: FSMContext, cfg: Config):
    if not is_admin(cfg, m.from_user.id):
        return

    data = await state.get_data()
    key = data.get("key")
    if not key:
        await state.clear()
        await m.answer("Key tidak ditemukan. /cancel")
        return

    val = (m.text or "").strip()

    # basic validation for channel ids
    if key in ("force_channel_id", "rate_channel_id", "storage_channel_id"):
        try:
            int(val)
        except ValueError:
            await m.answer("Harus angka (contoh: -1001234567890). Coba kirim lagi.")
            return

    await set_setting(key, val)
    await state.clear()
    await m.answer(f"✅ Tersimpan: {key} = {val}")

@router.message(AdminSet.waiting_image, F.photo)
async def receive_image(m: Message, state: FSMContext, cfg: Config):
    if not is_admin(cfg, m.from_user.id):
        return

    data = await state.get_data()
    key = data.get("key")
    if key not in ("start_photo", "poster_photo"):
        await state.clear()
        await m.answer("Key image tidak valid. /cancel")
        return

    file_id = m.photo[-1].file_id
    await set_setting(key, file_id)
    await state.clear()
    await m.answer(f"✅ Image tersimpan: {key} (file_id)")
