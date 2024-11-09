from databases import Database


DATABASE_URL = "sqlite+aiosqlite:///./fastnote.db"
database = Database(DATABASE_URL)


async def init_database(db: Database) -> None:
    await db.execute("""
CREATE TABLE IF NOT EXISTS notes(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    title TEXT DEFAULT "Untitled",
    content TEXT NOT NULL
);""")
