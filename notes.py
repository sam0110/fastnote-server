from datetime import UTC, datetime
from typing import List, Optional, Text
from databases import Database
from pydantic import BaseModel


class ClientNote(BaseModel):
    title: Text
    content: Text


class Note(BaseModel):
    id: int
    created_at: str
    updated_at: str
    title: Text
    content: Text


async def get_notes(db: Database) -> List[Note]:
    notes: List[Note] = []

    rows = await db.fetch_all("SELECT * FROM notes ORDER BY created_at DESC")
    for row in rows:
        notes.append(Note(**dict(row)))

    return notes


async def get_note(db: Database, id: int) -> Optional[Note]:
    row = await db.fetch_one("SELECT * FROM notes WHERE id=:id", {"id": id})
    if row == None:
        return None

    return Note(**dict(row))


async def create_note(db: Database, client_note: ClientNote) -> Optional[Note]:
    id = await db.execute("""
INSERT INTO notes (created_at, updated_at, title, content)
VALUES (:created_at, :updated_at, :title, :content)
""",
        {
            "created_at": datetime.now(UTC),
            "updated_at": datetime.now(UTC),
            "title": client_note.title,
            "content": client_note.content,
        },
    )

    return await get_note(db, id)


async def update_note(db: Database, id: int, client_note: ClientNote) -> Optional[Note]:
    await db.execute("""
UPDATE notes SET updated_at=:updated_at, title=:title, content=:content
WHERE id=:id
""",
        {
            "id": id,
            "updated_at": datetime.now(UTC),
            "title": client_note.title,
            "content": client_note.content,
        }
    )

    return await get_note(db, id)


async def delete_note(db: Database, id: int) -> None:
    await db.execute(
        "DELETE FROM notes WHERE id=:id",
        { "id": id },
    )
