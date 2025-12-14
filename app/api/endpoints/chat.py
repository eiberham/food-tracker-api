from fastapi import APIRouter, status, Depends
from fastapi.responses import StreamingResponse
from supabase.client import Client
from typing import Annotated
from app.schemas.chat_msg import ChatMsg
from app.services.chat_service import ChatService
from app.database import get_db

router = APIRouter()

@router.post("/", 
    status_code=status.HTTP_200_OK,
    response_class=StreamingResponse,
    responses={
        200: {
            "description": "Stream of chat responses",
            "content": {
                "text/event-stream": {
                    "example": "data: {\"type\": \"agent\", \"content\": \"Hello! How can I help you today?\"}\n\ndata: {\"type\": \"tool_call\", \"tool\": \"get_meals_of_date\", \"input\": {\"date\": \"2024-12-10\"}}\n\n"
                }
            }
        }
    },
    summary="Chat with AI Agent (Streaming)",
    description="""
    Start a streaming chat conversation with the AI agent.
    
    The response will be a Server-Sent Events (SSE) stream with content-type `text/event-stream`.
    Each event contains JSON data with the agent's response chunks.
    
    **Testing in Swagger:**
    - Click "Try it out"
    - Enter your message
    - Click "Execute" 
    - The response will show as a download (due to streaming)
    
    **Testing with curl:**
    ```bash
    curl -X POST "http://localhost:8000/chat/" \\
      -H "Content-Type: application/json" \\
      -H "Accept: text/event-stream" \\
      -H "Authorization: Bearer YOUR_TOKEN" \\
      -d '{"message": "Hello!"}'
    ```
    """
)
async def chat(request: ChatMsg, db: Annotated[Client, Depends(get_db)]):
    stream = ChatService.chat(db, request.message)
    return StreamingResponse(stream, media_type="text/event-stream")