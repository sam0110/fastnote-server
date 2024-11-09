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
);
"""
    )
    await db.execute("""
CREATE TABLE IF NOT EXISTS categories(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TEXT NOT NULL,
    name TEXT NOT NULL,
    color TEXT DEFAULT "#000000"
);
"""
    )
    await db.execute("""
CREATE TABLE IF NOT EXISTS notes_categories(
    note_id INTEGER NOT NULL,
    category_id INTEGER NOT NULL,
    FOREIGN KEY(note_id) REFERENCES notes(id),
    FOREIGN KEY(category_id) REFERENCES categories(id),
    PRIMARY KEY (note_id, category_id)
);
"""
    )
