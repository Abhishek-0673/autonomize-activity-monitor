from typing import Optional

from src.core.config import settings


class UserResolver:
    """
    Resolves natural language names into JIRA account IDs.
    """
    NAME_MAP = {
        "abhishek": settings.jira_abhishek_account_id,
        "abhialien": settings.jira_abhialien_account_id,
        "test": settings.jira_test_account_id,
    }

    @classmethod
    def resolve(cls, name: str) -> Optional[str]:
        name = name.lower().strip()
        return cls.NAME_MAP.get(name)

    @classmethod
    def resolve_reverse(cls, account_id: str) -> Optional[str]:
        # Reverse lookup: accountId → name
        for name, acc_id in cls.NAME_MAP.items():
            if acc_id == account_id:
                return name.capitalize()
        return None