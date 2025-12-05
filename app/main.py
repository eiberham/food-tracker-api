from fastapi import FastAPI, Depends
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
import redis.asyncio as redis
import app.config as config

from contextlib import asynccontextmanager
from app.api.api import router
from app.database import engine, Base

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    redis_client = redis.from_url(config.vars['redis_url'], encoding="utf-8", decode_responses=True)
    await FastAPILimiter.init(redis=redis_client)
    yield

app = FastAPI(title="Food Tracker", version="v1", lifespan=lifespan)

app.include_router(router)

@app.get("/", include_in_schema=False, dependencies=[Depends(RateLimiter(times=5, seconds=60))])
async def read_root():
    return "Welcome to the food tracker api."


