from abc import ABC, abstractmethod

class BaseClient(ABC):
    """Abstract base class for all external API clients."""

    @abstractmethod
    def get_user_activity(self, username: str) -> dict:
        """Fetch activity for a given username."""
        pass
