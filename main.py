from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import database, init_database


@asynccontextmanager
async def lifespan(_: FastAPI):
    await database.connect()
    await init_database(database)
    yield
    await database.disconnect()


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def read_root():
    return {"Hello": "World"}

