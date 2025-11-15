import os
from datetime import datetime, timedelta, timezone
from dateutil.relativedelta import relativedelta
from src.integrations.github_client import GitHubClient
from src.core.logger import get_logger

logger = get_logger(__name__)


class GitHubService:
    def __init__(self):
        self.client = GitHubClient()
        self.repo_name = os.environ.get("GITHUB_REPO_NAME", "autonomize-activity-monitor")

    # ------------------------------------------------------
    # PERIOD → DATE RANGE MAPPER
    # ------------------------------------------------------
    def resolve_period(self, period: str):
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
            until = datetime(last_month_end.year, last_month_end.month, last_month_end.day, 23, 59, 59,
                             tzinfo=timezone.utc)

        else:
            return None, None

        return since, until

    # ------------------------------------------------------
    # CORE DATE FILTER FUNCTION
    # ------------------------------------------------------
    def apply_date_filter(self, commits, since, until):
        """Filter commits by datetime range."""
        filtered = []
        for c in commits:
            ts = c.get("commit", {}).get("author", {}).get("date")
            if not ts:
                continue

            try:
                commit_dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
            except:
                continue

            # Only compare when filter exists
            if since and commit_dt < since:
                continue
            if until and commit_dt > until:
                continue

            filtered.append(c)

        return filtered

    # ------------------------------------------------------
    # 1️⃣ GET COMMITS (limit + offset + period)
    # ------------------------------------------------------
    def get_user_commits(self, username: str, limit: int = 10, offset: int = 0,
                         period: str = None, since: str = None, until: str = None):

        # Convert a period like "this_week" → since/until datetime
        if period:
            since, until = self.resolve_period(period)

        # Convert ISO date strings to datetime
        if isinstance(since, str):
            since = datetime.fromisoformat(since)

        if isinstance(until, str):
            until = datetime.fromisoformat(until)

        raw = self.client.get_recent_commits(username, self.repo_name)
        if not raw["success"]:
            return {"error": raw["error"]}

        all_commits = raw["data"]

        # Apply date filter
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

        return {
            "commits": commits,
            "meta": {
                "total": total,
                "limit": limit,
                "offset": offset,
                "returned": len(commits),
                "period": period,
                "since": since.isoformat() if since else None,
                "until": until.isoformat() if until else None
            },
        }

    # ------------------------------------------------------
    # 2️⃣ PULL REQUESTS
    # ------------------------------------------------------
    def get_user_prs(self, username: str, limit: int = 10, offset: int = 0):
        raw = self.client.get_pull_requests(username, self.repo_name)

        if not raw["success"]:
            return {"error": raw["error"]}

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

        return {
            "prs": prs,
            "meta": {
                "total": total,
                "limit": limit,
                "offset": offset,
                "returned": len(prs),
            },
        }

    # ------------------------------------------------------
    # 3️⃣ RECENT REPOS
    # ------------------------------------------------------
    def get_recent_repos(self, username: str, limit: int = 10, offset: int = 0):
        raw = self.client.get_recent_repos(username)

        if not raw["success"]:
            return {"error": raw["error"]}

        all_repos = raw["data"]
        total = len(all_repos)

        paginated = all_repos[offset: offset + limit]

        return {
            "recent_repos": paginated,
            "meta": {
                "total": total,
                "limit": limit,
                "offset": offset,
                "returned": len(paginated),
            },
        }

    # ------------------------------------------------------
    # 4️⃣ FUSION ENDPOINT USED BY /activity
    # ------------------------------------------------------
    def get_user_github_activity(self, username: str, limit: int = 10, offset: int = 0):
        return {
            "commits": self.get_user_commits(username, limit, offset),
            "prs": self.get_user_prs(username, limit, offset),
            "recent_repos": self.get_recent_repos(username, limit, offset),
        }
