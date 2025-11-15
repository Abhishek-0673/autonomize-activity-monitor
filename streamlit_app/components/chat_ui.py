import streamlit as st


def user_message(text, timestamp):
    st.markdown(
        f"""
        <div style="
            background-color:#DCF8C6;
            padding:10px 15px;
            border-radius:10px;
            margin:5px 0;
            max-width:80%;
            float:right;
            clear:both;
            font-size:14px;
            position: relative;
        ">
            <div>{text}</div>
            <div style="font-size:11px; color:#555; text-align:right; margin-top:4px;">
                {timestamp}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


def bot_message(text, timestamp):
    st.markdown(
        f"""
        <div style="
            background-color:#F1F0F0;
            padding:10px 15px;
            border-radius:10px;
            margin:5px 0;
            max-width:80%;
            float:left;
            clear:both;
            font-size:14px;
        ">
            <div>{text}</div>
            <div style="font-size:11px; color:#777; text-align:right; margin-top:4px;">
                {timestamp}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

def info_card(title: str, body: str):
    st.markdown(
        f"""
        <div style="
            background: white;
            border-radius: 12px;
            padding: 16px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.1);
            margin: 10px 0;
        ">
            <h4 style="margin-bottom:8px;">{title}</h4>
            <div style="font-size:14px; line-height:1.5;">
                {body}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
