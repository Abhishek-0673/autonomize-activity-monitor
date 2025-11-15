from src.services.activity_summary_service import ActivitySummaryService
from src.services.intent_service import IntentService
from src.services.jira_service import JiraService
from src.services.github_service import GitHubService
from src.services.query_parser_service import QueryParserService
from src.core.user_resolver import UserResolver


class ActivityService:
    def __init__(self):
        self.jira = JiraService()
        self.github = GitHubService()

    def get_activity(self, question: str, limit: int = 5, offset: int = 0):

        # S1: Extract user
        user_name = QueryParserService.extract_user(question)
        if not user_name:
            return {"error": "Could not identify the user from your question."}

        # S2: Resolve IDs from UserResolver
        ids = UserResolver.resolve(user_name)
        if not ids:
            return {"error": f"No accountId configured for '{user_name}'"}

        jira_id = ids["jira"]
        github_username = ids["github"]

        # S3: Detect intent (JIRA / commits / PRs / repos / full)
        intent = IntentService.detect_intent(question)

        # S4: Fetch GitHub once (with pagination)
        github_data = self.github.get_user_github_activity(
            github_username,
            limit=limit,
            offset=offset
        )

        # S5: Fetch JIRA once (with pagination)
        jira_data = self.jira.get_user_issues(
            jira_id,
            limit=limit,
            offset=offset
        )

        # S6: Intent dispatcher map
        response_map = {
            "JIRA_ISSUES": lambda: {
                "user": user_name,
                "jira": jira_data
            },
            "GITHUB_COMMITS": lambda: {
                "user": user_name,
                "commits": github_data.get("commits", []),
                "meta": github_data.get("commit_meta", {})
            },
            "GITHUB_PRS": lambda: {
                "user": user_name,
                "prs": github_data.get("prs", []),
                "meta": github_data.get("pr_meta", {})
            },
            "GITHUB_REPOS": lambda: {
                "user": user_name,
                "recent_repos": github_data.get("recent_repos", []),
                "meta": github_data.get("repo_meta", {})
            },
        }

        # S7: Return specific intent
        if intent in response_map:
            return response_map[intent]()

        # S8: Default: Return full activity fusion
        summary = ActivitySummaryService.generate(
            user=user_name,
            jira_data=jira_data,
            github_data=github_data
        )

        return {
            "user": user_name,
            "summary": summary,
            "jira": jira_data,
            "github": github_data
        }
