from langgraph.graph import StateGraph, START, END
from app.workflows.insights.state import InsightsState
from app.workflows.insights.agents.analyst import AnalystAgent
from app.workflows.insights.agents.output import OutputAgent
from supabase.client import Client

class InsightsWorkflow:
    def __init__(self, user_id: str, db: Client):
        self.user_id = user_id
        self.db = db

        self.analyst_agent = AnalystAgent(model="gpt-4.1-mini", db=self.db)
        self.output_agent = OutputAgent(model="gpt-4.1")

        self.graph = StateGraph(InsightsState)
    
    def build_graph(self) -> StateGraph[InsightsState]:
        self.graph.add_node("analysis", self.analysis_node)
        self.graph.add_node("output", self.outcome_node)
        self.graph.add_edge(START, "analysis")
        self.graph.add_edge("analysis", "output")
        self.graph.add_edge("output", END)
        return self.graph.compile()
    
    def analysis_node(self, state: InsightsState) -> InsightsState:
        """A simple node that adds a preliminary analysis to the state."""
        result = self.analyst_agent.run(self.user_id)
        update = {**state, "preliminary": result}
        return update
    
    def outcome_node(self, state: InsightsState) -> InsightsState:
        """A simple node that adds a recommended message to the state."""
        insights = self.output_agent.run(state['preliminary'])
        update = {**state, "insights": insights}
        return update