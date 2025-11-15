import os

import requests
from src.core.config import settings
from src.core.logger import get_logger

logger = get_logger(__name__)

class GitHubClient:
    BASE_URL = os.environ.get("GITHUB_API_HOST_URL", "https://api.github.com")

    def __init__(self):
        self.token = settings.github_token
        self.headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github+json",
            "User-Agent": "activity-monitor"
        }

    def _get(self, url: str, params=None, headers=None):
        try:
            response = requests.get(
                url,
                headers=headers or self.headers,
                params=params or {}
            )
            data = response.json()

            if response.status_code >= 400:
                return {
                    "success": False,
                    "error": data.get("message", "Unknown GitHub error")
                }

            return {"success": True, "data": data}

        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_recent_commits(self, username: str, repo_name: str, limit: int = 5, page: int = 1):
        """Fetch commits from a repo with pagination."""
        url = f"{self.BASE_URL}/repos/{username}/{repo_name}/commits"

        params = {
            "per_page": limit,
            "page": page,
        }

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

    def get_total_commits(self, username: str, repo_name: str):
        """
        Fetch total number of commits in the repo using GitHub Link headers.
        """

        url = f"{self.BASE_URL}/repos/{username}/{repo_name}/commits"
        params = {"per_page": 1, "page": 1}

        response_data = requests.get(
            url,
            headers=self.headers,
            params=params
        )

        # If no link header → only 1 page
        link = response_data.headers.get("Link", "")
        if not link:
            return 1

        # Example link:
        # <https://api.../commits?page=12>; rel="last"
        parts = link.split(",")
        last = [p for p in parts if 'rel="last"' in p]

        if not last:
            return 1

        last_url = last[0].split(";")[0].strip()[1:-1]
        last_page_num = int(last_url.split("page=")[-1])

        return last_page_num  # total commits = last_page_num (since per_page=1)


