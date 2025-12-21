from langchain.agents import create_agent
from langchain.agents.middleware import SummarizationMiddleware
from langgraph.checkpoint.memory import InMemorySaver
from langsmith import traceable

from app.llm.tools import get_tools
from app.llm.model import llm
from app.llm.prompt import prompt
from supabase.client import Client

from app.api.middlewares.monitor_guardrail import MonitorGuardrailMiddleware

@traceable
def create(db: Client):
    MESSAGES_THRESHOLD = 20
    CONTEXT_THRESHOLD = 5000

    bound_tools = get_tools(db=db)

    agent = create_agent(
        model=llm,
        tools=bound_tools,
        system_prompt=prompt,
        checkpointer=InMemorySaver(),
        middleware=[
            SummarizationMiddleware(
                model=llm, 
                trigger=("tokens", CONTEXT_THRESHOLD),
                keep=("messages", MESSAGES_THRESHOLD)
            ),
            MonitorGuardrailMiddleware()
        ]
    )
    
    return agent
