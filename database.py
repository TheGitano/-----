import aiosqlite

DB_NAME = "movies.db"

async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT UNIQUE,
            genre TEXT,
            message_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        await db.commit()

async def add_movie(title, genre, message_id):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "INSERT OR IGNORE INTO movies (title, genre, message_id) VALUES (?, ?, ?)",
            (title, genre, message_id)
        )
        await db.commit()

async def get_movies_by_genre(genre):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute(
            "SELECT title, message_id FROM movies WHERE genre=? ORDER BY title",
            (genre,)
        )
        return await cursor.fetchall()

async def get_all_genres():
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("SELECT DISTINCT genre FROM movies ORDER BY genre")
        return [row[0] for row in await cursor.fetchall()]
