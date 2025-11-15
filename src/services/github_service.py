from src.integrations.github_client import GitHubClient
from src.core.logger import get_logger

logger = get_logger(__name__)


class GitHubService:
    def __init__(self):
        self.client = GitHubClient()
        self.repo_name = "autonomize-activity-monitor"

    def get_user_github_activity(self, username: str, limit: int = 5, page: int = 1):
        # ---- Total commits ----
        total_commits = self.client.get_total_commits(username, self.repo_name)
        total_pages = (total_commits + limit - 1) // limit  # ceil

        # ---- Commits for this page ----
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
                "sha": item.get("sha")
            }
            for item in commit_items
        ]

        # ---- PRs ----
        prs_raw = self.client.get_pull_requests(username, self.repo_name)
        if not prs_raw["success"]:
            return {"error": prs_raw["error"]}

        prs = [
            {
                "title": pr.get("title"),
                "url": pr.get("html_url"),
                "repo": self.repo_name
            }
            for pr in prs_raw["data"].get("items", [])
        ]

        # ---- Final Response ----
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
            }
        }

