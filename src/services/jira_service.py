from src.api.utils.response_builder import success, failure
from src.core.user_resolver import UserResolver
from src.integrations.jira_client import JiraClient
from src.core.logger import get_logger

logger = get_logger(__name__)

class JiraService:
    """Handles communication with the JIRA Cloud REST API."""
    def __init__(self):
        self.client = JiraClient()

    def get_user_issues(self, account_id: str, limit: int = 10, offset: int = 0):
        """Fetch issues for a user."""
        data = self.client.get_user_activity(account_id)
        member_name = UserResolver.resolve_reverse(account_id) or "This user"

        if "error" in data:
            return failure(f"Failed to fetch issues for {member_name}.", data["error"])

        issues = data.get("issues", [])
        total = len(issues)

        if total == 0:
            return success(message=f"No active issues found for {member_name}.", items=[], meta={"total": 0})

        paginated = issues[offset: offset + limit]

        return success(
            message=f"{member_name} has {total} active issue(s).",
            items=paginated,
            meta={
                "total": total,
                "limit": limit,
                "offset": offset,
                "returned": len(paginated)
            }
        )

    def get_issue_details(self, issue_key: str):
        """Fetch details of a specific JIRA issue."""
        data = self.client.get_issue_details(issue_key)
        if "error" in data:
            return failure(f"Failed to fetch issue {issue_key}.", data["error"])

        fields = data.get("fields", data)

        def get_val(*path):
            """Helper function to extract values from nested dicts."""
            curr = fields
            for p in path:
                if isinstance(curr, dict):
                    curr = curr.get(p)
                else:
                    return None
            return curr

        def extract_description(desc):
            """Extracts description from JIRA issue."""
            if desc is None:
                return None
            if isinstance(desc, str):
                return desc
            if isinstance(desc, dict) and desc.get("type") == "doc":
                text = []
                for block in desc.get("content", []):
                    if block.get("type") == "paragraph":
                        for item in block.get("content", []):
                            t = item.get("text")
                            if t:
                                text.append(t)
                return " ".join(text)
            return None

        raw_changelog = data.get("changelog") or fields.get("changelog") or []
        changelog = []

        if isinstance(raw_changelog, list):
            for c in raw_changelog:
                changelog.append({
                    "field": c.get("field"),
                    "from": c.get("from"),
                    "to": c.get("to"),
                    "created": c.get("created")
                })
        else:
            for h in raw_changelog.get("histories", []):
                for item in h.get("items", []):
                    changelog.append({
                        "field": item.get("field"),
                        "from": item.get("fromString"),
                        "to": item.get("toString"),
                        "created": h.get("created")
                    })

        normalized = {
            "issue_key": data.get("key"),
            "summary": get_val("summary"),
            "description": extract_description(get_val("description")),
            "status": get_val("status", "name"),
            "priority": get_val("priority", "name"),
            "assignee": get_val("assignee", "displayName"),
            "reporter": get_val("reporter", "displayName"),
            "labels": get_val("labels") or [],
            "issue_type": get_val("issuetype", "name"),
            "updated": get_val("updated"),
            "created": get_val("created"),
            "attachments": fields.get("attachment", []),
            "changelog": changelog
        }

        return success(
            message=f"Issue {issue_key} details retrieved.",
            items=normalized
        )
