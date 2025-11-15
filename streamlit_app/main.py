import streamlit as st
from components.chat_ui import user_message, bot_message, info_card
from components.api_client import cached_backend, cached_ai_insights


st.set_page_config(page_title="Autonomize Activity Chat", page_icon="🤖")

st.title("🤖 Autonomize Activity Assistant")
st.markdown("Ask about team activity, JIRA, or GitHub!")

# Chat history
if "chat" not in st.session_state:
    st.session_state.chat = []


def process_message():
    message = st.session_state.input_box.strip()
    if not message:
        return

    # Add user message (no UI rendering here)
    st.session_state.chat.append(("user", message))
    st.session_state.input_box = ""

    # Call backend + AI
    with st.spinner("Analyzing…"):
        payload, error = cached_backend(message)

        if error:
            st.session_state.chat.append(("bot", f"⚠️ {error}"))
            return

        insights = cached_ai_insights(payload)

    # Add bot message to chat
    st.session_state.chat.append(("bot", insights))



# Render chat history
for role, msg in st.session_state.chat:
    if role == "user":
        user_message(msg)
    else:
        bot_message(msg)

# Input box
st.text_input("Message:", key="input_box", on_change=process_message)
