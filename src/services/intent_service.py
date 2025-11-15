import re
from src.integrations.ai_client import AIClient


class IntentService:
    """
    Production-grade intent classifier.
    Priority order:
        1) Explicit source keywords (JIRA/Github)
        2) Full-activity phrases (ONLY if no explicit source mentioned)
        3) Keyword rules
        4) AI fallback
        5) Default = FULL_ACTIVITY
    """

    # --- Explicit source keywords (strongest signal) ---
    JIRA_KEYWORDS = ["jira", "ticket", "issue", "assigned"]
    GITHUB_KEYWORDS = ["commit", "commits", "pr", "pull request",
                       "repo", "repository", "repositories", "pushed"]

    # --- Traditional keyword-based rules ---
    INTENT_PATTERNS = {
        "JIRA_ISSUES": [
            r"\bjira\b", r"\bticket\b", r"\bissue\b", r"\bassigned\b"
        ],
        "GITHUB_COMMITS": [
            r"\bcommit\b", r"recent commits", r"\bpushed\b"
        ],
        "GITHUB_PRS": [
            r"\bpull request\b", r"\bpr\b", r"merge request"
        ],
        "GITHUB_REPOS": [
            r"\brepo\b", r"repositories", r"recent repos"
        ],
    }

    # --- These phrases imply "give me the overall activity",
    #     but ONLY when user does NOT mention JIRA or GitHub explicitly
    FULL_ACTIVITY_PHRASES = [
        r"working on",
        r"what.*doing",
        r"activity",
        r"status",
        r"update",
        r"progress",
        r"summary",
    ]

    @staticmethod
    def _contains_any(text: str, keywords: list[str]) -> bool:
        return any(k in text for k in keywords)

    @staticmethod
    def detect_intent(text: str) -> str:
        """Determine intent with layered logic."""
        if not text:
            return "FULL_ACTIVITY"

        text_lower = text.lower()

        # -----------------------------------------
        # STEP 1 — Strongest signal: explicit source
        # -----------------------------------------
        explicit_jira = IntentService._contains_any(text_lower, IntentService.JIRA_KEYWORDS)
        explicit_github = IntentService._contains_any(text_lower, IntentService.GITHUB_KEYWORDS)

        if explicit_jira and not explicit_github:
            return "JIRA_ISSUES"
        if explicit_github and not explicit_jira:
            # We still need pattern matching to map to commits/PRs/repos
            # but we know it's GitHub-only intent
            pass  # continue to normal keyword evaluation

        # -----------------------------------------
        # STEP 2 — Full activity override,
        #          but ONLY if no explicit source was mentioned
        # -----------------------------------------
        if not explicit_jira and not explicit_github:
            for phrase in IntentService.FULL_ACTIVITY_PHRASES:
                if re.search(phrase, text_lower):
                    return "FULL_ACTIVITY"

        # -----------------------------------------
        # STEP 3 — Keyword rule-based matching
        # -----------------------------------------
        for intent, patterns in IntentService.INTENT_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, text_lower):
                    return intent

        # -----------------------------------------
        # STEP 4 — AI fallback (ambiguous queries)
        # -----------------------------------------
        try:
            ai = AIClient()
            ai_intent = ai.classify_intent(text)
            if ai_intent:
                return ai_intent
        except Exception:
            pass

        # -----------------------------------------
        # STEP 5 — Safe default
        # -----------------------------------------
        return "FULL_ACTIVITY"
