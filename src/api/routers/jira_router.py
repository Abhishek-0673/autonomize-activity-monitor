from fastapi import APIRouter
from src.services.jira_service import JiraService
from src.core.user_resolver import UserResolver

router = APIRouter(prefix="/api/v1/jira", tags=["JIRA"])
jira_service = JiraService()


@router.get("/users/{username}/issues")
def get_user_issues(username: str, limit: int = 10, offset: int = 0):

    resolved = UserResolver.resolve(username)
    if not resolved:
        return {"error": f"No accountId configured for '{username}'"}

    account_id = resolved["jira"]

    return jira_service.get_user_issues(account_id, limit=limit, offset=offset)


@router.get("/issues/{issue_key}")
def get_issue_details(issue_key: str):
    """Get full details of a specific JIRA issue."""
    return jira_service.get_issue_details(issue_key)
