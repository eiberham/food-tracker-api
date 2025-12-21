from fastapi import FastAPI, Depends
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
from app.database import get_cache
from contextlib import asynccontextmanager
from app.api.api import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await FastAPILimiter.init(redis=get_cache())
    yield

app = FastAPI(title="Food Tracker", version="v1", lifespan=lifespan)

app.include_router(router)

@app.get("/", include_in_schema=False, dependencies=[Depends(RateLimiter(times=5, seconds=60))])
async def read_root():
    return "Welcome to the food tracker api."

@app.get("/health", include_in_schema=False, dependencies=[Depends(RateLimiter(times=5, seconds=60))])
async def health_check():
    return {"status": "ok"}


