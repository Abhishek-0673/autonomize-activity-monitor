from src.api.utils.response_builder import success, failure
from src.services.activity_summary_service import ActivitySummaryService
from src.services.jira_service import JiraService
from src.services.github_service import GitHubService
from src.services.query_parser_service import QueryParserService
from src.services.intent_service import IntentService
from src.core.user_resolver import UserResolver

class ActivityService:
    """Activity service for generating activity summaries."""
    def __init__(self):
        self.jira = JiraService()
        self.github = GitHubService()
        self.summarizer = ActivitySummaryService()

    def get_activity(self, question: str, limit: int = 5, offset: int = 0):
        """Generate activity summary for a user."""

        user_name = QueryParserService.extract_user(question)
        if not user_name:
            return failure("Could not identify the user from your question.")

        ids = UserResolver.resolve(user_name)
        if not ids:
            return failure(f"No accountId configured for '{user_name}'")

        jira_id = ids["jira"]
        github_username = ids["github"]

        intent = IntentService.detect_intent(question)

        jira_data = self.jira.get_user_issues(jira_id, limit, offset)
        github_data = self.github.get_user_github_activity(github_username, limit, offset)

        summary_text = self.summarizer.generate(user_name, jira_data, github_data)

        intent_map = {
            "JIRA_ISSUES": lambda: success(
                message=f"JIRA issues for {user_name}",
                items={
                    "jira": jira_data,
                    "github": github_data,
                    "summary": summary_text
                }
            ),
            "GITHUB_COMMITS": lambda: success(
                message=f"GitHub commits for {user_name}",
                items={
                    "commits": github_data.get("commits"),
                    "github": github_data,
                    "summary": summary_text
                }
            ),
            "GITHUB_PRS": lambda: success(
                message=f"GitHub PRs for {user_name}",
                items={
                    "prs": github_data.get("prs"),
                    "github": github_data,
                    "summary": summary_text
                }
            ),
            "GITHUB_REPOS": lambda: success(
                message=f"GitHub repositories for {user_name}",
                items={
                    "recent_repos": github_data.get("recent_repos"),
                    "github": github_data,
                    "summary": summary_text
                }
            )
        }

        if intent in intent_map:
            return intent_map[intent]()

        return success(
            message=f"Complete activity report for {user_name}",
            items={
                "jira": jira_data,
                "github": github_data,
                "summary": summary_text
            }
        )
