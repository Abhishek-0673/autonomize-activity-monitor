from src.services.intent_service import IntentService
from src.services.jira_service import JiraService
from src.services.github_service import GitHubService
from src.services.query_parser_service import QueryParserService
from src.core.user_resolver import UserResolver

from src.services.jira_service import JiraService
from src.services.github_service import GitHubService
from src.services.query_parser_service import QueryParserService
from src.core.user_resolver import UserResolver
from src.services.intent_service import IntentService


class ActivityService:
    def __init__(self):
        self.jira = JiraService()
        self.github = GitHubService()

    def get_activity(self, question: str, limit: int = 5, page: int = 1):

        # S1: Extract user
        user_name = QueryParserService.extract_user(question)
        if not user_name:
            return {"error": "Could not identify the user from your question."}

        # S2: Resolve IDs
        ids = UserResolver.resolve(user_name)
        if not ids:
            return {"error": f"No accountId configured for '{user_name}'"}

        jira_id = ids["jira"]
        github_username = ids["github"]

        # S3: Detect intent
        intent = IntentService.detect_intent(question)

        # S4: Fetch JIRA + GitHub only once
        jira_data = self.jira.get_user_issues(jira_id)
        github_data = self.github.get_user_github_activity(
            github_username, limit=limit, page=page
        )

        # S5: Intent-based dispatcher map
        response_map = {
            "JIRA_ISSUES": lambda: {
                "user": user_name,
                "jira": jira_data
            },
            "GITHUB_COMMITS": lambda: {
                "user": user_name,
                "commits": github_data.get("commits", []),
                "pagination": github_data.get("pagination", {})
            },
            "GITHUB_PRS": lambda: {
                "user": user_name,
                "prs": github_data.get("prs", [])
            },
            "GITHUB_REPOS": lambda: {
                "user": user_name,
                "recent_repos": github_data.get("recent_repos", [])
            },
        }

        # S6: Return if intent matched
        if intent in response_map:
            return response_map[intent]()

        # S7: Default: Full fusion
        return {
            "user": user_name,
            "jira": jira_data,
            "github": github_data
        }
