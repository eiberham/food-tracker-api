from fastapi import APIRouter, Depends, status, UploadFile, HTTPException
from app.services.DocsService import DocsService
from app.database import get_db
from typing import Annotated
from sqlalchemy.orm import Session

router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED )
async def load_document(file: UploadFile, db: Annotated[Session, Depends(get_db)]):
    try: 
        response = DocsService.process(db, file)
        return response
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))