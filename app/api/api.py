from fastapi import APIRouter, Depends
from fastapi_limiter.depends import RateLimiter
from app.api.endpoints import auth, foods, insights, meals, symptoms, chat, documents
from app.api.dependencies.auth import verify_supabase_token, verify_cron_secret

router = APIRouter()
router.include_router(auth.router, prefix="/login", tags=["login"], dependencies=[Depends(RateLimiter(times=5, seconds=60))])
router.include_router(foods.router, prefix="/foods", tags=["foods"], dependencies=[Depends(verify_supabase_token), Depends(RateLimiter(times=5, seconds=60))])
router.include_router(meals.router, prefix="/meals", tags=["meals"], dependencies=[Depends(verify_supabase_token), Depends(RateLimiter(times=5, seconds=60))])
router.include_router(symptoms.router, prefix="/symptoms", tags=["symptoms"], dependencies=[Depends(verify_supabase_token), Depends(RateLimiter(times=5, seconds=60))])
router.include_router(chat.router, prefix="/chat", tags=["chat"], dependencies=[Depends(verify_supabase_token), Depends(RateLimiter(times=5, seconds=60))])
router.include_router(documents.router, prefix="/documents", tags=["documents"], dependencies=[Depends(RateLimiter(times=5, seconds=60))])
router.include_router(insights.router, prefix="/insights", tags=["insights"], dependencies=[Depends(verify_cron_secret)])