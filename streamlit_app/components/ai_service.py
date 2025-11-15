from .ai_client import AIClient


class AIService:
    """Streamlit-only AI service."""

    def __init__(self):
        self.ai = AIClient()

    # Natural insight summary (your main requirement)
    def generate_insights_from_json(self, data: dict) -> str:
        """
        Feed backend JSON (jira, github, summary...) and get a
        clean, meaningful natural-language insight summary.
        """

        prompt = f"""
        You generate concise natural-language insights.

        STRICT RULES:
        - Only mention sections that are present and non-empty in the JSON.
        - DO NOT mention JIRA if there is no JIRA data or total = 0.
        - DO NOT mention GitHub commits/PRs/repos if they are empty or missing.
        - DO NOT guess or invent activity.
        - Keep output 4–6 short sentences.
        - Write like a professional status insight.

        Example:
          If only JIRA exists → mention only JIRA.
          If only GitHub commits exist → mention only commits.
          If both exist → mention both.
          If PRs = 0 → DO NOT mention PRs.
          If repos = 0 → DO NOT mention repos.

        Data:
        {data}

        Now write the summary:
        """

        return self.ai.generate_insight(prompt)

    # Optional: bullet-style summary (super short)
    def generate_bullet_summary(self, data: dict) -> str:
        """
        Very short 3–5 bullet summary of high-level activity.
        """
        prompt = f"""
        Create a 3–5 bullet summary of the following activity.
        Follow rules:
        - Max 1 line per bullet
        - Use simple emojis
        - No timestamps
        - Summarize only counts

        Data:
        {data}
        """

        return self.ai.generate_bullet_summary(prompt)
