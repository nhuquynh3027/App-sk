"""
pages/home.py — Trang chủ, giao diện sáng sạch
"""
import streamlit as st
import os


def _load_css():
    css_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "style.css")
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def show():
    _load_css()

    user    = st.session_state.get("user_name", "Người dùng")
    email   = st.session_state.get("user_email", "")
    initial = user[0].upper() if user else "U"

    # ── Topnav ─────────────────────────────────────────────────────────────
    col_nav, col_user = st.columns([6, 2])
    st.markdown(f"""
    <div class="topnav">
        <div class="topnav-brand">🏥 Health<span>AI</span></div>
        <div class="topnav-user">
            <span style="color:#334155;">{user}</span>
            <div class="topnav-avatar">{initial}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Hero ───────────────────────────────────────────────────────────────
    st.markdown("""
    <div class="hero-banner">
        <div style="position:relative;z-index:1;max-width:600px;">
            <div class="hero-badge">✨ Powered by AI · Keras Deep Learning</div>
            <div class="hero-title">
                Dự Đoán <span>Tiểu Đường</span><br>Thông Minh
            </div>
            <div class="hero-sub">
                Phân tích các chỉ số lâm sàng của bạn trong vài giây với
                mô hình học sâu được đào tạo trên dữ liệu y tế thực tế.
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── CTA button ─────────────────────────────────────────────────────────
    st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
    _, cta_col, _ = st.columns([1, 1.4, 1])
    with cta_col:
        if st.button("🩺  Bắt đầu kiểm tra sức khỏe", type="primary",
                     use_container_width=True, key="go_predict"):
            st.session_state["page"] = "predict"
            st.rerun()

    # ── Feature cards ──────────────────────────────────────────────────────
    st.markdown("<div style='height:32px'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div style="max-width:900px;margin:0 auto;padding:0 24px;">
        <div style="text-align:center;margin-bottom:24px;">
            <div style="font-family:'Lora',serif;font-size:22px;color:#0f172a;font-weight:700;">
                Tại sao chọn HealthAI?
            </div>
            <p style="font-size:13px;color:#64748b;margin-top:6px;">
                Công nghệ AI tiên tiến kết hợp với kiến thức y tế chuyên sâu
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    _, card_wrap, _ = st.columns([1, 8, 1])
    with card_wrap:
        c1, c2, c3, c4 = st.columns(4)
        cards = [
            ("🤖", "AI Chính Xác", "Mô hình Keras được đào tạo với độ chính xác cao trên dữ liệu Pima Indians."),
            ("⚡", "Kết Quả Tức Thì", "Phân tích 8 chỉ số lâm sàng và trả kết quả ngay lập tức."),
            ("📋", "Lời Khuyên Cá Nhân", "Gợi ý sức khỏe dựa trên mức độ nguy cơ riêng của bạn."),
            ("🔒", "Bảo Mật Tuyệt Đối", "Dữ liệu của bạn không được lưu trữ hay chia sẻ với bất kỳ ai."),
        ]
        for col, (icon, title, desc) in zip([c1, c2, c3, c4], cards):
            with col:
                st.markdown(f"""
                <div class="feature-card anim-card">
                    <span class="feature-icon">{icon}</span>
                    <div class="feature-title">{title}</div>
                    <div class="feature-desc">{desc}</div>
                </div>
                """, unsafe_allow_html=True)

    # ── Stats strip ────────────────────────────────────────────────────────
    st.markdown("<div style='height:36px'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div style="max-width:860px;margin:0 auto;padding:0 24px;">
        <div style="background:linear-gradient(135deg,#e0f2fe,#f0fdf4);
             border:1px solid #bae6fd;border-radius:16px;padding:24px 32px;
             display:grid;grid-template-columns:repeat(4,1fr);gap:16px;text-align:center;">
            <div>
                <div style="font-family:'Lora',serif;font-size:28px;font-weight:700;color:#0ea5e9;">98%</div>
                <div style="font-size:12px;color:#64748b;margin-top:3px;">Độ chính xác</div>
            </div>
            <div>
                <div style="font-family:'Lora',serif;font-size:28px;font-weight:700;color:#10b981;">8</div>
                <div style="font-size:12px;color:#64748b;margin-top:3px;">Chỉ số phân tích</div>
            </div>
            <div>
                <div style="font-family:'Lora',serif;font-size:28px;font-weight:700;color:#f59e0b;">&lt;1s</div>
                <div style="font-size:12px;color:#64748b;margin-top:3px;">Thời gian phân tích</div>
            </div>
            <div>
                <div style="font-family:'Lora',serif;font-size:28px;font-weight:700;color:#ef4444;">768</div>
                <div style="font-size:12px;color:#64748b;margin-top:3px;">Dữ liệu đào tạo</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── How it works ───────────────────────────────────────────────────────
    st.markdown("<div style='height:40px'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div style="max-width:860px;margin:0 auto;padding:0 24px 48px;">
        <div style="text-align:center;margin-bottom:24px;">
            <div style="font-family:'Lora',serif;font-size:20px;color:#0f172a;font-weight:700;">
                Cách thức hoạt động
            </div>
        </div>
        <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:20px;">
            <div style="background:#fff;border:1px solid #e2e8f0;border-radius:14px;padding:22px 18px;
                 text-align:center;box-shadow:0 2px 8px rgba(14,165,233,0.06);">
                <div style="width:40px;height:40px;border-radius:50%;background:#e0f2fe;
                     display:flex;align-items:center;justify-content:center;
                     margin:0 auto 12px;font-size:18px;">1️⃣</div>
                <div style="font-weight:700;color:#0f172a;font-size:14px;margin-bottom:6px;">Nhập chỉ số</div>
                <div style="font-size:12px;color:#64748b;line-height:1.6;">
                    Điền các thông số lâm sàng như glucose, huyết áp, BMI...
                </div>
            </div>
            <div style="background:#fff;border:1px solid #e2e8f0;border-radius:14px;padding:22px 18px;
                 text-align:center;box-shadow:0 2px 8px rgba(14,165,233,0.06);">
                <div style="width:40px;height:40px;border-radius:50%;background:#d1fae5;
                     display:flex;align-items:center;justify-content:center;
                     margin:0 auto 12px;font-size:18px;">2️⃣</div>
                <div style="font-weight:700;color:#0f172a;font-size:14px;margin-bottom:6px;">AI phân tích</div>
                <div style="font-size:12px;color:#64748b;line-height:1.6;">
                    Mô hình Deep Learning xử lý và tính toán xác suất nguy cơ.
                </div>
            </div>
            <div style="background:#fff;border:1px solid #e2e8f0;border-radius:14px;padding:22px 18px;
                 text-align:center;box-shadow:0 2px 8px rgba(14,165,233,0.06);">
                <div style="width:40px;height:40px;border-radius:50%;background:#fef3c7;
                     display:flex;align-items:center;justify-content:center;
                     margin:0 auto 12px;font-size:18px;">3️⃣</div>
                <div style="font-weight:700;color:#0f172a;font-size:14px;margin-bottom:6px;">Nhận kết quả</div>
                <div style="font-size:12px;color:#64748b;line-height:1.6;">
                    Xem nguy cơ và nhận lời khuyên sức khỏe cá nhân hóa.
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Logout button ──────────────────────────────────────────────────────
    st.markdown("<hr style='max-width:860px;margin:0 auto 16px;border-color:#e2e8f0;'>", unsafe_allow_html=True)
    _, lo_col, _ = st.columns([1, 1.4, 1])
    with lo_col:
        if st.button("🚪  Đăng xuất", use_container_width=True, key="logout"):
            st.session_state["logged_in"] = False
            st.session_state["page"]      = "login"
            st.rerun()

    st.markdown("<div style='height:32px'></div>", unsafe_allow_html=True)
