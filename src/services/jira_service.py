from src.core.user_resolver import UserResolver
from src.integrations.jira_client import JiraClient
from src.core.logger import get_logger

logger = get_logger(__name__)

class JiraService:
    def __init__(self):
        self.client = JiraClient()

    def get_user_issues(self, account_id: str):
        data = self.client.get_user_activity(account_id)

        # resolve name
        member_name = UserResolver.resolve_reverse(account_id) or "This user"

        if "error" in data:
            return {"message": f"Failed to fetch issues for {member_name}.", "error": data["error"]}

        if data["count"] == 0:
            return {"message": f"No active issues found for {member_name}."}

        return {
            "message": f"{member_name} has {data['count']} active issue(s).",
            "issues": data["issues"],
        }
