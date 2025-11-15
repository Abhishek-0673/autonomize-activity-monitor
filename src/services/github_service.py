from src.integrations.github_client import GitHubClient
from src.core.logger import get_logger

logger = get_logger(__name__)


class GitHubService:
    def __init__(self):
        self.client = GitHubClient()
        self.repo_name = "autonomize-activity-monitor"

    def get_user_github_activity(self, username: str):
        # ---- Fetch commits ----
        commits_raw = self.client.get_recent_commits(username, self.repo_name)

        if not commits_raw["success"]:
            return {"error": f"GitHub commits error: {commits_raw['error']}"}

        # Repo commits format:
        # [
        #   {
        #       "commit": {...},
        #       "html_url": "...",
        #       ...
        #   }
        # ]

        commits = [
            {
                "repo": f"{username}/{self.repo_name}",
                "message": item.get("commit", {}).get("message"),
                "timestamp": item.get("commit", {}).get("author", {}).get("date"),
                "url": item.get("html_url")
            }
            for item in commits_raw["data"]
        ]

        # ---- Fetch PRs ----
        prs_raw = self.client.get_pull_requests(username, self.repo_name)

        if not prs_raw["success"]:
            return {"error": f"GitHub PR error: {prs_raw['error']}"}

        pr_items = prs_raw["data"].get("items", [])

        prs = [
            {
                "title": pr.get("title"),
                "url": pr.get("html_url"),
                "repo": pr.get("repository_url", "").split("/")[-1]
            }
            for pr in pr_items
        ]

        # ---- Final Response ----
        return {
            "commit_count": len(commits),
            "commits": commits,
            "pr_count": len(prs),
            "prs": prs,
        }
