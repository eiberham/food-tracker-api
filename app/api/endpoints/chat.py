from fastapi import APIRouter, status, Depends
from app.api.dependencies.auth import verify_token
from app.schemas.ChatMsg import ChatMsg
from app.services.ChatService import ChatService
from app.database import get_db

router = APIRouter()

@router.post("/", status_code=status.HTTP_200_OK)
async def chat(request: ChatMsg, user=Depends(verify_token), db=Depends(get_db)):
    return ChatService.chat(db, user.id, request.message)