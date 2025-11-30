from app.schemas.Food import FoodCreate, FoodUpdate
from app.models.Food import Food

class FoodService:

    @classmethod
    def list_foods(cls, db):
        foods = db.query(Food).all()
        return foods
    
    @classmethod
    def create_food(cls, db, payload : FoodCreate) :
        exists = cls.get_food_by_name(db, payload.name)
        if exists:
            raise Exception("Food with this name already exists")
        
        food = Food(**payload.model_dump())
        db.add(food)
        db.commit()
        db.refresh(food)
        return food
    
    @classmethod
    def update_food(cls, db, food_id: int, payload : FoodUpdate):
        food = cls.get_food_by_id(db, food_id)
        if not food:
            return None
        
        for key, value in payload.model_dump().items():
            setattr(food, key, value)
        
        db.commit()
        db.refresh(food)
        return food
    
    @classmethod
    def get_food(cls, db, food_id: int):
        food = cls.get_food_by_id(db, food_id)
        if not food:
            return None
        return food
    
    @classmethod
    def delete_food(cls, db, food_id: str):
        food = cls.get_food_by_id(db, food_id)
        if not food:
            return False
        
        db.delete(food)
        db.commit()
        return True
    
    @classmethod
    def get_food_by_id(cls, db, food_id: int):
        food = db.query(Food).filter_by(id=food_id).first()
        return food
    
    @classmethod
    def get_food_by_name(cls, db, name: str):
        food = db.query(Food).filter_by(name=name).first()
        return food