from src.integrations.ai_client import AIClient


class AIService:
    def __init__(self):
        self.ai = AIClient()

    def generate_activity_summary(self, user: str, jira: dict, github: dict):
        prompt = f"""
        Summarize this activity for user: {user}
        
        JIRA Issues:
        {jira}
        
        GitHub Activity:
        {github}
        
        Write a short natural language summary.
        """

        return self.ai.generate_answer(prompt)
