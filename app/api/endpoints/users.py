from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Annotated

from app.database import get_db
from app.services.user_service import UserService
from app.schemas.user import UserCreate, UserUpdate

router = APIRouter()

@router.get("/", 
    status_code=status.HTTP_200_OK,
    summary="List All Users",
    description="Retrieve a list of all user entries stored in the system."
)
async def list_users(db: Annotated[Session, Depends(get_db)]):
    users = UserService.list_users(db)
    return {"users": users}

@router.get("/{user_id}", 
    status_code=status.HTTP_200_OK,
    summary="Get User by ID",
    description="Retrieve the details of a specific user by its ID."
)
async def read_user(user_id: int, db: Annotated[Session, Depends(get_db)]):
    user = UserService.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return {"user": user}

@router.put("/{user_id}", 
    status_code=status.HTTP_200_OK,
    summary="Update an Existing User",
    description="Update the details of an existing user entry by its ID."
)
async def update_user(user_id: int, user: UserUpdate, db: Annotated[Session, Depends(get_db)]):
    user = UserService.update_user(db, user_id, user)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    return {"message": f"User with ID {user_id} updated", "user": user}

@router.post("/", 
    status_code=status.HTTP_201_CREATED,
    summary="Create a New User",
    description="Add a new user entry to the system."
)
async def create_user(user: UserCreate, db: Annotated[Session, Depends(get_db)]):
    user = UserService.create_user(db, user)
    return {"message": "User created", "user": user}

@router.delete("/{user_id}", 
    status_code=status.HTTP_200_OK,
    summary="Delete User by ID",
    description="Delete a specific user entry by its ID."
)
async def delete_user(user_id: int, db: Annotated[Session, Depends(get_db)]):
    success = UserService.delete_user(db, user_id)
    if success:
        return {"message": f"User with ID {user_id} deleted"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")