from fastapi import APIRouter, status
from app.schemas.ChatMsg import ChatMsg
from app.services.ChatService import ChatService

router = APIRouter()

@router.post("/", status_code=status.HTTP_200_OK)
async def chat(request: ChatMsg):
    return ChatService.chat(request.message)