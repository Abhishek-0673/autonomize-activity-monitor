import re
from src.integrations.ai_client import AIClient

class IntentService:
    """
    NLP-driven + AI-fallback intent classifier.
    """

    # Classic keyword-based map
    INTENT_PATTERNS = {
        "JIRA_ISSUES": [
            r"jira", r"issue", r"ticket", r"assigned", r"working on",
        ],
        "GITHUB_COMMITS": [
            r"commit", r"code pushed", r"recent commits", r"pushed",
        ],
        "GITHUB_PRS": [
            r"pull request", r"pr", r"merge request",
        ],
        "GITHUB_REPOS": [
            r"repo", r"repositories", r"activity repos",
        ],
    }

    @staticmethod
    def detect_intent(text: str) -> str:
        """Detect intent based on keyword patterns and AI."""
        text_lower = text.lower()

        # Step 1 — Classic keyword matching
        for intent, patterns in IntentService.INTENT_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, text_lower):
                    return intent

        # Step 2 — AI fallback (when ambiguous)
        ai = AIClient()
        ai_intent = ai.classify_intent(text)

        return ai_intent or "FULL_ACTIVITY"
