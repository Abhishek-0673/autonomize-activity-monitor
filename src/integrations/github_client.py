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

    def _get(self, url: str, params=None, headers=None):
        try:
            response = requests.get(url, headers=headers or self.headers, params=params)
            data = response.json()
            if response.status_code >= 400:
                return {"success": False, "error": data.get("message", "Unknown GitHub error")}
            return {"success": True, "data": data}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_recent_commits(self, username: str):
        url = f"{self.BASE_URL}/search/commits"
        params = {
            "q": f"author:{username}",
            "sort": "author-date",
            "order": "desc"
        }
        headers = {
            **self.headers,
            "Accept": "application/vnd.github.cloak-preview"  # required!
        }
        return self._get(url, params=params, headers=headers)

    def get_pull_requests(self, username: str):
        url = f"{self.BASE_URL}/search/issues"
        params = {
            "q": f"author:{username} type:pr state:open"
        }
        return self._get(url, params=params)
