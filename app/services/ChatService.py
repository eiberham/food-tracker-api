from groq import Groq
import os

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

class ChatService:
    
    @classmethod
    def chat(cls, message: str):
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": message}
            ]
        )
        return response.choices[0].message.content