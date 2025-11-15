import os
from datetime import datetime, timedelta, timezone
from src.integrations.github_client import GitHubClient
from src.api.utils.response_builder import success, failure
from src.core.logger import get_logger

logger = get_logger(__name__)


class GitHubService:
    """GitHub service for fetching user activity."""
    def __init__(self):
        self.client = GitHubClient()
        self.repo_name = os.environ.get("GITHUB_REPO_NAME", "autonomize-activity-monitor")

    # Converts period strings like "today" / "this_week" → (since, until)
    def resolve_period(self, period: str):
        """Resolve period strings to since/until datetimes."""
        if not period:
            return None, None

        now = datetime.utcnow().replace(tzinfo=timezone.utc)

        if period == "today":
            since = datetime(now.year, now.month, now.day, tzinfo=timezone.utc)
            until = now

        elif period == "yesterday":
            y = now - timedelta(days=1)
            since = datetime(y.year, y.month, y.day, tzinfo=timezone.utc)
            until = datetime(now.year, now.month, now.day, tzinfo=timezone.utc)

        elif period == "this_week":
            start = now - timedelta(days=now.weekday())
            since = datetime(start.year, start.month, start.day, tzinfo=timezone.utc)
            until = now

        elif period == "last_week":
            start = now - timedelta(days=now.weekday() + 7)
            end = start + timedelta(days=6)
            since = datetime(start.year, start.month, start.day, tzinfo=timezone.utc)
            until = datetime(end.year, end.month, end.day, 23, 59, 59, tzinfo=timezone.utc)

        elif period == "this_month":
            since = datetime(now.year, now.month, 1, tzinfo=timezone.utc)
            until = now

        elif period == "last_month":
            first_this_month = datetime(now.year, now.month, 1, tzinfo=timezone.utc)
            last_month_end = first_this_month - timedelta(days=1)
            since = datetime(last_month_end.year, last_month_end.month, 1, tzinfo=timezone.utc)
            until = datetime(last_month_end.year, last_month_end.month, last_month_end.day,
                             23, 59, 59, tzinfo=timezone.utc)

        else:
            return None, None

        return since, until

    # Filters commits based on since/until
    def apply_date_filter(self, commits, since, until):
        """Apply date filters to commits."""
        filtered = []
        for c in commits:
            ts = c.get("commit", {}).get("author", {}).get("date")
            if not ts:
                continue

            try:
                commit_dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
            except:
                continue

            if since and commit_dt < since:
                continue
            if until and commit_dt > until:
                continue

            filtered.append(c)

        return filtered

    # Commit endpoint with filters and pagination
    def get_user_commits(
        self,
        username: str,
        limit: int = 10,
        offset: int = 0,
        period: str = None,
        since: str = None,
        until: str = None
    ):
        """Fetch commits from a repo with pagination."""
        if period:
            since, until = self.resolve_period(period)

        if isinstance(since, str):
            since = datetime.fromisoformat(since).replace(tzinfo=timezone.utc)

        if isinstance(until, str):
            until = datetime.fromisoformat(until).replace(tzinfo=timezone.utc)

        raw = self.client.get_recent_commits(username, self.repo_name)
        if not raw["success"]:
            return failure(raw["error"])

        all_commits = raw["data"]

        filtered = self.apply_date_filter(all_commits, since, until)
        total = len(filtered)

        paginated = filtered[offset: offset + limit]

        commits = [
            {
                "repo": f"{username}/{self.repo_name}",
                "message": c.get("commit", {}).get("message"),
                "timestamp": c.get("commit", {}).get("author", {}).get("date"),
                "url": c.get("html_url"),
                "sha": c.get("sha"),
            }
            for c in paginated
        ]

        return success(
            message=f"Commits retrieved for {username}.",
            items=commits,
            meta={
                "total": total,
                "limit": limit,
                "offset": offset,
                "returned": len(commits),
                "period": period,
                "since": since.isoformat() if since else None,
                "until": until.isoformat() if until else None,
            }
        )

    # PR endpoint with pagination
    def get_user_prs(self, username: str, limit: int = 10, offset: int = 0):
        """Fetch PRs from a repo with pagination."""
        raw = self.client.get_pull_requests(username, self.repo_name)

        if not raw["success"]:
            return failure(raw["error"])

        all_prs = raw["data"].get("items", [])
        total = len(all_prs)

        paginated = all_prs[offset: offset + limit]

        prs = [
            {
                "title": pr.get("title"),
                "url": pr.get("html_url"),
                "repo": self.repo_name,
            }
            for pr in paginated
        ]

        return success(
            message=f"PRs retrieved for {username}.",
            items=prs,
            meta={
                "total": total,
                "limit": limit,
                "offset": offset,
                "returned": len(prs),
            }
        )

    # Repository endpoint with pagination
    def get_recent_repos(self, username: str, limit: int = 10, offset: int = 0):
        """Fetch recent repos for a user with pagination."""
        raw = self.client.get_recent_repos(username)

        if not raw["success"]:
            return failure(raw["error"])

        all_repos = raw["data"]
        total = len(all_repos)

        paginated = all_repos[offset: offset + limit]

        return success(
            message=f"Recent repositories retrieved for {username}.",
            items=paginated,
            meta={
                "total": total,
                "limit": limit,
                "offset": offset,
                "returned": len(paginated),
            }
        )

    # Fusion endpoint used by /activity
    def get_user_github_activity(self, username: str, limit: int = 10, offset: int = 0, period: str = None, since: str = None, until: str = None):
        """Fuse commits, PRs, and repos for a user."""
        commits = self.get_user_commits(username, limit, offset, period, since, until)
        prs = self.get_user_prs(username, limit, offset)
        repos = self.get_recent_repos(username, limit, offset)

        return success(
            message=f"GitHub activity retrieved for {username}.",
            items={
                "commits": commits,
                "prs": prs,
                "recent_repos": repos,
            }
        )
