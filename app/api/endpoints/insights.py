from fastapi import APIRouter, Depends
from supabase.client import Client
from typing import Annotated

from app.database import get_authenticated_db
from app.workflows.insights.graph import InsightsWorkflow
from app.services.email_service import EmailService

router = APIRouter()

@router.get("/insights/{user_id}", 
    include_in_schema=True,
    status_code=200,
    summary="Get Food Insights",
    description="Retrieve food insights based on analysis of symptoms."
)
async def get_insights(user_id: str, db: Annotated[Client, Depends(get_authenticated_db)]):
    workflow = InsightsWorkflow(user_id, db)
    graph =workflow.build_graph()
    initial_state = { "preliminary": "",  "insights": ""}
    result = graph.invoke(initial_state)
    to = db.auth.get_user().user.email
    EmailService.send(db, to, result['insights'])