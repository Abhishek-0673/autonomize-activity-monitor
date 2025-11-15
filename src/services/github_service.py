from src.integrations.github_client import GitHubClient
from src.core.logger import get_logger

logger = get_logger(__name__)

class GitHubService:
    def __init__(self):
        self.client = GitHubClient()

    def get_user_github_activity(self, username: str):
        commits_raw = self.client.get_recent_commits(username)
        prs_raw = self.client.get_pull_requests(username)

        if not commits_raw["success"]:
            return {"error": commits_raw["error"]}

        if not prs_raw["success"]:
            return {"error": prs_raw["error"]}

        commits = []
        for e in commits_raw["data"]:
            if e.get("type") == "PushEvent":
                commits_list = e.get("payload", {}).get("commits", [])
                for commit in commits_list:
                    commits.append({
                        "repo": e["repo"]["name"],
                        "message": commit.get("message"),
                        "timestamp": e.get("created_at")
                    })

        prs = [
            {
                "title": item.get("title"),
                "url": item.get("html_url"),
                "repo": item.get("repository_url", "").split("/")[-1]
            }
            for item in prs_raw["data"].get("items", [])
        ]

        return {
            "commit_count": len(commits),
            "commits": commits[:5],  # limit for demo
            "pr_count": len(prs),
            "prs": prs
        }

