from dataclasses import replace
from bot.config import Config
from bot.db import get_all_settings

def _to_int(s: str) -> int:
    return int(str(s).strip())

def _t(s: str | None) -> str | None:
    if s is None:
        return None
    return s.replace("\\n", "\n")

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

    # images
    if "start_photo" in s:
        cfg = replace(cfg, start_photo=(s["start_photo"] or None))
    if "poster_photo" in s:
        cfg = replace(cfg, poster_photo=(s["poster_photo"] or None))

    # texts
    v = _t(s.get("not_join_text"))
    if v is not None:
        cfg = replace(cfg, not_join_text=v)

    v = _t(s.get("joined_text"))
    if v is not None:
        cfg = replace(cfg, joined_text=v)

    v = _t(s.get("ask_caption_text"))
    if v is not None:
        cfg = replace(cfg, ask_caption_text=v)

    # NEW post texts
    v = _t(s.get("default_post_caption"))
    if v is not None:
        cfg = replace(cfg, default_post_caption=v)

    v = _t(s.get("link_label_text"))
    if v is not None:
        cfg = replace(cfg, link_label_text=v)

    v = _t(s.get("donate_line_text"))
    if v is not None:
        cfg = replace(cfg, donate_line_text=v)

    return cfg
