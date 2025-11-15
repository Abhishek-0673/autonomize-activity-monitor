import requests
from src.core.config import settings
from src.core.logger import get_logger
from src.integrations.base_client import BaseClient

logger = get_logger(__name__)

class JiraClient(BaseClient):
    """Handles communication with the JIRA Cloud REST API."""

    def __init__(self):
        self.base_url = f"{settings.jira_base_url}/rest/api/3"
        self.auth = (settings.jira_email, settings.jira_api_token)
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

    def get_user_activity(self, account_id: str) -> dict:
        """Fetch issues assigned to the given JIRA accountId."""

        jql = f'project = SCRUM AND assignee = "{account_id}" AND statusCategory != Done ORDER BY updated DESC'
        logger.info(f"Final JQL used: {jql}")

        url = f"{self.base_url}/search/jql"
        payload = {
            "jql": jql,
            "maxResults": 10,
            "fields": ["summary", "status", "updated"]
        }

        logger.info(f"Fetching JIRA issues for accountId: {account_id}")

        try:
            response = requests.post(url, auth=self.auth, headers=self.headers, json=payload)

            # Don't use raise_for_status() — handle errors manually
            try:
                data = response.json()
            except Exception as e:
                logger.error(f"JIRA returned invalid JSON: {e}")
                return {"error": "Invalid JSON response from JIRA."}

            # Handle HTTP errors gracefully
            if response.status_code >= 400:
                error_msg = data.get("errorMessages", ["Unknown JIRA error"])[0]
                logger.error(f"JIRA error for {account_id}: {error_msg}")
                return {"error": error_msg}

            # Handle JIRA application-level errors
            if "errorMessages" in data:
                error_msg = data["errorMessages"][0]
                logger.error(f"JIRA error for {account_id}: {error_msg}")
                return {"error": error_msg}

            # Safe extraction
            issues = [
                {
                    "key": issue.get("key"),
                    "summary": issue.get("fields", {}).get("summary"),
                    "status": issue.get("fields", {}).get("status", {}).get("name"),
                    "updated": issue.get("fields", {}).get("updated"),
                }
                for issue in data.get("issues", [])
            ]

            return {"user": account_id, "count": len(issues), "issues": issues}

        except requests.exceptions.RequestException as e:
            logger.error(f"Network error contacting JIRA: {e}")
            return {"error": "Network error contacting JIRA service."}

    def get_issue_details(self, issue_key: str):
        """Fetch details of a specific JIRA issue."""
        url = f"{self.base_url}/issue/{issue_key}?expand=changelog"

        try:
            r = requests.get(url, auth=self.auth, headers=self.headers)
            data = r.json()

            if r.status_code >= 400:
                return {"error": data.get("errorMessages", ["Unknown error"])[0]}

            issue = {
                "key": data.get("key"),
                "summary": data["fields"].get("summary"),
                "description": data["fields"].get("description"),
                "status": data["fields"].get("status", {}).get("name"),
                "priority": data["fields"].get("priority", {}).get("name"),
                "assignee": data["fields"].get("assignee", {}).get("displayName"),
                "updated": data["fields"].get("updated"),
                "created": data["fields"].get("created"),
                "comments": [
                    {
                        "author": c["author"]["displayName"],
                        "body": c["body"],
                        "created": c["created"]
                    }
                    for c in data["fields"].get("comment", {}).get("comments", [])
                ],
                "changelog": [
                    {
                        "field": h["items"][0].get("field"),
                        "from": h["items"][0].get("fromString"),
                        "to": h["items"][0].get("toString"),
                        "created": h.get("created")
                    }
                    for h in data.get("changelog", {}).get("histories", [])
                ]
            }

            return issue

        except Exception as e:
            return {"error": str(e)}



