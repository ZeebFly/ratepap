import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class Config:
    bot_token: str
    bot_username: str

    force_channel_id: int
    storage_channel_id: int
    rate_channel_id: int

    admin_ids: list[int]
    donate_url: str

    start_photo: str | None
    poster_photo: str | None

    not_join_text: str
    joined_text: str
    ask_caption_text: str

    rate_channel_mention: str | None
    post_title: str
    rate_prompt_text: str

def _parse_admin_ids(raw: str) -> list[int]:
    raw = (raw or "").strip()
    if not raw:
        return []
    out: list[int] = []
    for x in raw.split(","):
        x = x.strip()
        if x.isdigit():
            out.append(int(x))
    return out

def load_config() -> Config:
    return Config(
        bot_token=os.environ["BOT_TOKEN"],
        bot_username=os.environ["BOT_USERNAME"].lstrip("@"),

        force_channel_id=int(os.environ["FORCE_CHANNEL_ID"]),
        storage_channel_id=int(os.environ["STORAGE_CHANNEL_ID"]),
        rate_channel_id=int(os.environ["RATE_CHANNEL_ID"]),

        admin_ids=_parse_admin_ids(os.getenv("ADMIN_IDS", "")),
        donate_url=os.getenv("DONATE_URL", "https://example.com/donate"),

        start_photo=os.getenv("START_PHOTO"),
        poster_photo=os.getenv("POSTER_PHOTO"),

        not_join_text=os.getenv(
            "NOT_JOIN_TEXT",
            "Kamu belum join channel.\nJoin dulu supaya bisa donate & lanjut ✅"
        ),
        joined_text=os.getenv(
            "JOINED_TEXT",
            "Welcome!\nSilakan donate dulu atau pilih gender 👇"
        ),
        ask_caption_text=os.getenv("ASK_CAPTION_TEXT", "Kirim caption kamu."),

        rate_channel_mention=os.getenv("RATE_CHANNEL_MENTION"),
        post_title=os.getenv("POST_TITLE", "Rate PAP"),
        rate_prompt_text=os.getenv("RATE_PROMPT_TEXT", "Kasih rating di komentar!"),
    )
