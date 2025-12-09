from fastapi import APIRouter, status, Depends
from fastapi.responses import StreamingResponse
from app.api.dependencies.auth import verify_token
from app.schemas.chat_msg import ChatMsg
from app.services.chat_service import ChatService
from app.database import get_db

router = APIRouter()

@router.post("/", status_code=status.HTTP_200_OK)
async def chat(request: ChatMsg, user=Depends(verify_token), db=Depends(get_db)):
    stream = ChatService.chat(db, user.id, request.message)
    return StreamingResponse(stream, media_type="text/event-stream")