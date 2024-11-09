from typing import List
from fastapi import FastAPI, status
from contextlib import asynccontextmanager
import categories
from database import database, init_database
import notes


@asynccontextmanager
async def lifespan(_: FastAPI):
    await database.connect()
    await init_database(database)
    yield
    await database.disconnect()


app = FastAPI(lifespan=lifespan)


@app.post("/note", response_model=notes.Note)
async def post_note(client_note: notes.ClientNote):
    note = await notes.create_note(database, client_note)
    return note


@app.get("/notes", response_model=List[notes.Note])
async def get_notes():
    note_list = await notes.get_notes(database)
    return note_list


@app.get("/note/{note_id}", response_model=notes.Note)
async def get_note(note_id: int):
    note = await notes.get_note(database, note_id)
    return note


@app.patch("/note/{note_id}", response_model=notes.Note)
async def update_note(note_id: int, client_note: notes.ClientNote):
    return await notes.update_note(database, note_id, client_note)


@app.delete("/note/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_note(note_id: int):
    await notes.delete_note(database, note_id)


@app.post("/categories")
async def create_category(category: categories.ClientCategory):
    return await categories.create_category(database, category)


@app.get("/categories")
async def get_categories():
    return await categories.get_categories(database)


@app.get("/categories/{category_name}")
async def get_category_notes(category_name: str):
    return await categories.get_category_notes(database, category_name)


@app.post("/categories/{category_id}/add-note", status_code=status.HTTP_204_NO_CONTENT)
async def add_note_to_category(category_id: int, note: categories.ClientAddNote):
    return await categories.add_note_to_category(database, category_id, note.note_id)

