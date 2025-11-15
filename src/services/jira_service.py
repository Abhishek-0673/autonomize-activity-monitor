from src.core.user_resolver import UserResolver
from src.integrations.jira_client import JiraClient
from src.core.logger import get_logger

logger = get_logger(__name__)

class JiraService:
    def __init__(self):
        self.client = JiraClient()

    def get_user_issues(self, account_id: str, limit: int = 10, offset: int = 0):
        """
        Fetch full issue list from JIRA (working version),
        then apply clean limit+offset pagination.
        """
        data = self.client.get_user_activity(account_id)
        member_name = UserResolver.resolve_reverse(account_id) or "This user"

        # Handle JIRA errors
        if "error" in data:
            return {
                "message": f"Failed to fetch issues for {member_name}.",
                "error": data["error"]
            }

        issues = data.get("issues", [])
        total = len(issues)

        if total == 0:
            return {"message": f"No active issues found for {member_name}."}

        # LOCAL OFFSET + LIMIT
        start = offset
        end = offset + limit
        paginated = issues[start:end]

        return {
            "message": f"{member_name} has {total} active issue(s).",
            "issues": paginated,
            "meta": {
                "total": total,
                "limit": limit,
                "offset": offset,
                "returned": len(paginated)
            }
        }

    def get_issue_details(self, issue_key: str):
        data = self.client.get_issue_details(issue_key)

        if "error" in data:
            return {"error": data["error"]}

        fields = data.get("fields", {})
        changelog_raw = data.get("changelog", {})

        # Ensure changelog is safe
        histories = []
        if isinstance(changelog_raw, dict):
            histories = changelog_raw.get("histories", [])

        return {
            "issue_key": issue_key,
            "summary": fields.get("summary"),
            "status": fields.get("status", {}).get("name"),
            "updated": fields.get("updated"),
            "changelog": histories
        }


