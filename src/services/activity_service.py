from src.api.utils.response_builder import success, failure
from src.services.activity_summary_service import ActivitySummaryService
from src.services.jira_service import JiraService
from src.services.github_service import GitHubService
from src.services.period_parser import PeriodParser
from src.services.query_parser_service import QueryParserService
from src.services.intent_service import IntentService
from src.core.user_resolver import UserResolver


class ActivityService:
    def __init__(self):
        self.jira = JiraService()
        self.github = GitHubService()
        self.summarizer = ActivitySummaryService()

    #   TOP-LEVEL INTENT TEXT
    def _intent_message(self, intent: str, user: str) -> str:
        mapping = {
            "JIRA_ISSUES": f"JIRA issues for {user}",
            "GITHUB_COMMITS": f"Recent commits by {user}",
            "GITHUB_PRS": f"Pull requests by {user}",
            "GITHUB_REPOS": f"Repository activity for {user}",
        }
        return mapping.get(intent, f"Activity summary for {user}")

    #   HELPERS: build response items per intent
    def _build_jira_items(self, jira_data):
        return {"jira": jira_data}

    def _build_github_commits_items(self, github_data):
        return {"commits": github_data["data"]["items"]["commits"]}

    def _build_github_prs_items(self, github_data):
        return {"prs": github_data["data"]["items"]["prs"]}

    def _build_github_repos_items(self, github_data):
        return {"repos": github_data["data"]["items"]["recent_repos"]}

    def _build_full_activity_items(self, jira_data, github_data, summary_text):
        return {
            "jira": jira_data,
            "github": github_data,
            "summary": summary_text
        }

    #   MAIN ENTRYPOINT — clean, readable, no duplication
    def get_activity(self, question: str, limit: int = 5, offset: int = 0):
        # 1. Identify user
        user_name = QueryParserService.extract_user(question)
        if not user_name:
            return failure("Could not identify the user from our records!")

        # 2. Resolve accounts
        ids = UserResolver.resolve(user_name)
        if not ids:
            return success(
                message=f"No accountId configured for '{user_name}'.",
                items={},
                meta={}
            )

        jira_id = ids["jira"]
        github_username = ids["github"]

        # 3. Determine intent
        intent = IntentService.detect_intent(question)
        period = PeriodParser.detect_period(question)

        # 4. Fetch raw data once
        jira_data = self.jira.get_user_issues(jira_id, limit, offset)
        github_data = self.github.get_user_github_activity(
            github_username,
            limit,
            offset,
            period,
        )

        # 5. Generate summary (deterministic)
        summary_text = self.summarizer.generate(user_name, jira_data, github_data)

        # 6. Intent → Response builder mapping
        intent_builders = {
            "JIRA_ISSUES": lambda: self._build_jira_items(jira_data),
            "GITHUB_COMMITS": lambda: self._build_github_commits_items(github_data),
            "GITHUB_PRS": lambda: self._build_github_prs_items(github_data),
            "GITHUB_REPOS": lambda: self._build_github_repos_items(github_data),
        }

        # 7. Pick builder
        items = intent_builders.get(
            intent,
            lambda: self._build_full_activity_items(jira_data, github_data, summary_text)
        )()

        # 8. Top-level message
        top_message = self._intent_message(intent, user_name)

        # 9. Final unified response
        return success(
            message=top_message,
            items=items,
            meta={"limit": limit, "offset": offset}
        )
