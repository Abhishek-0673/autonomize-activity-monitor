import os
from src.integrations.github_client import GitHubClient
from src.core.logger import get_logger

logger = get_logger(__name__)


class GitHubService:
    def __init__(self):
        self.client = GitHubClient()
        # Your repo name stays intact for commits & PR checks
        self.repo_name = os.environ.get("GITHUB_REPO_NAME", "autonomize-activity-monitor")

    def get_user_github_activity(self, username: str, limit: int = 5, offset: int = 0):
        """
        Fetch GitHub activity (commits, PRs, repos)
        using LIMIT + OFFSET with clean metadata format.
        """

        # --------------------------
        # 1. Fetch commits (raw)
        # --------------------------
        commits_raw = self.client.get_recent_commits(
            username=username,
            repo_name=self.repo_name
        )

        if not commits_raw["success"]:
            return {"error": commits_raw["error"]}

        all_commits = commits_raw["data"]
        total_commits = len(all_commits)

        # local pagination
        paginated_commits = all_commits[offset: offset + limit]

        commits = [
            {
                "repo": f"{username}/{self.repo_name}",
                "message": item.get("commit", {}).get("message"),
                "timestamp": item.get("commit", {}).get("author", {}).get("date"),
                "url": item.get("html_url"),
                "sha": item.get("sha"),
            }
            for item in paginated_commits
        ]

        commit_meta = {
            "total": total_commits,
            "limit": limit,
            "offset": offset,
            "returned": len(commits)
        }

        # --------------------------
        # 2. Pull Requests
        # --------------------------
        prs_raw = self.client.get_pull_requests(username, self.repo_name)

        if not prs_raw["success"]:
            return {"error": prs_raw["error"]}

        all_prs = prs_raw["data"].get("items", [])
        total_prs = len(all_prs)

        paginated_prs = all_prs[offset: offset + limit]

        prs = [
            {
                "title": pr.get("title"),
                "url": pr.get("html_url"),
                "repo": self.repo_name
            }
            for pr in paginated_prs
        ]

        pr_meta = {
            "total": total_prs,
            "limit": limit,
            "offset": offset,
            "returned": len(prs)
        }

        # --------------------------
        # 3. Recent repositories
        # --------------------------
        repos_raw = self.client.get_recent_repos(username)

        if not repos_raw["success"]:
            return {"error": repos_raw["error"]}

        all_repos = repos_raw["data"]
        total_repos = len(all_repos)

        paginated_repos = all_repos[offset: offset + limit]

        repo_meta = {
            "total": total_repos,
            "limit": limit,
            "offset": offset,
            "returned": len(paginated_repos)
        }

        # --------------------------
        # 4. Final structured output
        # --------------------------
        return {
            "commits": commits,
            "commit_meta": commit_meta,

            "prs": prs,
            "pr_meta": pr_meta,

            "recent_repos": paginated_repos,
            "repo_meta": repo_meta
        }
