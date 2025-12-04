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

    llm_with_tools = llm.bind_tools(bound_tools)
    
    class SimpleAgent:
        def __init__(self, llm_with_tools, tools, prompt):
            self.llm = llm_with_tools
            self.tools = {tool.name: tool for tool in tools}
            self.prompt = prompt
            
        def invoke(self, input_dict):
            message = input_dict["input"]
            full_prompt = f"{self.prompt}\n\nUser: {message}\nAssistant:"
            
            response = self.llm.invoke(full_prompt)
            
            if response.tool_calls:
                for tool_call in response.tool_calls:
                    tool_name = tool_call['name']
                    tool_args = tool_call['args']
                    
                    print(f"Executing tool {tool_name} with args {tool_args}")
                    
                    if tool_name in self.tools:
                        try:
                            tool_result = self.tools[tool_name].invoke(tool_args)
                            
                            # Create a follow-up call with the tool result
                            follow_up_prompt = f"{full_prompt}\n\nTool {tool_name} returned: {tool_result}\n\nBased on this information, please provide a helpful response:"
                            final_response = llm.invoke(follow_up_prompt)
                            
                            return {"messages": [final_response]}
                        except Exception as e:
                            error_response = f"I tried to search for information but encountered an error: {e}"
                            return {"messages": [type('MockMessage', (), {'content': error_response})()]}
            
            return {"messages": [response]}
    
    agent = SimpleAgent(llm_with_tools, bound_tools, prompt)

    """ agent = create_agent(
        model=llm,
        tools=bound_tools,
        system_prompt=prompt,
    ) """
    
    return agent
