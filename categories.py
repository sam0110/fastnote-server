from datetime import UTC, datetime
from typing import List, Optional
from databases import Database
from pydantic import BaseModel
from notes import Note


class ClientCategory(BaseModel):
    name: str
    color: str


class ClientAddNote(BaseModel):
    note_id: int


class Category(BaseModel):
    id: int
    name: str
    created_at: str


async def get_categories(db: Database) -> List[Category]:
    rows = await db.fetch_all("SELECT * FROM categories ORDER BY created_at DESC");

    categories: List[Category] = []
    for row in rows:
        categories.append(Category(**dict(row)))

    return categories


async def get_category(db: Database, id: int) -> Optional[Category]:
    row = await db.fetch_one("SELECT * FROM categories WHERE id=:id", { "id": id })
    if row == None:
        return None

    return Category(**dict(row))


async def get_category_notes(db: Database, category_name: str) -> List[Note]:
    rows = await db.fetch_all("""
SELECT *, categories.name FROM notes
LEFT JOIN notes_categories ON notes.id=notes_categories.note_id
LEFT JOIN categories ON notes_categories.category_id=categories.id
WHERE categories.name=:category_name
""",
        { "category_name": category_name }
    )

    notes: List[Note] = []
    for row in rows:
        notes.append(Note(**dict(row)))

    return notes


async def create_category(db: Database, client_category: ClientCategory) -> Optional[Category]:
    id = await db.execute("""
INSERT INTO categories (name, color, created_at)
VALUES (:name, :color, :created_at)
""",
        {
            "name": client_category.name,
            "color": client_category.color,
            "created_at": datetime.now(UTC)
        },
    )

    return await get_category(db, id)


async def add_note_to_category(
        db: Database,
        note_id: int,
        category_id: int
) -> None:
    await db.execute("""
INSERT INTO notes_categories (note_id, category_id)
VALUES (:note_id, :category_id)
""",
        {
            "note_id": note_id,
            "category_id": category_id,
        }
    )

