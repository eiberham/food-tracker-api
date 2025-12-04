import app.config as config
from langchain_groq import ChatGroq

llm = ChatGroq(
    groq_api_key=config.vars['groq_api_key'],
    model="llama-3.1-8b-instant",
)