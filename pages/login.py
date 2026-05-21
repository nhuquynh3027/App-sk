"""
pages/login.py — Đăng nhập & Đăng ký, giao diện sáng sạch
"""
import streamlit as st
import os


def _load_css():
    css_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "style.css")
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# Tài khoản mặc định
DEFAULT_ACCOUNTS = {
    "tonngokhong@health.ai":   {"password": "tonngokhong", "name": "Tôn Ngộ Không"},
    "trubacgioi@health.ai":  {"password": "trubatgioi",  "name": "Trư Bát Giới"},
    "duongtang@health.ai": {"password": "duongtang123", "name": "Đường Tăng"},
    "satang@health.ai": {"password": "satang123", "name": "Sa Tăng"},
}


def _get_accounts():
    if "registered_accounts" not in st.session_state:
        st.session_state["registered_accounts"] = {}
    merged = {**DEFAULT_ACCOUNTS, **st.session_state["registered_accounts"]}
    return merged


def show():
    _load_css()

    st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #e0f2fe 0%, #f0fdf4 50%, #e0f2fe 100%) !important;
    }
    section.main > div.block-container { padding: 0 !important; }
    
    /* Style cho input đẹp hơn */
    .stTextInput > div > div > input {
        border-radius: 12px !important;
        border: 1.5px solid #e2e8f0 !important;
        padding: 10px 14px !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: #0ea5e9 !important;
        box-shadow: 0 0 0 2px rgba(14,165,233,0.2) !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # Decorative top bar
    st.markdown("""
    <div style="height:4px;background:linear-gradient(90deg,#0ea5e9,#10b981,#0ea5e9);width:100%;"></div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:48px'></div>", unsafe_allow_html=True)

    _, center, _ = st.columns([1, 1.6, 1])

    with center:
        # Logo
        st.markdown("""
        <div style="text-align:center; margin-bottom:28px;">
            <div style="display:inline-flex;align-items:center;justify-content:center;
                 width:72px;height:72px;border-radius:20px;
                 background:linear-gradient(135deg,#0ea5e9,#10b981);
                 box-shadow:0 8px 24px rgba(14,165,233,0.30);margin-bottom:14px;">
                <span style="font-size:34px;">🏥</span>
            </div>
            <div style="font-family:'Lora',serif;font-size:26px;color:#0f172a;font-weight:700;">
                HealthAI Portal
            </div>
            <div style="font-size:13px;color:#64748b;margin-top:6px;">
                Hệ thống dự đoán tiểu đường thông minh
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Tab chooser
        if "auth_tab" not in st.session_state:
            st.session_state["auth_tab"] = "login"

        tab_login, tab_register = st.columns(2)
        with tab_login:
            active_l = st.session_state["auth_tab"] == "login"
            if st.button("🔑  Đăng nhập", use_container_width=True,
                         type="primary" if active_l else "secondary", key="tab_login_btn"):
                st.session_state["auth_tab"] = "login"
                st.rerun()
        with tab_register:
            active_r = st.session_state["auth_tab"] == "register"
            if st.button("✏️  Đăng ký", use_container_width=True,
                         type="primary" if active_r else "secondary", key="tab_register_btn"):
                st.session_state["auth_tab"] = "register"
                st.rerun()

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

        err_spot = st.empty()
        ok_spot = st.empty()

        # ĐĂNG NHẬP
        if st.session_state["auth_tab"] == "login":
            # Dòng chữ - không có khung trắng
            st.markdown("""
            <p style="font-size:13px;color:#64748b;margin-bottom:20px;text-align:center;">
                Nhập thông tin để truy cập hệ thống
            </p>
            """, unsafe_allow_html=True)

            # Form đăng nhập trực tiếp, không khung
            email = st.text_input("📧 Email", placeholder="doctor@health.ai", key="li_email")
            password = st.text_input("🔑 Mật khẩu", type="password", placeholder="Nhập mật khẩu", key="li_pass")

            st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
            btn_login = st.button("🚀  Đăng nhập", type="primary", use_container_width=True, key="do_login")

            st.markdown("""
            <div style="text-align:center;font-size:12px;color:#94a3b8;margin-top:20px;">
                Chưa có tài khoản?
                <span style="color:#0ea5e9;">Chọn tab Đăng ký ↑</span>
            </div>
            """, unsafe_allow_html=True)

            if btn_login:
                e = email.strip()
                p = password
                if not e or not p:
                    err_spot.error("⚠️ Vui lòng điền đầy đủ thông tin.")
                else:
                    accounts = _get_accounts()
                    acct = accounts.get(e)
                    if acct and acct["password"] == p:
                        st.session_state["logged_in"] = True
                        st.session_state["user_email"] = e
                        st.session_state["user_name"] = acct.get("name", e.split("@")[0].capitalize())
                        st.session_state["page"] = "home"
                        st.rerun()
                    else:
                        err_spot.error("❌ Email hoặc mật khẩu không đúng.")

        # ĐĂNG KÝ
        else:
            st.markdown("""
            <p style="font-size:13px;color:#64748b;margin-bottom:20px;text-align:center;">
                Tạo tài khoản mới để sử dụng hệ thống
            </p>
            """, unsafe_allow_html=True)

            full_name = st.text_input("👤 Họ và tên", placeholder="Nguyễn Văn A", key="rg_name")
            email_r = st.text_input("📧 Email", placeholder="example@email.com", key="rg_email")
            pass_r = st.text_input("🔑 Mật khẩu", type="password", placeholder="Tối thiểu 6 ký tự", key="rg_pass")
            pass_r2 = st.text_input("🔑 Xác nhận mật khẩu", type="password", placeholder="Nhập lại mật khẩu", key="rg_pass2")

            st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
            btn_reg = st.button("✅  Tạo tài khoản", type="primary", use_container_width=True, key="do_register")

            if btn_reg:
                e = email_r.strip()
                n = full_name.strip()
                p = pass_r
                p2 = pass_r2
                accounts = _get_accounts()
                if not all([e, n, p, p2]):
                    err_spot.error("⚠️ Vui lòng điền đầy đủ tất cả các trường.")
                elif p != p2:
                    err_spot.error("❌ Mật khẩu xác nhận không khớp.")
                elif len(p) < 6:
                    err_spot.error("⚠️ Mật khẩu cần ít nhất 6 ký tự.")
                elif e in accounts:
                    err_spot.error("❌ Email này đã được đăng ký rồi.")
                elif "@" not in e or "." not in e:
                    err_spot.error("⚠️ Email không hợp lệ.")
                else:
                    if "registered_accounts" not in st.session_state:
                        st.session_state["registered_accounts"] = {}
                    st.session_state["registered_accounts"][e] = {"password": p, "name": n}
                    ok_spot.success(f"✅ Đăng ký thành công! Xin chào {n}. Hãy đăng nhập.")
                    st.session_state["auth_tab"] = "login"

        st.markdown("<div style='height:48px'></div>", unsafe_allow_html=True)

    # Footer
    st.markdown("""
    <div style="text-align:center;font-size:11px;color:#94a3b8;padding:16px 0 24px;">
        © 2024 HealthAI · Phiên bản 3.0 · Chỉ dành cho mục đích nghiên cứu
    </div>
    """, unsafe_allow_html=True)