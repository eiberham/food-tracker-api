from app.models.Symptom import Symptom
from app.schemas.Symptom import SymptomCreate, SymptomUpdate
from app.services.MealService import MealService
from app.services.UserService import UserService

class SymptomService:

    @classmethod
    def list_symptoms(cls, db):
        symptoms = db.query(Symptom).all()
        return symptoms

    @classmethod
    def create_symptom(cls, db, payload: SymptomCreate):
        symptom = Symptom(**payload.model_dump())

        if not UserService.get_user_by_id(db, payload.user_id):
            raise Exception("User does not exist")
        
        if not MealService.get_meal_by_id(db, payload.meal_id):
            raise Exception("Meal does not exist")
        
        db.add(symptom)
        db.commit()
        db.refresh(symptom)
        return symptom
    
    @classmethod
    def update_symptom(cls, db, symptom_id: int, payload: SymptomUpdate):
        symptom = cls.get_symptom_by_id(db, symptom_id)
        if not symptom:
            return None
        
        for key, value in payload.model_dump().items():
            setattr(symptom, key, value)

        db.commit()
        db.refresh(symptom)
        return symptom
    
    @classmethod
    def get_symptom_by_id(cls, db, symptom_id: int):
        symptom = db.query(Symptom).filter_by(id=symptom_id).first()
        if not symptom:
            return None
        return symptom
    
    @classmethod
    def delete_symptom(cls, db, symptom_id: int):
        symptom = cls.get_symptom_by_id(db, symptom_id)
        if not symptom:
            return False
        
        db.delete(symptom)
        db.commit()
        return True