import json
from langchain_core.tools import tool
from supabase.client import Client

def create_tools(db: Client):
    @tool(description="Retrieve all meals and symptoms logged by a user on a specific date")
    def get_monthly_insights(user_id: str) -> str:
        """Retrieve all meals and symptoms logged in the last month.
        
        Returns:
            String containing meals and symptoms data for the last month
        """
        data = db.rpc("get_monthly_insights", {"p_user_id": user_id}).execute()
        result = data.data
        if not result:
            return "No data found for the last month"
        return json.dumps(result, indent=2)
    
    return [get_monthly_insights]
    
    