import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


def _unescape_newlines(s: str | None) -> str:
    if s is None:
        return ""
    # Ubah literal "\n" menjadi newline sungguhan
    return s.replace("\\n", "\n")


@dataclass(frozen=True)
class Config:
    bot_token: str
    bot_username: str

    force_channel_id: int
    storage_channel_id: int
    rate_channel_id: int

    admin_ids: list[int]

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

        start_photo=os.getenv("START_PHOTO") or None,
        poster_photo=os.getenv("POSTER_PHOTO") or None,

        not_join_text=_unescape_newlines(os.getenv(
            "NOT_JOIN_TEXT",
            "Kamu belum join channel.\\nJoin dulu supaya bisa lanjut ✅"
        )),
        joined_text=_unescape_newlines(os.getenv(
            "JOINED_TEXT",
            "Welcome!\\nPilih gender dulu ya 👇"
        )),
        ask_caption_text=_unescape_newlines(os.getenv(
            "ASK_CAPTION_TEXT",
            'Silakan tulis caption PAP kamu.\\n\\nKetik /skip untuk tanpa caption.'
        )),

        rate_channel_mention=os.getenv("RATE_CHANNEL_MENTION") or None,
        post_title=os.getenv("POST_TITLE", "Rate PAP"),
        rate_prompt_text=os.getenv("RATE_PROMPT_TEXT", "Kasih rating di komentar!"),
    )
