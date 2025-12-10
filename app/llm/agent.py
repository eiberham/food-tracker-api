from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from langsmith import traceable

from app.llm.tools import get_tools
from app.llm.model import llm
from app.llm.prompt import prompt
from sqlalchemy.orm import Session

from app.api.middlewares.monitor_guardrail import MonitorGuardrailMiddleware

@traceable
def create(db: Session, user_id: int):

    bound_tools = get_tools(db=db, user_id=user_id)

    agent = create_agent(
        model=llm,
        tools=bound_tools,
        system_prompt=prompt,
        checkpointer=InMemorySaver(),
        middleware=[MonitorGuardrailMiddleware()]
    )
    
    return agent
