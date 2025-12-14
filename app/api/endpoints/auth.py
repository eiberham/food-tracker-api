from fastapi import APIRouter, status
from app.schemas.auth import AuthenticationRequest
from app.services.auth_service import AuthService

router = APIRouter()

@router.post("/",
    status_code=status.HTTP_200_OK,
    summary="User Login",
    description="Authenticate user and return an access token."
)
async def login(credentials: AuthenticationRequest):
    response = AuthService.login(credentials.email, credentials.password)
    return response