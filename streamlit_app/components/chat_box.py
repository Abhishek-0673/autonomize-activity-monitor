import streamlit as st
from datetime import datetime
from .message_bubble import user_bubble, bot_bubble
from .api_client import ask_backend

def init_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []

def append_message(role, text):
    st.session_state.messages.append(
        {
            "role": role,
            "text": text,
            "time": datetime.now().strftime("%H:%M")
        }
    )

def render_chat():
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            user_bubble(msg["text"], msg["time"])
        else:
            bot_bubble(msg["text"], msg["time"])

def chat_input_box():
    user_input = st.chat_input("Ask about a team member...")

    if user_input:
        append_message("user", user_input)

        reply, error = ask_backend(user_input)
        if error:
            append_message("bot", f"⚠️ {error}")
        else:
            append_message("bot", reply)

        st.rerun()
