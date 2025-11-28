from fastapi import APIRouter
from app.api.endpoints import foods

router = APIRouter()

router.include_router(foods.router, prefix="/foods", tags=["foods"])