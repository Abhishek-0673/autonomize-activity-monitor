from src.integrations.github_client import GitHubClient
from src.core.logger import get_logger

logger = get_logger(__name__)


class GitHubService:
    def __init__(self):
        self.client = GitHubClient()

    def get_user_github_activity(self, username: str):
        # Fetch commits (via Search API)
        commits_raw = self.client.get_recent_commits(username)

        # Fetch PRs
        prs_raw = self.client.get_pull_requests(username)

        # Handle errors from commits API
        if not commits_raw["success"]:
            return {"error": f"GitHub commits error: {commits_raw['error']}"}

        # Handle errors from PRs API
        if not prs_raw["success"]:
            return {"error": f"GitHub PRs error: {prs_raw['error']}"}

        # Parse commits from Search API
        commit_items = commits_raw["data"].get("items", [])
        commits = [
            {
                "repo": item.get("repository", {}).get("full_name"),
                "message": item.get("commit", {}).get("message"),
                "timestamp": item.get("commit", {})
                                 .get("author", {})
                                 .get("date"),
                "url": item.get("html_url")
            }
            for item in commit_items
        ]

        # Only show the latest 5 commits for demo clarity
        commits = commits[:5]

        # Parse Pull Requests
        prs_items = prs_raw["data"].get("items", [])
        prs = [
            {
                "title": pr.get("title"),
                "url": pr.get("html_url"),
                "repo": pr.get("repository_url", "").split("/")[-1]
            }
            for pr in prs_items
        ]

        # Final output
        return {
            "commit_count": len(commits),
            "commits": commits,
            "pr_count": len(prs),
            "prs": prs
        }
