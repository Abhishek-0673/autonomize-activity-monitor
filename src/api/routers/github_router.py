from fastapi import APIRouter, Query
from src.services.github_service import GitHubService

router = APIRouter(prefix="/github", tags=["GitHub"])
service = GitHubService()


# Summary Endpoint (recommended for demo)
@router.get("/{username}")
def github_summary(
    username: str,
    limit: int = Query(5, ge=1, le=50),
    offset: int = Query(0, ge=0)
):
    """
    Quick GitHub overview:
    - Recent commits
    - Active PRs
    - Recent repositories
    """
    return {
        "commits": service.get_user_commits(username, limit, offset),
        "prs": service.get_user_prs(username, limit, offset),
        "recent_repos": service.get_recent_repos(username, limit, offset),
    }


# Get recent commits with date filters
@router.get("/{username}/commits")
def get_commits(
    username: str,
    limit: int = Query(5, ge=1, le=50),
    offset: int = Query(0, ge=0),
    period: str = Query(None, description="today | yesterday | this_week | last_week | this_month | last_month"),
    date_from: str = Query(None),
    date_to: str = Query(None),
):
    return service.get_user_commits(
        username=username,
        limit=limit,
        offset=offset,
        period=period,
        date_from=date_from,
        date_to=date_to
    )

# Get pull requests
@router.get("/{username}/prs")
def get_prs(
    username: str,
    limit: int = Query(5),
    offset: int = Query(0)
):
    return service.get_user_prs(username, limit, offset)


# Get recent repositories
@router.get("/{username}/repos")
def get_repos(
    username: str,
    limit: int = Query(5),
    offset: int = Query(0)
):
    return service.get_recent_repos(username, limit, offset)
