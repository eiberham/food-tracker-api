from fastapi import APIRouter, Depends, status
from supabase.client import Client
from typing import Annotated

from app.database import get_adm_db
from app.workflows.insights.graph import InsightsWorkflow
from app.services.insights_service import InsightsService

router = APIRouter()

@router.post("/", 
    include_in_schema=False,
    status_code=status.HTTP_200_OK,
    summary="Get Food Insights",
    description="Retrieve food insights based on analysis of symptoms."
)
async def get_insights(db: Annotated[Client, Depends(get_adm_db)]):
    users = db.auth.list_users().data
    for user in users:
        user_id = user.id
        workflow = InsightsWorkflow(user_id, db)
        graph = workflow.build_graph()
        initial_state = { "preliminary": "",  "insights": ""}
        result = graph.invoke(initial_state)
        InsightsService.upsert(db, user_id, result['insights'])