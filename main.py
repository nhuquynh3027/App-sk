"""
main.py — Entry point cho ứng dụng HealthAI Diabetes
Chạy: streamlit run main.py
"""

import streamlit as st

st.set_page_config(
    page_title="HealthAI — Dự Đoán Tiểu Đường",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
[data-testid="stSidebar"] { display: none !important; }
[data-testid="collapsedControl"] { display: none !important; }
</style>
""", unsafe_allow_html=True)

from pages import login, home, predict

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "page" not in st.session_state:
    st.session_state["page"] = "login"

page = st.session_state["page"]

if not st.session_state["logged_in"]:
    login.show()
elif page == "home":
    home.show()
elif page == "predict":
    predict.show()
else:
    home.show()
