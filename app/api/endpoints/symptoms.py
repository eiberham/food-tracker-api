from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def read_root():
    return "Symptoms endpoint."

@router.post("/")
async def create_symptom(symptom: dict):
    return {"message": "Symptom recorded", "symptom": symptom}

@router.put("/{symptom_id}")
async def update_symptom(symptom_id: int, symptom: dict):
    return {"message": f"Symptom with ID {symptom_id} updated", "symptom": symptom}

@router.get("/{symptom_id}")
async def read_symptom(symptom_id: int):
    return {"symptom_id": symptom_id, "description": f"Symptom{symptom_id} details"}

@router.delete("/{symptom_id}")
async def delete_symptom(symptom_id: int):
    return {"message": f"Symptom with ID {symptom_id} deleted"}