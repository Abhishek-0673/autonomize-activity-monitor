from fastapi import APIRouter, Query
from src.api.models.query_models import QueryRequestModel
from src.services.activity_service import ActivityService

router = APIRouter()
service = ActivityService()

@router.post("/activity")
def get_activity(
    payload: QueryRequestModel,
    limit: int = Query(10, ge=1, le=50),
    offset: int = Query(0, ge=0)
):
    return service.get_activity(
        question=payload.question,
        limit=limit,
        offset=offset
    )
