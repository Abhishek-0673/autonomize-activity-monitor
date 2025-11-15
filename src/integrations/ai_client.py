import openai
from src.core.logger import get_logger
from src.core.config import settings

logger = get_logger(__name__)


class AIClient:
    def __init__(self):
        openai.api_key = settings.openai_api_key

    def classify_intent(self, text: str) -> str:
            """
            Use AI to classify user intent when keyword rules fail.
            """

            prompt = f"""
            Classify the user's question into one of the following intents:
        
            - JIRA_ISSUES
            - GITHUB_COMMITS
            - GITHUB_PRS
            - GITHUB_REPOS
            - FULL_ACTIVITY
        
            Return ONLY the intent name.
        
            Question:
            {text}
            """

            try:
                resp = openai.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=5,
                )

                return resp.choices[0].message.content.strip()

            except:
                return "FULL_ACTIVITY"

    def generate_summary(self, user: str, jira_data: dict, github_data: dict) -> str:
        """
        Generates extremely short, safe, bullet-point summary.
        """

        prompt = f"""
        You generate extremely short bullet summaries for workload/activity.
        
        STRICT RULES:
        - Keep summary under 4–5 bullet points.
        - Bullets must be very short — max 1 line each.
        - Use simple emojis (1 per bullet).
        - NO repo names, NO commit messages, NO descriptions.
        - NO dates, NO timestamps.
        - NO sensitive details of any kind.
        - Only summarize counts and high-level activity.
        
        Example output format:
        🧩 JIRA: 3 issues
        💻 Commits: 5
        📂 PRs: 1
        📦 Repos active: 2
        
        Data:
        JIRA: {jira_data}
        GitHub: {github_data}
        
        Now generate summary for user: {user}
        """

        try:
            response = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You generate extremely short and safe summaries."},
                    {"role": "user", "content": prompt},
                ],
                max_tokens=150,
            )

            return response.choices[0].message.content

        except Exception as e:
            logger.error(f"AI summary generation failed: {e}")
            return "⚠️ AI summary unavailable."
