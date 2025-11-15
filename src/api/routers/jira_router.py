from fastapi import APIRouter, HTTPException
from src.services.jira_service import JiraService

router = APIRouter(prefix="/jira", tags=["JIRA"])
jira_service = JiraService()

@router.get("/{username}")
def get_user_issues(username: str):
    """Fetch JIRA issues for a given user."""
    data = jira_service.get_user_issues(username)

    if "error" in data:
        raise HTTPException(status_code=500, detail=data["error"])

    return data
