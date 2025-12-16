from app.schemas.symptom import SymptomCreate, SymptomUpdate
from app.services.meal_service import MealService
from datetime import date
from supabase.client import Client

class SymptomService:

    @classmethod
    def list_symptoms(cls, db: Client):
        symptoms = db.table("symptom").select("*").execute()
        return symptoms.data

    @classmethod
    def create_symptom(cls, db: Client, payload: SymptomCreate):
        if not MealService.get_meal_by_id(db, payload.meal_id):
            raise Exception("Meal does not exist")
        
        result = db.rpc("create_symptom_for_user", {
            "p_meal_id": payload.meal_id,
            "p_datetime": payload.datetime.isoformat() if payload.datetime else None,
            "p_symptom_type": payload.symptom_type,
            "p_severity": payload.severity,
            "p_notes": payload.notes
        }).execute()

        return result.data[0] if result.data else None
    
    @classmethod
    def update_symptom(cls, db: Client, symptom_id: int, payload: SymptomUpdate):
        symptom = cls.get_symptom_by_id(db, symptom_id)
        if not symptom:
            return None

        response = db.rpc("update_symptom_for_user", {
            "p_symptom_id": symptom_id,
            "p_datetime": payload.datetime.isoformat() if hasattr(payload, 'datetime') and payload.datetime else symptom['datetime'],
            "p_symptom_type": payload.symptom_type if hasattr(payload, 'symptom_type') else symptom['symptom_type'],
            "p_severity": payload.severity if hasattr(payload, 'severity') else symptom['severity'],
            "p_notes": payload.notes if hasattr(payload, 'notes') else symptom['notes'],
            "p_meal_id": payload.meal_id if hasattr(payload, 'meal_id') else symptom['meal_id']
        }).execute()

        return response.data[0] if response.data else None
    
    @classmethod
    def get_symptom_by_id(cls, db: Client, symptom_id: int):
        symptom = db.table("symptom").select("*").eq("id", symptom_id).single().execute()
        if not symptom.data:
            return None
        return symptom.data 
    
    @classmethod
    def delete_symptom(cls, db: Client, symptom_id: int):
        symptom = cls.get_symptom_by_id(db, symptom_id)
        if not symptom:
            return False
        
        db.table("symptom").delete().eq("id", symptom_id).execute()
        return True
    
    @staticmethod
    def get_symptoms_of_date(db: Client, target_date: date):
        symptoms = db.table("symptom").eq("datetime", target_date).execute()
        return symptoms
    

get_symptoms_of_date = SymptomService.get_symptoms_of_date