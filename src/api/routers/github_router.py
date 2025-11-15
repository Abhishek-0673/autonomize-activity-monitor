from fastapi import APIRouter, Query
from src.services.github_service import GitHubService

router = APIRouter(prefix="/github", tags=["GitHub"])
service = GitHubService()

# Summary
@router.get("/{username}")
def github_summary(
    username: str,
    limit: int = Query(5),
    offset: int = Query(0),
):
    return service.get_user_github_activity(username, limit, offset)


# Commits with period OR date range
@router.get("/{username}/commits")
def get_commits(
    username: str,
    limit: int = Query(5),
    offset: int = Query(0),
    period: str = Query(None, description="today|yesterday|this_week|last_week|this_month|last_month"),
    since: str = Query(None, description="ISO date like 2025-01-01"),
    until: str = Query(None, description="ISO date like 2025-01-20"),
):
    return service.get_user_commits(username, limit, offset, period, since, until)


# Pull Requests
@router.get("/{username}/prs")
def get_prs(username: str, limit: int = 5, offset: int = 0):
    return service.get_user_prs(username, limit, offset)


# Repos
@router.get("/{username}/repos")
def get_repos(username: str, limit: int = 5, offset: int = 0):
    return service.get_recent_repos(username, limit, offset)
