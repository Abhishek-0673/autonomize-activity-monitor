import json

import streamlit as st


def load_css():
    with open("styles/chat.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def user_bubble(text, time):
    st.markdown(
        f"""
        <div style="text-align:right; margin:8px;">
            <div style="
                display:inline-block;
                background:#DCF8C6;
                padding:10px 14px;
                border-radius:12px;
                max-width:70%;
            ">{text}</div><br>
            <span style="font-size:10px; color:gray;">{time}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

def bot_bubble(text, time):
    st.markdown(
        f"""
        <div style="text-align:left; margin:8px;">
            <div style="
                display:inline-block;
                background:#E8E8E8;
                padding:10px 14px;
                border-radius:12px;
                max-width:70%;
            ">{json.loads(json.dumps(text, indent=2))}</div><br>
            <span style="font-size:10px; color:gray;">{time}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
