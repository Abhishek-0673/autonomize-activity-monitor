class IntentService:

    INTENT_KEYWORDS = {
        "JIRA_ISSUES": ["assigned", "ticket", "tickets", "issue", "issues"],
        "GITHUB_COMMITS": ["commit", "commits"],
        "GITHUB_PRS": ["pull", "pulls", "pr", "pull request", "pull requests"],
        "GITHUB_REPOS": ["repo", "repos", "contributed", "contributions"],
    }

    @staticmethod
    def detect_intent(question: str) -> str:
        q = question.lower()

        # Dictionary-based intent scan
        for intent, keywords in IntentService.INTENT_KEYWORDS.items():
            if any(keyword in q for keyword in keywords):
                return intent

        return "FUSION"  # default fallback
