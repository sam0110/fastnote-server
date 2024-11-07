from typing import List, Text
from databases import Database
from pydantic import BaseModel


class Note(BaseModel):
    id: int
    created_at: str
    content: Text


async def get_notes(db: Database) -> List[Note]:
    notes: List[Note] = []

    rows = await db.fetch_all("SELECT * FROM notes ORDER BY created_at DESC;")
    for row in rows:
        notes.append(Note(**dict(row)))

    return notes

async def get_note(db: Database, id: int) -> Note | None:
    row = await db.fetch_one("SELECT * FROM notes WHERE id=(:id)", {"id": id})
    if row == None:
        return None
    return Note(**dict(row))
