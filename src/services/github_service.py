import os

from src.integrations.github_client import GitHubClient
from src.core.logger import get_logger

logger = get_logger(__name__)


class GitHubService:
    def __init__(self):
        self.client = GitHubClient()
        self.repo_name = os.environ.get("GITHUB_REPO_NAME", "autonomize-activity-monitor")

    def get_user_github_activity(self, username: str, limit: int = 5, page: int = 1):
        """
        Fetch GitHub commits and PRs for a user with pagination,
        total commits, total pages, and full navigation links.
        """

        # 1. Total commits + total pages
        total_commits = self.client.get_total_commits(username, self.repo_name)
        total_pages = max(1, (total_commits + limit - 1) // limit)

        # 2. Fetch commits for current page
        commits_raw = self.client.get_recent_commits(
            username=username,
            repo_name=self.repo_name,
            limit=limit,
            page=page
        )

        if not commits_raw["success"]:
            return {"error": commits_raw["error"]}

        commit_items = commits_raw["data"]

        commits = [
            {
                "repo": f"{username}/{self.repo_name}",
                "message": item.get("commit", {}).get("message"),
                "timestamp": item.get("commit", {}).get("author", {}).get("date"),
                "url": item.get("html_url"),
                "sha": item.get("sha"),
            }
            for item in commit_items
        ]

        # 3. Pull Requests
        prs_raw = self.client.get_pull_requests(username, self.repo_name)
        if not prs_raw["success"]:
            return {"error": prs_raw["error"]}

        pr_items = prs_raw["data"].get("items", [])
        prs = [
            {
                "title": pr.get("title"),
                "url": pr.get("html_url"),
                "repo": self.repo_name
            }
            for pr in pr_items
        ]

        # 4. Next & Previous Pagination Logic
        next_page = page + 1 if page < total_pages else None
        prev_page = page - 1 if page > 1 else None

        base_url = f"/github/{username}"

        next_page_url = (
            f"{base_url}?limit={limit}&page={next_page}"
            if next_page else None
        )

        prev_page_url = (
            f"{base_url}?limit={limit}&page={prev_page}"
            if prev_page else None
        )

        # 5. Final Response
        return {
            "commit_count": len(commits),
            "commits": commits,
            "pr_count": len(prs),
            "prs": prs,
            "pagination": {
                "page": page,
                "limit": limit,
                "returned": len(commit_items),
                "total_commits": total_commits,
                "total_pages": total_pages,
                "next_page": next_page,
                "prev_page": prev_page,
                "next_page_url": next_page_url,
                "prev_page_url": prev_page_url,
            }
        }


