from typing import Any
from langchain.agents.middleware import AgentMiddleware, AgentState, hook_config
from langgraph.runtime import Runtime

class MonitorGuardrailMiddleware(AgentMiddleware):
    """Monitor guardrail middleware for monitoring agent execution"""

    def __init__(self):
        super().__init__()

    @hook_config(can_jump_to=[])
    def before_agent(self, state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
        """Monitor and log before agent execution"""
        if state.get("messages"):
            last_message = state["messages"][-1]
            print(f"🛡️ Before Agent: Processing message: {last_message.content[:100]}...")
        return None

    @hook_config(can_jump_to=[])
    def after_agent(self, state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
        """Monitor and log after agent execution"""
        if state.get("messages"):
            last_message = state["messages"][-1]
            print(f"🛡️ After Agent: Generated response: {last_message.content[:100]}...")
        return None