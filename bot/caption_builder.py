from bot.config import Config

def build_rate_post_caption(cfg: Config, gender: str, user_caption: str | None) -> str:
    """
    Output contoh:
    Rate PAP

    rate aku dong 😳

    Kasih rating di komentar!
    #cowo
    @RatePapChannel
    """
    lines: list[str] = []

    title = (cfg.post_title or "Rate PAP").strip()
    if title:
        lines.append(title)

    cap = (user_caption or "").strip()
    if cap:
        lines.append("")
        lines.append(cap)

    # prompt rating (selalu ada)
    prompt = (cfg.rate_prompt_text or "").strip()
    if prompt:
        lines.append("")
        lines.append(prompt)

    # footer hashtag + mention
    lines.append(f"#{gender}")

    mention = (cfg.rate_channel_mention or "").strip()
    if mention:
        lines.append(mention)

    return "\n".join(lines).strip()
