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

    welcome_text: str
    ask_caption_text: str
    post_template: str

def _parse_admin_ids(raw: str) -> list[int]:
    raw = (raw or "").strip()
    if not raw:
        return []
    return [int(x.strip()) for x in raw.split(",") if x.strip().isdigit()]

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
        welcome_text=os.getenv("WELCOME_TEXT", "Welcome!"),
        ask_caption_text=os.getenv("ASK_CAPTION_TEXT", "Kirim caption kamu."),
        post_template=os.getenv("POST_TEMPLATE", "Rate PAP\n\n{user_caption}\n\n#{gender}"),
    )
