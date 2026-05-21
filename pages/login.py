"""
pages/login.py — Trang đăng nhập (centered, clean, no demo buttons, no HTML leak)
"""
import streamlit as st
import os


def _load_css():
    css_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "style.css")
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


ACCOUNTS = {
    "admin@health.ai":   "health2024",
    "doctor@health.ai":  "doctor123",
    "patient@health.ai": "patient123",
}


def show():
    _load_css()

    # Extra page-level overrides: full-height centering, lighter bg
    st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] {
        background:
            radial-gradient(ellipse at 25% 25%, rgba(10,191,188,0.07) 0%, transparent 45%),
            radial-gradient(ellipse at 80% 75%, rgba(228,185,91,0.04) 0%, transparent 45%),
            #132038 !important;
    }
    /* Hide block padding so we can center manually */
    section.main > div.block-container { padding: 0 !important; }
    </style>
    """, unsafe_allow_html=True)

    # ── Full-height centering wrapper ─────────────────────────────────────
    # We use a narrow single column to keep the card in the middle
    _, center, _ = st.columns([1, 1.4, 1])

    with center:
        st.markdown("<div style='height:60px'></div>", unsafe_allow_html=True)

        # ── Logo / brand ──────────────────────────────────────────────────
        st.markdown("""
        <div style="text-align:center; margin-bottom:32px;">
            <div style="font-size:52px; margin-bottom:10px;">🏥</div>
            <div style="font-family:'Playfair Display',serif; font-size:26px;
                 color:#eef2f7; font-weight:700;">HealthAI Portal</div>
            <div style="font-size:13px; color:#7a93b4; margin-top:6px;">
                Hệ thống dự đoán tiểu đường thông minh
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ── Card wrapper ──────────────────────────────────────────────────
        st.markdown("""
        <div style="background:#1a2e4a; border:1.5px solid rgba(10,191,188,0.20);
             border-radius:20px; padding:36px 32px 28px;
             box-shadow:0 16px 48px rgba(0,0,0,0.35);">
        </div>
        """, unsafe_allow_html=True)

        # ── Form fields (Streamlit widgets) ───────────────────────────────
        st.markdown("""
        <div style="background:#1a2e4a; border:1.5px solid rgba(10,191,188,0.20);
             border-radius:20px; padding:36px 32px 28px;
             box-shadow:0 16px 48px rgba(0,0,0,0.35);">
            <p style="font-size:13px; color:#7a93b4; margin-bottom:20px; text-align:center;">
                Vui lòng đăng nhập để tiếp tục
            </p>
        </div>
        """, unsafe_allow_html=True)

        email    = st.text_input("Email", placeholder="doctor@health.ai", key="login_email",
                                  label_visibility="collapsed")
        st.markdown('<p style="font-size:12px;color:#7a93b4;margin:-8px 0 12px 2px;">📧 Email / Tên đăng nhập</p>',
                    unsafe_allow_html=True)

        password = st.text_input("Mật khẩu", type="password", placeholder="Nhập mật khẩu",
                                  key="login_password", label_visibility="collapsed")
        st.markdown('<p style="font-size:12px;color:#7a93b4;margin:-8px 0 16px 2px;">🔑 Mật khẩu</p>',
                    unsafe_allow_html=True)

        st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
        btn = st.button("🚀  Đăng nhập", type="primary", use_container_width=True, key="btn_login")

        # Error placeholder
        err_spot = st.empty()

        st.markdown("""
        <p style="text-align:center; font-size:12px; color:#7a93b4; margin-top:20px;">
            Chưa có tài khoản?
            <span style="color:#0abfbc;">Liên hệ quản trị viên</span>
        </p>
        """, unsafe_allow_html=True)

        st.markdown("<div style='height:60px'></div>", unsafe_allow_html=True)

        # ── Auth logic ────────────────────────────────────────────────────
        if btn:
            e = email.strip()
            p = password
            if not e or not p:
                err_spot.error("Vui lòng nhập đầy đủ email và mật khẩu.")
            elif ACCOUNTS.get(e) == p:
                st.session_state["logged_in"]  = True
                st.session_state["user_email"] = e
                st.session_state["user_name"]  = e.split("@")[0].capitalize()
                st.session_state["page"]       = "home"
                st.rerun()
            else:
                err_spot.error("❌ Email hoặc mật khẩu không đúng.")
