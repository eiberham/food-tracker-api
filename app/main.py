from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.api.api import router
from app.database import engine, Base

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(title="Food Tracker API", version="v1", lifespan=lifespan)

app.include_router(router)

@app.get("/")
async def read_root():
    return "Welcome to the food tracker api."


