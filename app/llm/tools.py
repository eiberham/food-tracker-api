from langchain_core.tools import tool
from sentence_transformers import SentenceTransformer
from app.services.meal_service import MealService
from app.services.symptom_service import SymptomService
from app.services.retriever_service import RetrieverService
from datetime import date
import app.config as config
import json

def get_tools(db):
    @tool(description="Retrieve all meals logged by a user on a specific date")
    def get_meals_of_date(target_date: date):
        """Retrieve all meals logged by a user on a specific date.
        
        Args:
            target_date: Date to retrieve meals for (YYYY-MM-DD format)
            
        Returns:
            String containing meals data for the specified date
        """
        meals = MealService.get_meals_of_date(db, target_date)
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
        symptoms = SymptomService.get_symptoms_of_date(db, target_date)
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
    
    @tool(description="Search relevant documents based on a query")
    def search_docs(query: str) -> str:
        """Search relevant documents based on a query.  
        
        Args:
            query: The search query string.

        Returns:
            A string containing the search results.
        """

        try:
            supabase_url = config.vars["supabase_url"]
            supabase_secret_key = config.vars["supabase_secret_key"]

            model = SentenceTransformer('BAAI/bge-small-en')
            vector = model.encode(query)

            retriever = RetrieverService(supabase_url, supabase_secret_key)
            results = retriever.search(embedding=vector.tolist(), match_count=3)

            context = "".join([result['content'] for result in results])
            # Limit context to prevent token overflow
            return context[:2000] + "..." if len(context) > 2000 else context
        
        except Exception as e:
            return f"Error during document search: {str(e)}"

    
    return [get_meals_of_date, get_symptoms_of_date, search_docs]