from dataclasses import replace
from bot.config import Config
from bot.db import get_all_settings

def _to_int(s: str) -> int:
    return int(str(s).strip())

async def load_runtime_config(base: Config) -> Config:
    s = await get_all_settings()

    cfg = base

    # channels
    if "force_channel_id" in s:
        cfg = replace(cfg, force_channel_id=_to_int(s["force_channel_id"]))
    if "rate_channel_id" in s:
        cfg = replace(cfg, rate_channel_id=_to_int(s["rate_channel_id"]))
    if "storage_channel_id" in s:
        cfg = replace(cfg, storage_channel_id=_to_int(s["storage_channel_id"]))

    # images (file_id)
    if "start_photo" in s:
        cfg = replace(cfg, start_photo=s["start_photo"] or None)
    if "poster_photo" in s:
        cfg = replace(cfg, poster_photo=s["poster_photo"] or None)

    # texts
    def get_text(k: str) -> str | None:
        v = s.get(k)
        if v is None:
            return None
        return v.replace("\\n", "\n")

    v = get_text("not_join_text")
    if v is not None:
        cfg = replace(cfg, not_join_text=v)

    v = get_text("joined_text")
    if v is not None:
        cfg = replace(cfg, joined_text=v)

    v = get_text("ask_caption_text")
    if v is not None:
        cfg = replace(cfg, ask_caption_text=v)

    v = get_text("rate_prompt_text")
    if v is not None:
        cfg = replace(cfg, rate_prompt_text=v)

    v = get_text("post_title")
    if v is not None:
        cfg = replace(cfg, post_title=v)

    v = get_text("rate_channel_mention")
    if v is not None:
        cfg = replace(cfg, rate_channel_mention=v)

    return cfg
