from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def read_root():
    return "login endpoint"

@router.post("/")
async def login(credentials: dict):
    """
    19/07/2021
    12/08/2021 Offer
    30/08/2021 Start
    Simulate a login endpoint.
    Take username and password and generate a token (not implemented).
    """
    return {"message": "Login successful", "credentials": credentials}