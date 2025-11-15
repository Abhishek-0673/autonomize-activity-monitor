import re


class PeriodParser:

    PERIOD_PATTERNS = {
        "today": r"\btoday\b",
        "yesterday": r"\byesterday\b",
        "this_week": r"\bthis week\b",
        "last_week": r"\blast week\b",
        "this_month": r"\bthis month\b",
        "last_month": r"\blast month\b",
    }

    @staticmethod
    def detect_period(text: str) -> str:
        text = text.lower()

        for period, pattern in PeriodParser.PERIOD_PATTERNS.items():
            if re.search(pattern, text):
                return period

        return "default"
