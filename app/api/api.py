from fastapi import APIRouter, Depends
from app.api.endpoints import foods, users, login, meals, symptoms, chat
from app.api.dependencies.auth import verify_token

router = APIRouter()
router.include_router(login.router, prefix="/login", tags=["login"])
router.include_router(foods.router, prefix="/foods", tags=["foods"], dependencies=[Depends(verify_token)])
router.include_router(users.router, prefix="/users", tags=["users"], dependencies=[Depends(verify_token)])
router.include_router(meals.router, prefix="/meals", tags=["meals"], dependencies=[Depends(verify_token)])
router.include_router(symptoms.router, prefix="/symptoms", tags=["symptoms"], dependencies=[Depends(verify_token)])
router.include_router(chat.router, prefix="/chat", tags=["chat"], dependencies=[Depends(verify_token)])