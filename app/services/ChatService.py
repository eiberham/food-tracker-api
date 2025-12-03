from app.llm.agent import create
from sqlalchemy.orm import Session

class ChatService:
    
    @classmethod
    def chat(cls, db: Session, user_id:int, message: str):
        try:
            agent = create(db, user_id)
            response = agent.invoke({"input": message})

            return {"response": response}
        except Exception as e:
            print(f"Error in ChatService: {e}")
            raise e


        