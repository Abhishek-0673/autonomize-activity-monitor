import requests
from src.core.config import settings
from src.core.logger import get_logger

logger = get_logger(__name__)

class GitHubClient:
    BASE_URL = "https://api.github.com"

    def __init__(self):
        self.token = settings.github_token
        self.headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github+json",
            "User-Agent": "activity-monitor"
        }

    def _get(self, url: str, params=None, headers=None):
        try:
            response = requests.get(url, headers=headers or self.headers, params=params)
            data = response.json()
            if response.status_code >= 400:
                return {"success": False, "error": data.get("message", "Unknown GitHub error")}
            return {"success": True, "data": data}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_recent_commits(self, username: str, repo_name: str = "autonomize-activity-monitor"):
        """Fetch latest commits for the given repo."""
        url = f"{self.BASE_URL}/repos/{username}/{repo_name}/commits"
        params = {"per_page": 5}

        return self._get(url, params=params)

    def get_pull_requests(self, username: str, repo_name: str = "autonomize-activity-monitor"):
        """Search PRs authored by user in a specific repo only."""
        url = f"{self.BASE_URL}/search/issues"

        params = {
            "q": f"author:{username} repo:{username}/{repo_name} type:pr",
            "sort": "created",
            "order": "desc"
        }

        return self._get(url, params=params)

