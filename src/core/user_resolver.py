from typing import Optional

from src.core.config import settings


class UserResolver:
    """
    Resolves natural language names into JIRA account IDs.
    """
    MAP = {
        "abhishek": {
            "jira": settings.jira_abhishek_account_id,
            "github": settings.github_username_for_abhishek
        },
        "abhialien": {
            "jira": settings.jira_abhialien_account_id,
            "github": settings.github_username_for_abhialien
        }
    }

    @staticmethod
    def resolve(name: str):
        """Resolve a natural language name into a JIRA account ID."""
        key = name.lower()
        return UserResolver.MAP.get(key)

    @staticmethod
    def resolve_reverse(jira_id: str):
        """Resolve a JIRA account ID into a natural language name."""
        for name, ids in UserResolver.MAP.items():
            if ids["jira"] == jira_id:
                return name
        return None