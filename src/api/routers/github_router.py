from fastapi import APIRouter
from src.services.github_service import GitHubService

router = APIRouter()
service = GitHubService()

@router.get("/github/{username}")
def get_github_activity(
    username: str,
    limit: int = 5,
    page: int = 1
):
    service = GitHubService()
    return service.get_user_github_activity(username, limit=limit, page=page)
