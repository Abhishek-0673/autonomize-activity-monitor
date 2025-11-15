import os
import openai


def log_err(msg: str):
    print(f"[AIClient] ERROR: {msg}")


class AIClient:
    """Minimal AI client for Streamlit frontend."""

    def __init__(self):
        key = os.getenv("OPENAI_API_KEY")
        if not key:
            log_err("OPENAI_API_KEY not set.")
        openai.api_key = key

    # Generic insight generator (paragraph-style)
    def generate_insight(self, prompt: str) -> str:
        try:
            resp = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=250,
            )
            return resp.choices[0].message.content

        except Exception as e:
            log_err(e)
            return "⚠️ Unable to generate insights."

    # High-level bullet summary (optional)
    def generate_bullet_summary(self, prompt: str) -> str:
        try:
            resp = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You write extremely short bullet summaries."},
                    {"role": "user", "content": prompt},
                ],
                max_tokens=150,
            )
            return resp.choices[0].message.content

        except Exception as e:
            log_err(e)
            return "⚠️ Summary unavailable."
