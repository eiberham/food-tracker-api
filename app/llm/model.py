import app.config as config
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    openai_api_key=config.vars['openai_api_key'],
    model="gpt-3.5-turbo",
    temperature=0.0,
)