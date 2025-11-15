import re
from typing import Optional

from src.core.user_resolver import UserResolver

class QueryParserService:
    """
    Extracts user names from natural questions like:
    'What is Abhishek working on these days?'
    """
    @staticmethod
    def extract_user(question: str) -> Optional[str]:
        # Basic: split by space + look for known names
        words = re.findall(r"[A-Za-z]+", question.lower())

        for w in words:
            if UserResolver.resolve(w):
                return w

        return None

if __name__ == "__main__":
    print(QueryParserService.extract_user("What is Abhishek working on these days?"))