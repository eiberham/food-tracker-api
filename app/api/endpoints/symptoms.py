from fastapi import APIRouter, Depends, HTTPException, status
from app.services.symptom_service import SymptomService
from app.schemas.symptom import SymptomCreate, SymptomUpdate
from app.database import get_auth_db
from typing import Annotated
from supabase.client import Client

router = APIRouter()

@router.get("/", 
    status_code=status.HTTP_200_OK,
    summary="List All Symptoms",
    description="Retrieve a list of all symptom entries stored in the system."
)
async def list_symptoms(db: Annotated[Client, Depends(get_auth_db)]):
    symptoms = SymptomService.list_symptoms(db)
    return symptoms

@router.post("/", 
    status_code=status.HTTP_201_CREATED,
    summary="Create a New Symptom",
    description="Add a new symptom entry to the system."
)
async def create_symptom(symptom: SymptomCreate, db: Annotated[Client, Depends(get_auth_db)]):
    try:
        symptom = SymptomService.create_symptom(db, symptom)
        return {"message": "Symptom created", "symptom": symptom}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.put("/{symptom_id}", 
    status_code=status.HTTP_200_OK,
    summary="Update an Existing Symptom",
    description="Update the details of an existing symptom entry by its ID."
)
async def update_symptom(symptom_id: int, payload: SymptomUpdate, db: Annotated[Client, Depends(get_auth_db)]):
    symptom = SymptomService.update_symptom(db, symptom_id, payload)
    return {"message": f"Symptom with ID {symptom_id} updated", "symptom": symptom}

@router.get("/{symptom_id}", 
    status_code=status.HTTP_200_OK,
    summary="Get Symptom by ID",
    description="Retrieve the details of a specific symptom entry by its ID."
)
async def get_symptom(symptom_id: int, db: Annotated[Client, Depends(get_auth_db)]):
    symptom = SymptomService.get_symptom_by_id(db, symptom_id)
    if not symptom:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Symptom not found")
    return {"symptom": symptom}

@router.delete("/{symptom_id}", 
    status_code=status.HTTP_200_OK,
    summary="Delete Symptom by ID",
    description="Delete a specific symptom entry by its ID."
)
async def delete_symptom(symptom_id: int, db: Annotated[Client, Depends(get_auth_db)]):
    symptom = SymptomService.delete_symptom(db, symptom_id)
    if not symptom:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Symptom not found")
    return {"message": f"Symptom with ID {symptom_id} deleted"}