from langchain_core.tools import tool
from app.services.meal_service import MealService
from app.services.symptom_service import SymptomService
from datetime import date
import json

def get_tools(db, user_id: int):
    @tool(description="Retrieve all meals logged by a user on a specific date")
    def get_meals_of_date(target_date: date):
        """Retrieve all meals logged by a user on a specific date.
        
        Args:
            target_date: Date to retrieve meals for (YYYY-MM-DD format)
            
        Returns:
            String containing meals data for the specified date
        """
        meals = MealService.get_meals_of_date(db, user_id, target_date)
        if not meals:
            return f"No meals found for {target_date}"
        
        # return a response in string format
        result = []
        for meal in meals:
            info = {
                "id": meal.id,
                "name": meal.name,
                "created_at": str(meal.created_at),
                "foods": [food.food_id for food in meal.meal_foods] if hasattr(meal, 'meal_foods') else []
            }
            result.append(info)
        
        return json.dumps(result, indent=2)

    @tool(description="Retrieve all symptoms logged by a user on a specific date")
    def get_symptoms_of_date(target_date: date):
        """Retrieve all symptoms logged by a user on a specific date.
        
        Args:
            target_date: Date to retrieve symptoms for (YYYY-MM-DD format)
            
        Returns:
            String containing symptoms data for the specified date
        """
        symptoms = SymptomService.get_symptoms_of_date(db, user_id, target_date)
        if not symptoms:
            return f"No symptoms found for {target_date}"
        
        # return a response in string format
        result = []
        for symptom in symptoms:
            info = {
                "id": symptom.id,
                "name": symptom.name,
                "severity": symptom.severity,
                "datetime": str(symptom.datetime),
                "notes": symptom.notes
            }
            result.append(info)
        
        return json.dumps(result, indent=2)
    
    return [get_meals_of_date, get_symptoms_of_date]