from app.services.MealService import get_meals_of_date
from app.services.SymptomService import get_symptoms_of_date

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_meals_of_date",
            "description": "Retrieve all meals logged by a user on a specific date.",
            "parameters": {
                "type": "object",
                "properties": {
                    "date": {
                        "type": "string",
                        "format": "date",
                        "description": "The date for which to retrieve meals (YYYY-MM-DD)."
                    }
                },
                "required": ["date"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_symptoms_of_date",
            "description": "Retrieve all symptoms logged by a user on a specific date.",
            "parameters": {
                "type": "object",
                "properties": {
                    "date": {
                        "type": "string",
                        "format": "date",
                        "description": "The date for which to retrieve symptoms (YYYY-MM-DD)."
                    }
                },
                "required": ["date"]
            }
        }
    }
]

function_map = {
    "get_meals_of_date": get_meals_of_date,
    "get_symptoms_of_date": get_symptoms_of_date
}