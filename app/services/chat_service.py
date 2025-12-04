from app.llm.agent import create
from sqlalchemy.orm import Session

class ChatService:
    
    @classmethod
    def chat(cls, db: Session, user_id:int, message: str):
        try:
            
            agent = create(db, user_id)
            
            response = agent.invoke({"input": message})
            
            if isinstance(response, dict):
                if "messages" in response:
                    last_message = response["messages"][-1]
                    response_text = last_message.content
                elif "output" in response:
                    response_text = response["output"]
                else:
                    response_text = str(response)
            else:
                response_text = str(response)
                
            return {"response": response_text}
        except Exception as e:
            print(f"Error in ChatService: {e}")
            raise e


        