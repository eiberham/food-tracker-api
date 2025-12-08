from app.llm.agent import create
from sqlalchemy.orm import Session

class ChatService:
    
    @classmethod
    def chat(cls, db: Session, user_id:int, message: str):
        try:
            
            agent = create(db, user_id)
            
            response = agent.invoke(
                { "messages": [{"role": "user", "content": message}]},
                {"configurable": {"thread_id": "1"}}
            )

            return response
        except Exception as e:
            print(f"Error in ChatService: {e}")
            raise e


        