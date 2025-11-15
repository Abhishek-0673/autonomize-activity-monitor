from datetime import datetime

import streamlit as st
from components.chat_ui import user_message, bot_message
from components.api_client import cached_backend, cached_ai_insights


st.set_page_config(page_title="Autonomize Activity Chat", page_icon="🤖")

st.title("🤖 Autonomize Activity Assistant")
st.markdown("Ask anything about JIRA, GitHub, or team activity!")

# Session State Setup
if "chat" not in st.session_state:
    st.session_state.chat = []

if "pending_input" not in st.session_state:
    st.session_state.pending_input = ""


# BACKEND + AI combined handler
def handle_message(msg: str):
    msg = msg.strip()
    if not msg:
        return

    timestamp = datetime.now().strftime("%I:%M %p")   # Example: 09:44 AM

    st.session_state.chat.append(("user", msg, timestamp))

    with st.spinner("Analyzing…"):
        payload, error = cached_backend(msg)

        if error:
            st.session_state.chat.append(("bot", f"⚠️ {error}", timestamp))
            return

        insights = cached_ai_insights(payload)

    bot_timestamp = datetime.now().strftime("%I:%M %p")
    st.session_state.chat.append(("bot", insights, bot_timestamp))


# Callback for Enter key
def on_enter_pressed():
    msg = st.session_state.pending_input.strip()
    if not msg:
        return

    handle_message(msg)

    # Allowed because callback runs BEFORE UI rerender
    st.session_state.pending_input = ""


# RENDER CHAT
for role, msg, ts in st.session_state.chat:
    if role == "user":
        user_message(msg, ts)
    else:
        bot_message(msg, ts)


# WhatsApp-like Input Bar
col1, col2, col3 = st.columns([1, 8, 1])

with col1:
    st.button("🔐")

with col3:
    send_btn = st.button("➜",  type="tertiary", help="Send")

with col2:
    st.text_input(
        "Message",
        key="pending_input",
        placeholder="Type a message…",
        on_change=on_enter_pressed,
        label_visibility="collapsed"
    )


# SEND BUTTON HANDLER
if send_btn:
    on_enter_pressed()
