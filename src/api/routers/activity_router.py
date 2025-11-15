from fastapi import APIRouter, Query
from src.api.models.query_models import QueryRequestModel
from src.services.activity_service import ActivityService

router = APIRouter()
service = ActivityService()

@router.post("/activity")
def get_activity(
    payload: QueryRequestModel,
    limit: int = Query(5, description="Items per page"),
    page: int = Query(1, description="Page number")
):
    return service.get_activity(
        question=payload.question,
        limit=limit,
        page=page
    )
