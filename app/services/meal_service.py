from app.models.meal import Meal
from app.models.meal_food import MealFood
from app.schemas.meal import MealCreate, MealUpdate
from app.services.food_service import FoodService
from app.services.user_service import UserService
from datetime import date
from sqlalchemy.orm import Session

class MealService:
    
    @classmethod
    def list_meals(cls, db: Session):
        meals = db.query(Meal).all()
        return meals
    
    @classmethod
    def create_meal(cls, db: Session, payload: MealCreate):
        meal = Meal(**payload.model_dump(exclude={"food_ids"}))

        if not UserService.get_user_by_id(db, meal.user_id):
            raise Exception("User does not exist")

        #add food associations to meal_food table
        for food_id in payload.food_ids:
            if not FoodService.get_food(db, food_id):
                raise Exception(f"Food with ID {food_id} does not exist")
            meal.meal_foods.append(MealFood(food_id=food_id))

        db.add(meal)
        db.commit()
        db.refresh(meal)
        return meal
    
    @classmethod
    def update_meal(cls, db: Session, meal_id: int, payload: MealUpdate):
        meal = cls.get_meal_by_id(db, meal_id)
        if not meal:
            return None

        if not UserService.get_user_by_id(db, meal.user_id):
            raise Exception("User does not exist")
        
        for key, value in payload.model_dump(exclude={"food_ids"}).items():
            setattr(meal, key, value)

        if payload.food_ids is not None:
            for food_id in payload.food_ids:
                if not FoodService.get_food(db, food_id):
                    raise Exception(f"Food with ID {food_id} does not exist")
                
            meal.meal_foods.clear()

            for food_id in payload.food_ids:
                meal.meal_foods.append(MealFood(food_id=food_id))
        
        db.commit()
        db.refresh(meal)
        return meal
    
    @classmethod
    def get_meal(cls, db: Session, meal_id: int):
        meal = cls.get_meal_by_id(db, meal_id)
        if not meal:
            return None
        return meal
    
    @classmethod
    def delete_meal(cls, db: Session, meal_id: int):
        meal = cls.get_meal_by_id(db, meal_id)
        if not meal:
            return False
        
        db.delete(meal)
        db.commit()
        return True

    @classmethod
    def get_meal_by_id(cls, db: Session, meal_id: int):
        meal = db.query(Meal).filter_by(id=meal_id).first()
        if not meal:
            return None
        return meal
    
    @staticmethod
    def get_meals_of_date(db: Session, user_id: int, target_date: date):
        from sqlalchemy import func
        meals = db.query(Meal).filter(
            Meal.user_id == user_id,
            func.date(Meal.created_at) == target_date
        ).all()
        return meals

get_meals_of_date = MealService.get_meals_of_date