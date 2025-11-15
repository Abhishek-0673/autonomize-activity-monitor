from datetime import datetime, timedelta, timezone
import os
from dateutil import parser as date_parser

from src.integrations.github_client import GitHubClient
from src.core.logger import get_logger

logger = get_logger(__name__)


class GitHubService:
    def __init__(self):
        self.client = GitHubClient()
        self.repo_name = os.environ.get("GITHUB_REPO_NAME", "autonomize-activity-monitor")

    # ------------------------------------------------------
    # DATE FILTER HELPERS
    # ------------------------------------------------------
    from datetime import timezone
    from dateutil import parser as date_parser

    def apply_date_filter(self, commits, since=None, until=None):
        """Filter commits by date range (timezone-safe)."""

        filtered = []

        for item in commits:
            ts = item.get("commit", {}).get("author", {}).get("date")
            if not ts:
                continue

            commit_date = date_parser.parse(ts)

            # Make commit_date timezone aware
            if commit_date.tzinfo is None:
                commit_date = commit_date.replace(tzinfo=timezone.utc)

            # Normalize since/until
            if since and since.tzinfo is None:
                since = since.replace(tzinfo=timezone.utc)
            if until and until.tzinfo is None:
                until = until.replace(tzinfo=timezone.utc)

            # Apply filter
            if since and commit_date < since:
                continue
            if until and commit_date > until:
                continue

            filtered.append(item)

        return filtered

    def resolve_relative_dates(self, period: str):
        """Convert keywords like 'this_week' into datetime ranges."""
        today = datetime.utcnow().date()

        if period == "today":
            return today, today

        if period == "yesterday":
            y = today - timedelta(days=1)
            return y, y

        if period == "this_week":
            start = today - timedelta(days=today.weekday())
            return start, today

        if period == "last_week":
            start = today - timedelta(days=today.weekday() + 7)
            end = start + timedelta(days=6)
            return start, end

        if period == "this_month":
            start = today.replace(day=1)
            return start, today

        if period == "last_month":
            first = today.replace(day=1)
            last_month_end = first - timedelta(days=1)
            last_month_start = last_month_end.replace(day=1)
            return last_month_start, last_month_end

        return None, None

    # ------------------------------------------------------
    # COMMITS WITH DATE FILTERS
    # ------------------------------------------------------
    def get_user_commits(self, username: str, limit: int = 10, offset: int = 0,
                         period: str = None, date_from: str = None, date_to: str = None):

        raw = self.client.get_recent_commits(username, self.repo_name)

        if not raw["success"]:
            return {"error": raw["error"]}

        all_commits = raw["data"]

        # --------------------------------------------
        # 1️⃣ Resolve date filters
        # --------------------------------------------
        since, until = None, None

        # relative filters
        if period:
            since, until = self.resolve_relative_dates(period)
            if since:
                since = datetime.combine(since, datetime.min.time(), tzinfo=timezone.utc)
            if until:
                until = datetime.combine(until, datetime.max.time(), tzinfo=timezone.utc)

        # absolute filters
        if date_from:
            since = datetime.combine(
                date_parser.parse(date_from).date(),
                datetime.min.time()
            )
        if date_to:
            until = datetime.combine(
                date_parser.parse(date_to).date(),
                datetime.max.time()
            )

        # --------------------------------------------
        # 2️⃣ Apply date filtering
        # --------------------------------------------
        filtered_commits = self.apply_date_filter(all_commits, since, until)

        total = len(filtered_commits)

        # --------------------------------------------
        # 3️⃣ Local pagination
        # --------------------------------------------
        paginated = filtered_commits[offset: offset + limit]

        commits = [
            {
                "repo": f"{username}/{self.repo_name}",
                "message": item.get("commit", {}).get("message"),
                "timestamp": item.get("commit", {}).get("author", {}).get("date"),
                "url": item.get("html_url"),
                "sha": item.get("sha"),
            }
            for item in paginated
        ]

        return {
            "commits": commits,
            "meta": {
                "total": total,
                "limit": limit,
                "offset": offset,
                "returned": len(commits),
                "filtered_since": since.isoformat() if since else None,
                "filtered_until": until.isoformat() if until else None,
                "period": period,
            },
        }
