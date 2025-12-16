from app.schemas.meal import MealCreate, MealUpdate
from app.services.food_service import FoodService
from datetime import date
from supabase.client import Client

class MealService:
    
    @classmethod
    def list_meals(cls, db: Client):
        meals = db.table("meal").select("*").execute()
        return meals.data
    
    @classmethod
    def create_meal(cls, db: Client, payload: MealCreate):
        meal = payload.model_dump(exclude={"food_ids"})
        
        if hasattr(payload, 'food_ids') and payload.food_ids :
            for food_id in payload.food_ids:
                if not FoodService.get_food(db, food_id):
                    raise Exception(f"Food with ID {food_id} does not exist")
        
        result = db.rpc("create_meal_with_foods", {
            "meal_name": meal["name"],
            "food_ids": payload.food_ids or []
        }).execute()

        return result.data[0] if result.data else None
    
    @classmethod
    def update_meal(cls, db: Client, meal_id: int, payload: MealUpdate):
        meal = cls.get_meal_by_id(db, meal_id)
        if not meal:
            return None
        
        meal = payload.model_dump(exclude_unset=True, exclude={"food_ids"})

        result = db.rpc("update_meal_with_foods", {
            "p_meal_id": meal_id,
            "meal_name": meal["name"],
            "food_ids": payload.food_ids if hasattr(payload, 'food_ids') else None
        }).execute()

        return result.data[0] if result.data else None
        
    @classmethod
    def get_meal(cls, db: Client, meal_id: int):
        meal = cls.get_meal_by_id(db, meal_id)
        if not meal:
            return None
        return meal
    
    @classmethod
    def delete_meal(cls, db: Client, meal_id: int):
        meal = cls.get_meal_by_id(db, meal_id)
        if not meal:
            return False
        
        db.table("meal").delete().eq("id", meal_id).execute()
        return True

    @classmethod
    def get_meal_by_id(cls, db: Client, meal_id: int):
        meal = db.table("meal").select("*").eq("id", meal_id).execute()
        if not meal.data:
            return None
        return meal.data[0]
    
    @staticmethod
    def get_meals_of_date(db: Client, target_date: date):
        meals = db.table("meal").eq(
            "created_at", target_date
        ).execute()
        return meals

get_meals_of_date = MealService.get_meals_of_date