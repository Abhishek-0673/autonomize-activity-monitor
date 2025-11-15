from src.services.activity_summary_service import ActivitySummaryService
from src.services.jira_service import JiraService
from src.services.github_service import GitHubService
from src.services.query_parser_service import QueryParserService
from src.services.intent_service import IntentService
from src.core.user_resolver import UserResolver


class ActivityService:
    def __init__(self):
        self.jira = JiraService()
        self.github = GitHubService()
        # You can use AI Summarizer here too.
        self.summarizer = ActivitySummaryService()

    def get_activity(self, question: str, limit: int = 5, offset: int = 0):

        # 1. Extract user
        user_name = QueryParserService.extract_user(question)
        if not user_name:
            return {"error": "Could not identify the user from your question."}

        # 2. Resolve accounts
        ids = UserResolver.resolve(user_name)
        if not ids:
            return {"error": f"No accountId configured for '{user_name}'"}

        jira_id = ids["jira"]
        github_username = ids["github"]

        # 3. Detect intent
        intent = IntentService.detect_intent(question)

        # 4. Fetch JIRA & GitHub (always fetch both so summary is accurate)
        jira_data = self.jira.get_user_issues(jira_id, limit, offset)
        github_data = self.github.get_user_github_activity(github_username, limit, offset)

        # 5. Prepare summary (always use deterministic summarizer)
        summary_text = self.summarizer.generate(user_name, jira_data, github_data)

        # 6. Intent Routing — include github in every response to avoid surprises
        intent_map = {
            "JIRA_ISSUES": lambda: {
                "user": user_name,
                "jira": jira_data,
                "github": github_data,  # <-- include github here
                "summary": summary_text
            },
            "GITHUB_COMMITS": lambda: {
                "user": user_name,
                "commits": github_data.get("commits"),
                "github": github_data,
                "summary": summary_text
            },
            "GITHUB_PRS": lambda: {
                "user": user_name,
                "prs": github_data.get("prs"),
                "github": github_data,
                "summary": summary_text
            },
            "GITHUB_REPOS": lambda: {
                "user": user_name,
                "recent_repos": github_data.get("recent_repos"),
                "github": github_data,
                "summary": summary_text
            },
        }

        if intent in intent_map:
            return intent_map[intent]()

        # 7. Default: Full fusion
        return {
            "user": user_name,
            "jira": jira_data,
            "github": github_data,
            "summary": summary_text,
        }
