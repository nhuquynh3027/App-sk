"""
pages/login.py — Trang đăng nhập
"""
import streamlit as st


def _load_css():
    import os
    css_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "style.css")
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


DEMO_ACCOUNTS = {
    "admin@health.ai":   "health2024",
    "doctor@health.ai":  "doctor123",
    "patient@health.ai": "patient123",
}


def show():
    _load_css()

    # Full-page background with geometric shapes
    st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] {
        background: radial-gradient(ellipse at 30% 20%, rgba(10,191,188,0.08) 0%, transparent 50%),
                    radial-gradient(ellipse at 80% 80%, rgba(228,185,91,0.05) 0%, transparent 50%),
                    #0b1628 !important;
    }
    /* Center the login vertically */
    .login-outer {
        min-height: 100vh;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 40px 16px;
    }
    </style>
    """, unsafe_allow_html=True)

    # Decorative floating blobs
    st.markdown("""
    <div style="position:fixed;top:80px;left:80px;width:260px;height:260px;
         border-radius:50%;background:radial-gradient(circle,rgba(10,191,188,0.06),transparent 70%);
         pointer-events:none;"></div>
    <div style="position:fixed;bottom:100px;right:100px;width:320px;height:320px;
         border-radius:50%;background:radial-gradient(circle,rgba(228,185,91,0.05),transparent 70%);
         pointer-events:none;"></div>
    """, unsafe_allow_html=True)

    # ---- Two-column layout: left branding, right form ----
    left, _, right = st.columns([5, 1, 4])

    with left:
        st.markdown("""
        <div style="padding: 60px 20px 40px; max-width: 480px;">
            <div style="
                display:inline-flex; align-items:center; gap:8px;
                background:rgba(10,191,188,0.10); border:1px solid rgba(10,191,188,0.25);
                border-radius:999px; padding:6px 16px; font-size:12px;
                color:#0abfbc; font-weight:600; letter-spacing:0.08em;
                text-transform:uppercase; margin-bottom:28px;">
                ✦ AI-Powered Health Platform
            </div>
            <h1 style="font-family:'Playfair Display',serif;font-size:clamp(32px,4vw,52px);
                font-weight:700;line-height:1.18;color:#f5f7fa;margin-bottom:20px;">
                Hệ Thống<br>
                <span style="color:#0abfbc;">Dự Đoán</span><br>
                Tiểu Đường AI
            </h1>
            <p style="font-size:15px;color:#8fa3c0;line-height:1.7;margin-bottom:36px;max-width:400px;">
                Ứng dụng mạng nơ-ron tiên tiến để phân tích nguy cơ tiểu đường và 
                đưa ra tư vấn sức khỏe cá nhân hóa theo tiêu chuẩn lâm sàng.
            </p>

            <!-- Stats row -->
            <div style="display:flex; gap:24px; flex-wrap:wrap;">
                <div style="text-align:center;">
                    <div style="font-family:'Playfair Display',serif;font-size:28px;color:#0abfbc;font-weight:700;">94%</div>
                    <div style="font-size:12px;color:#8fa3c0;margin-top:2px;">Độ chính xác mô hình</div>
                </div>
                <div style="width:1px;background:rgba(10,191,188,0.2);"></div>
                <div style="text-align:center;">
                    <div style="font-family:'Playfair Display',serif;font-size:28px;color:#e4b95b;font-weight:700;">8</div>
                    <div style="font-size:12px;color:#8fa3c0;margin-top:2px;">Chỉ số lâm sàng</div>
                </div>
                <div style="width:1px;background:rgba(10,191,188,0.2);"></div>
                <div style="text-align:center;">
                    <div style="font-family:'Playfair Display',serif;font-size:28px;color:#e05c6e;font-weight:700;">3s</div>
                    <div style="font-size:12px;color:#8fa3c0;margin-top:2px;">Thời gian phân tích</div>
                </div>
            </div>

            <!-- Visual grid of health icons -->
            <div style="margin-top:48px; display:grid; grid-template-columns:repeat(3,1fr); gap:12px; max-width:300px;">
                {icons}
            </div>
        </div>
        """.format(icons="".join([
            f"""<div style="background:rgba(17,34,64,0.8);border:1px solid rgba(10,191,188,0.12);
                border-radius:12px;padding:14px;text-align:center;font-size:22px;">{icon}</div>"""
            for icon in ["🫀","🩺","💉","🧬","🏥","📊","⚕️","🔬","📈"]
        ])), unsafe_allow_html=True)

    with right:
        st.markdown("<div style='padding:40px 0;'>", unsafe_allow_html=True)

        # Login card
        st.markdown("""
        <div class="login-card">
            <div class="login-logo">
                <span class="login-logo-icon">🏥</span>
                <div class="login-logo-title">HealthAI Portal</div>
                <div class="login-logo-sub">Đăng nhập để tiếp tục</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Form (Streamlit widgets can't be inside arbitrary HTML, so render below)
        with st.container():
            st.markdown("""
            <div style="background:rgba(17,34,64,0.70);border:1px solid rgba(10,191,188,0.18);
                 border-radius:24px;padding:36px 32px;backdrop-filter:blur(16px);">
            </div>""", unsafe_allow_html=True)

            email    = st.text_input("📧  Email / Tên đăng nhập", placeholder="doctor@health.ai", key="login_email")
            password = st.text_input("🔑  Mật khẩu", type="password", placeholder="••••••••", key="login_password")

            remember = st.checkbox("Ghi nhớ đăng nhập", value=True)

            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

            btn_login = st.button("🚀  Đăng nhập", type="primary", use_container_width=True)

            st.markdown("""
            <div class="login-divider">HOẶC DÙNG TÀI KHOẢN DEMO</div>
            """, unsafe_allow_html=True)

            col_a, col_b = st.columns(2)
            with col_a:
                demo_doc = st.button("👨‍⚕️ Bác sĩ Demo", use_container_width=True)
            with col_b:
                demo_pat = st.button("🧑 Bệnh nhân Demo", use_container_width=True)

            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
            st.markdown("""<p style="text-align:center;font-size:12px;color:#8fa3c0;">
                Chưa có tài khoản? <span style="color:#0abfbc;cursor:pointer;">Liên hệ quản trị viên</span>
            </p>""", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

        # ---- Handle login logic ----
        def do_login(email_val, pass_val, name):
            if DEMO_ACCOUNTS.get(email_val) == pass_val:
                st.session_state["logged_in"]   = True
                st.session_state["user_email"]  = email_val
                st.session_state["user_name"]   = name
                st.session_state["page"]        = "home"
                st.rerun()
            else:
                st.error("❌ Email hoặc mật khẩu không đúng. Vui lòng thử lại.")

        if btn_login:
            do_login(email.strip(), password, email.split("@")[0].capitalize())

        if demo_doc:
            do_login("doctor@health.ai", "doctor123", "Bác sĩ Nguyễn")

        if demo_pat:
            do_login("patient@health.ai", "patient123", "Bệnh nhân Demo")
