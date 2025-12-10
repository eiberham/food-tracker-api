from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.schemas.auth import AuthRequest, AuthResponse
from app.services.auth_service import AuthService
from app.database import get_db

router = APIRouter()

@router.post("/",
    status_code=status.HTTP_200_OK,
    summary="User Login",
    description="Authenticate user and return an access token."
)
async def login(credentials: AuthRequest, db: Session = Depends(get_db)) -> AuthResponse:
    token = AuthService.login(db, credentials.username, credentials.password)
    response = AuthResponse(access_token=token)
    return response