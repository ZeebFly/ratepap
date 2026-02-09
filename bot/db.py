import aiosqlite

DB_PATH = "bot.db"

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            gender TEXT
        )
        """)
        await db.execute("""
        CREATE TABLE IF NOT EXISTS submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            gender TEXT NOT NULL,
            user_caption TEXT,
            storage_chat_id INTEGER NOT NULL,
            storage_message_id INTEGER NOT NULL,
            status TEXT NOT NULL,          -- pending/approved/rejected
            created_at INTEGER NOT NULL
        )
        """)
        # ✅ settings table
        await db.execute("""
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT
        )
        """)
        await db.commit()

# ---------- USERS ----------
async def set_gender(user_id: int, gender: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
        INSERT INTO users(user_id, gender) VALUES(?, ?)
        ON CONFLICT(user_id) DO UPDATE SET gender=excluded.gender
        """, (user_id, gender))
        await db.commit()

async def get_gender(user_id: int) -> str | None:
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT gender FROM users WHERE user_id=?", (user_id,)) as cur:
            row = await cur.fetchone()
            return row[0] if row else None

# ---------- SUBMISSIONS ----------
async def create_submission(
    user_id: int,
    gender: str,
    user_caption: str | None,
    storage_chat_id: int,
    storage_message_id: int,
    created_at: int
) -> int:
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute("""
        INSERT INTO submissions(user_id, gender, user_caption, storage_chat_id, storage_message_id, status, created_at)
        VALUES(?, ?, ?, ?, ?, 'pending', ?)
        """, (user_id, gender, user_caption, storage_chat_id, storage_message_id, created_at))
        await db.commit()
        return cur.lastrowid

async def set_submission_caption(sub_id: int, caption: str | None):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("UPDATE submissions SET user_caption=? WHERE id=?", (caption, sub_id))
        await db.commit()

async def get_submission(sub_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("""
        SELECT id, user_id, gender, user_caption, storage_chat_id, storage_message_id, status, created_at
        FROM submissions WHERE id=?
        """, (sub_id,)) as cur:
            return await cur.fetchone()

async def set_submission_status(sub_id: int, status: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("UPDATE submissions SET status=? WHERE id=?", (status, sub_id))
        await db.commit()

# ---------- SETTINGS ----------
async def set_setting(key: str, value: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
        INSERT INTO settings(key, value) VALUES(?, ?)
        ON CONFLICT(key) DO UPDATE SET value=excluded.value
        """, (key, value))
        await db.commit()

async def get_setting(key: str) -> str | None:
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT value FROM settings WHERE key=?", (key,)) as cur:
            row = await cur.fetchone()
            return row[0] if row else None

async def get_all_settings() -> dict[str, str]:
    async with aiosqlite.connect(DB_PATH) as db:
        out: dict[str, str] = {}
        async with db.execute("SELECT key, value FROM settings") as cur:
            async for k, v in cur:
                out[str(k)] = str(v)
        return out

