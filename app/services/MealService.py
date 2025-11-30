from app.models.Meal import Meal
from app.schemas.Meal import MealCreate, MealUpdate

class MealService:
    
    @classmethod
    def list_meals(cls, db):
        meals = db.query(Meal).all()
        return meals
    
    @classmethod
    def create_meal(cls, db, payload: MealCreate):
        meal = Meal(**payload.model_dump())
        db.add(meal)
        db.commit()
        db.refresh(meal)
        return meal
    
    @classmethod
    def update_meal(cls, db, meal_id: int, payload: MealUpdate):
        meal = cls.get_meal_by_id(db, meal_id)
        if not meal:
            return None
        
        for key, value in payload.model_dump().items():
            setattr(meal, key, value)
        
        db.commit()
        db.refresh(meal)
        return meal
    
    @classmethod
    def get_meal(cls, db, meal_id: int):
        meal = cls.get_meal_by_id(db, meal_id)
        if not meal:
            return None
        return meal
    
    @classmethod
    def delete_meal(cls, db, meal_id: int):
        meal = cls.get_meal_by_id(db, meal_id)
        if not meal:
            return False
        
        db.delete(meal)
        db.commit()
        return True

    @classmethod
    def get_meal_by_id(cls, db, meal_id: int):
        meal = db.query(Meal).filter_by(id=meal_id).first()
        return meal
