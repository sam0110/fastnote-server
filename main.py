from typing import List
from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import database, init_database
from notes import ClientNote, Note, create_note, get_note, get_notes


@asynccontextmanager
async def lifespan(_: FastAPI):
    await database.connect()
    await init_database(database)
    yield
    await database.disconnect()


app = FastAPI(lifespan=lifespan)


@app.get("/notes", response_model=List[Note])
async def read_notes():
    notes = await get_notes(database)
    return notes


@app.get("/note/{note_id}", response_model=Note)
async def read_note(note_id: int):
    note = await get_note(database, note_id)
    return note


@app.post("/note", response_model=Note)
async def post_note(client_note: ClientNote):
    note = await create_note(database, client_note)
    return note


@app.get("/")
async def read_root():
    return {"Hello": "World"}
