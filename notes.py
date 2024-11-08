from typing import List, Text
from databases import Database
from pydantic import BaseModel


class ClientNote(BaseModel):
    content: Text


class Note(BaseModel):
    id: int
    created_at: str
    content: Text


async def get_notes(db: Database) -> List[Note]:
    notes: List[Note] = []

    rows = await db.fetch_all("SELECT * FROM notes ORDER BY created_at DESC")
    for row in rows:
        notes.append(Note(**dict(row)))

    return notes


async def get_note(db: Database, id: int) -> Note | None:
    row = await db.fetch_one("SELECT * FROM notes WHERE id=:id", {"id": id})
    if row == None:
        return None

    return Note(**dict(row))


async def create_note(db: Database, client_note: ClientNote) -> Note | None:
    id = await db.execute(
        "INSERT INTO notes (content) VALUES (:content) RETURNING id",
        { "content": client_note.content },
    )

    return await get_note(db, id)


async def delete_note(db: Database, id: int) -> None:
    await db.execute(
        "DELETE FROM notes WHERE id=:id",
        { "id": id },
    )
