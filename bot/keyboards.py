from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def kb_force_join(join_url: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Join Channel", url=join_url)],
        [InlineKeyboardButton(text="🔄 Saya Sudah Join", callback_data="check_join")]
    ])

def kb_main(donate_url: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💖 Donate", url=donate_url)],
        [
            InlineKeyboardButton(text="👧 Cewe", callback_data="gender:cewe"),
            InlineKeyboardButton(text="👦 Cowo", callback_data="gender:cowo"),
        ]
    ])

def kb_admin_approval(sub_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Approve", callback_data=f"admin:approve:{sub_id}"),
            InlineKeyboardButton(text="❌ Reject", callback_data=f"admin:reject:{sub_id}"),
        ]
    ])

def deep_link(bot_username: str, sub_id: int) -> str:
    return f"https://t.me/{bot_username}?start=pap_{sub_id}"

def kb_view_post(bot_username: str, sub_id: int, donate_url: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="👀 Lihat PAP", url=deep_link(bot_username, sub_id))],
        [InlineKeyboardButton(text="💖 Donate", url=donate_url)]
    ])
