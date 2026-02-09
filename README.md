# RatePAP Bot (aiogram v3)

## Features
- Force subscribe on /start (photo + welcome + join button)
- Donate button + gender selection
- User submits media + optional caption (or asked after)
- Media stored in STORAGE_CHANNEL
- Admin approval (Approve/Reject)
- Approved submissions are posted to RATE_CHANNEL with poster + custom caption + deep-link button
- Deep-link view enforces force-sub before showing media

## Setup
1) Copy .env.example to .env and fill values
2) Install deps:
   pip install -r requirements.txt
3) Run:
   python -m bot.main
