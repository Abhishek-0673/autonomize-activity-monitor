import hashlib

import requests
import os
import streamlit as st
from .ai_service import AIService

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

ai_service = AIService()


def ask_backend(question: str):
    """Call backend → generate insights → return final text."""
    try:
        res = requests.post(
            f"{BACKEND_URL}/activity",
            json={"question": question},
            timeout=10
        )

        if res.status_code != 200:
            return None, f"Server error: {res.text}"

        data = res.json()

        if not data.get("success"):
            return None, data.get("message", "Unknown error")

        # Extract items (jira/github/summary)
        items = data.get("data", {}).get("items", {})

        # Generate AI insights
        insights = ai_service.generate_insights_from_json(items)

        # Final output returned to the UI
        final_text = f"""
                    ### Insights
                    {insights}
                    """

        return final_text, None

    except Exception as e:
        return None, str(e)

@st.cache_data(show_spinner=False)
def cached_backend(question: str):
    return ask_backend(question)

@st.cache_data(show_spinner=False)
def cached_ai_insights(json_payload: dict):
    key = hashlib.md5(str(json_payload).encode()).hexdigest()
    return ai_service.generate_insights_from_json(json_payload)