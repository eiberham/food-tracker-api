from app.schemas.food import FoodCreate, FoodUpdate
from supabase.client import Client
class FoodService:

    @classmethod
    def list_foods(cls, db: Client):
        foods = db.table("food").select("*").execute()
        return foods.data
    
    @classmethod
    def create_food(cls, db: Client, payload : FoodCreate) :
        exists = cls.get_food_by_name(db, payload.name)
        if exists:
            raise Exception("Food with this name already exists")
        
        data = payload.model_dump()
        food = db.table("food").insert(data).select("*").execute()
        return food
    
    @classmethod
    def update_food(cls, db: Client, food_id: int, payload : FoodUpdate):
        food = cls.get_food_by_id(db, food_id)
        if not food:
            return None
        
        data = payload.model_dump(exclude_unset=True)
        food = db.table("food").update(data).eq("id", food_id).select("*").execute()
        return food
    
    @classmethod
    def get_food(cls, db: Client, food_id: int):
        food = cls.get_food_by_id(db, food_id)
        if not food:
            return None
        return food
    
    @classmethod
    def delete_food(cls, db: Client, food_id: str):
        food = cls.get_food_by_id(db, food_id)
        if not food:
            return False
        
        db.table("food").delete().eq("id", food_id).execute()
        return True
    
    @classmethod
    def get_food_by_id(cls, db: Client, food_id: int):
        food = db.table("food").select("*").eq("id", food_id).single().execute()
        return food
    
    @classmethod
    def get_food_by_name(cls, db: Client, name: str):
        food = db.table("food").select("*").eq("name", name).single().execute()
        return food