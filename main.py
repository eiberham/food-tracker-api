from fastapi import FastAPI
from app.api.api import router

app = FastAPI(title="Food Tracker API", version="1.0.0")

app.include_router(router)

@app.get("/")
async def read_root():
    return "Welcome to the food tracker api, designed to help me monitor my histamine intolerance."

