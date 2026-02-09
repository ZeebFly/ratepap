from bot.config import Config

def build_rate_post_caption(cfg: Config, gender: str, user_caption: str | None, link: str) -> str:
    """
    Format:
    #cewe
    Rate dong

    Link pap:
    https://t.me/...

    Donate Pap langsung ke bot  @ratepapchannel
    """
    lines: list[str] = []

    # 1) hashtag dulu
    lines.append(f"#{gender}")

    # 2) caption user (wajib ada di contohmu)
    cap = (user_caption or "").strip()
    if cap:
        lines.append(cap)
    else:
        # kalau user skip caption, pakai default (biar format tidak kosong)
        default_cap = (cfg.default_post_caption or "Rate dong").strip()
        lines.append(default_cap)

    lines.append("")  # spasi

    # 3) link label + link
    link_label = (cfg.link_label_text or "Link pap:").strip()
    lines.append(link_label)
    lines.append(link)

    lines.append("")  # spasi

    # 4) donate line
    donate_line = (cfg.donate_line_text or "").strip()
    if donate_line:
        lines.append(donate_line)

    return "\n".join(lines).strip()
