from typing import List
from fastapi import FastAPI, status
from contextlib import asynccontextmanager
from database import database, init_database
import notes


@asynccontextmanager
async def lifespan(_: FastAPI):
    await database.connect()
    await init_database(database)
    yield
    await database.disconnect()


app = FastAPI(lifespan=lifespan)


@app.get("/notes", response_model=List[notes.Note])
async def read_notes():
    note_list = await notes.get_notes(database)
    return note_list


@app.get("/note/{note_id}", response_model=notes.Note)
async def read_note(note_id: int):
    note = await notes.get_note(database, note_id)
    return note


@app.delete("/note/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_note(note_id: int):
    await notes.delete_note(database, note_id)


@app.post("/note", response_model=notes.Note)
async def post_note(client_note: notes.ClientNote):
    note = await notes.create_note(database, client_note)
    return note

