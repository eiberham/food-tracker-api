"""
In order to test the streaming endpoint, use this curl command:
curl -N -X POST 'http://localhost:8000/chat/' \
  -d '{"message": "What is the goal of a low histamine diet ?"}' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer JWT_TOKEN' \
  -H 'Accept: text/event-stream'
"""


from app.llm.agent import create
from sqlalchemy.orm import Session

class ChatService:
    
    @classmethod
    def chat(cls, db: Session, user_id:int, message: str):
        try:
            
            agent = create(db, user_id)

            def stream():
                for chunk in agent.stream(
                    {"messages": [{"role": "user", "content": message}]}, 
                    config={"configurable": {"thread_id": f"user_{user_id}"}},
                    stream_mode="updates"
                ):
                    yield f"data: {chunk}\n\n"
            
            """ 
            Without streaming:
            response = agent.invoke(
                { "messages": [{"role": "user", "content": message}]},
                {"configurable": {"thread_id": "1"}}
            ) 
            return response
            """

            return stream()
        except Exception as e:
            print(f"Error in ChatService: {e}")
            raise e


        