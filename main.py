"""
main.py — Entry point cho ứng dụng HealthAI Diabetes
Chạy: streamlit run main.py

Cấu trúc thư mục:
  main.py
  assets/
    style.css
    anh_1.jpg  ← (tuỳ chọn) thêm ảnh thực vào đây
    anh_2.jpg
    ...
  models/
    diabetes_model.h5
    scaler.pkl
  pages/
    login.py
    home.py
    predict.py
"""

import streamlit as st

# ── Page config phải gọi đầu tiên ──────────────────────────────────────────
st.set_page_config(
    page_title="HealthAI — Dự Đoán Tiểu Đường",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Ẩn sidebar mặc định của Streamlit ──────────────────────────────────────
st.markdown("""
<style>
[data-testid="stSidebar"] { display: none !important; }
[data-testid="collapsedControl"] { display: none !important; }
</style>
""", unsafe_allow_html=True)

# ── Import các trang (sau set_page_config) ──────────────────────────────────
from pages import login, home, predict

# ── Session state defaults ─────────────────────────────────────────────────
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "page" not in st.session_state:
    st.session_state["page"] = "login"

# ── Router ──────────────────────────────────────────────────────────────────
page = st.session_state["page"]

if not st.session_state["logged_in"]:
    login.show()
elif page == "home":
    home.show()
elif page == "predict":
    predict.show()
else:
    home.show()
