from fastapi import APIRouter, Depends, status, UploadFile, HTTPException
from app.services.docs_service import DocsService
from app.database import get_auth_db
from typing import Annotated
from supabase.client import Client

router = APIRouter()

@router.post("/", 
    status_code=status.HTTP_201_CREATED,
    summary="Upload and Process Document",
    description="""
        Upload a document file (PDF) to be processed and stored.
        Supported formats: PDF.
        The document will be parsed and relevant data extracted for later use.
    """
)
async def load_document(file: UploadFile, db: Annotated[Client, Depends(get_auth_db)]):
    try: 
        response = DocsService.process(db, file)
        return response
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))