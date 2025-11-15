import requests
from src.core.config import settings
from src.core.logger import get_logger

logger = get_logger(__name__)

class GitHubClient:
    BASE_URL = "https://api.github.com"

    def __init__(self):
        self.headers = {
            "Authorization": f"Bearer {settings.github_token}",
            "Accept": "application/vnd.github+json"
        }

    def _get(self, url: str, params: dict = None):
        try:
            response = requests.get(url, headers=self.headers, params=params)
            data = response.json()

            # Any error?
            if response.status_code >= 400:
                msg = data.get("message", "Unknown GitHub API error")
                logger.error(f"GitHub error: {msg}")
                return {"success": False, "error": msg}

            return {"success": True, "data": data}

        except Exception as e:
            logger.error(f"GitHub network error: {e}")
            return {"success": False, "error": str(e)}

    def get_recent_commits(self, username: str):
        url = f"{self.BASE_URL}/users/{username}/events"
        return self._get(url)

    def get_pull_requests(self, username: str):
        url = f"{self.BASE_URL}/search/issues"
        params = {
            "q": f"author:{username} type:pr state:open"
        }
        return self._get(url, params=params)
