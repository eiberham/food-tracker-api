from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.auth import AuthRequest, AuthResponse
from app.services.auth_service import AuthService
from app.database import get_db

router = APIRouter()

@router.post("/")
async def login(credentials: AuthRequest, db: Session = Depends(get_db)) -> AuthResponse:
    """
    19/07/2021
    12/08/2021 Offer
    30/08/2021 Start
    Simulate a login endpoint.
    Take username and password and generate a token (not implemented).
    """
    token = AuthService.login(db, credentials.username, credentials.password)
    response = AuthResponse(access_token=token)
    return response