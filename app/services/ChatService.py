from groq import Groq
import os
from app.llm.tools import tools, function_map
from app.llm.prompt import content
import json
from datetime import datetime

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

class ChatService:

    @classmethod
    def run_llm(cls, message: str):
        pass
    
    @classmethod
    def chat(cls, db, user_id:int, message: str):
        try:
            messages = [
                {
                    "role": "system", 
                    "content": content
                },
                {"role": "user", "content": message}
            ]
            
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=messages,
                tools=tools,
                tool_choice="auto",
            )

            message_obj = response.choices[0].message
            print(f"Response has tool_calls: {bool(message_obj.tool_calls)}")

            if message_obj.tool_calls:
                print(f"Tool calls found: {len(message_obj.tool_calls)}")
                
                # Process all tool calls and collect results
                tool_results = []
                
                for tool_call in message_obj.tool_calls:
                    try:
                        function_name = tool_call.function.name
                        args = json.loads(tool_call.function.arguments)
                        print(f"Calling function: {function_name} with args: {args}")
                        
                        # Convert date string to date object
                        date_str = args["date"]
                        date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()

                        result = function_map.get(function_name)(db, user_id, date_obj)
                        
                        # Convert SQLAlchemy objects to dictionaries
                        """ if hasattr(result, '__iter__') and not isinstance(result, (str, dict)):
                            result = [
                                {
                                    "id": item.id if hasattr(item, 'id') else None,
                                    "name": item.name if hasattr(item, 'name') else None,
                                    "description": item.description if hasattr(item, 'description') else None,
                                    "created_at": str(item.created_at) if hasattr(item, 'created_at') else None
                                } for item in result
                            ] """
                        
                        print(f"Function result: {result}")
                        tool_results.append({
                            "function": function_name,
                            "args": args,
                            "result": result
                        })
                    except Exception as e:
                        print(f"Error processing tool call: {e}")
                        tool_results.append({
                            "function": function_name,
                            "args": args,
                            "result": {"error": str(e)}
                        })

                # Create a simple response with the data
                if tool_results:
                    response_text = "Based on your data:\n\n"
                    for tool_result in tool_results:
                        if tool_result["function"] == "get_meals_of_date":
                            date = tool_result["args"]["date"]
                            meals = tool_result["result"]
                            if isinstance(meals, list) and meals:
                                response_text += f"**Meals on {date}:**\n"
                                for meal in meals:
                                    response_text += f"- {meal.get('name', 'Unknown meal')}\n"
                            else:
                                response_text += f"No meals found for {date}.\n"
                        elif tool_result["function"] == "get_symptoms_of_date":
                            date = tool_result["args"]["date"]
                            symptoms = tool_result["result"]
                            if isinstance(symptoms, list) and symptoms:
                                response_text += f"**Symptoms on {date}:**\n"
                                for symptom in symptoms:
                                    response_text += f"- {symptom.get('description', 'Unknown symptom')}\n"
                            else:
                                response_text += f"No symptoms found for {date}.\n"
                    
                    return response_text
                else:
                    return "I couldn't retrieve the data you requested."
            else:
                print("No tool calls made")
                return message_obj.content if message_obj.content else "I'm here to help with your food tracking!"
                
        except Exception as e:
            print(f"Error in chat service: {e}")
            return f"Sorry, I encountered an error: {str(e)}"
    