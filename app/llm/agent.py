from langchain.agents import create_agent
from app.llm.tools import get_tools
from app.llm.model import llm
from app.llm.prompt import prompt
from sqlalchemy.orm import Session

def create(db: Session, user_id: int):

    bound_tools = get_tools(db=db, user_id=user_id)
    
    print(f"Creating agent with {len(bound_tools)} tools:")
    for tool in bound_tools:
        print(f"- {tool.name}: {tool.description}")

    agent = create_agent(
        model=llm,
        tools=bound_tools,
        system_prompt=prompt,
    )

    return agent
