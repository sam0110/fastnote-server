from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import database, init_database
from notes import get_notes


@asynccontextmanager
async def lifespan(_: FastAPI):
    await database.connect()
    await init_database(database)
    yield
    await database.disconnect()


app = FastAPI(lifespan=lifespan)


@app.get("/notes")
async def read_notes():
    notes = await get_notes(database)
    return notes


@app.get("/")
async def read_root():
    return {"Hello": "World"}
