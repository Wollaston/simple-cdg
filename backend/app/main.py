from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager

from app.resources.bill import router as bill_router
from app.state import State


@asynccontextmanager
async def lifespan(_: FastAPI):
    "Context Manager that runs code on startup and shutdown"
    app.state.state = State.from_env()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(bill_router)


@app.get("/")
async def root():
    return {"res": "ok"}
