"""
pages/home.py — Trang chủ (sau khi đăng nhập)
"""
import streamlit as st
import base64, os


def _load_css():
    css_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "style.css")
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# SVG health-themed images generated inline — add real image files as
# assets/anh_1.jpg, anh_2.jpg … and they'll be loaded automatically.
GALLERY_SVG = [
    # Image 1: DNA / Genomics
    ("""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300">
  <defs>
    <radialGradient id="g1" cx="50%" cy="50%" r="60%">
      <stop offset="0%" stop-color="#0d2a4a"/>
      <stop offset="100%" stop-color="#0b1628"/>
    </radialGradient>
  </defs>
  <rect width="400" height="300" fill="url(#g1)"/>
  <!-- DNA helix -->
  <g opacity="0.9">
    <path d="M160,20 Q200,75 240,130 Q200,185 160,240 Q120,185 160,130 Q200,75 160,20" fill="none" stroke="#0abfbc" stroke-width="2.5"/>
    <path d="M240,20 Q200,75 160,130 Q200,185 240,240" fill="none" stroke="#e4b95b" stroke-width="2.5"/>
    <!-- rungs -->
    <line x1="178" y1="54" x2="222" y2="54" stroke="#8fa3c0" stroke-width="1.5" opacity="0.6"/>
    <line x1="165" y1="88" x2="235" y2="88" stroke="#8fa3c0" stroke-width="1.5" opacity="0.6"/>
    <line x1="160" y1="130" x2="240" y2="130" stroke="#0abfbc" stroke-width="2" opacity="0.8"/>
    <line x1="165" y1="170" x2="235" y2="170" stroke="#8fa3c0" stroke-width="1.5" opacity="0.6"/>
    <line x1="178" y1="205" x2="222" y2="205" stroke="#8fa3c0" stroke-width="1.5" opacity="0.6"/>
  </g>
  <circle cx="160" cy="20" r="4" fill="#0abfbc"/>
  <circle cx="240" cy="20" r="4" fill="#e4b95b"/>
  <circle cx="160" cy="240" r="4" fill="#e4b95b"/>
  <circle cx="240" cy="240" r="4" fill="#0abfbc"/>
  <!-- Glow -->
  <circle cx="200" cy="130" r="50" fill="none" stroke="#0abfbc" stroke-width="0.5" opacity="0.3"/>
  <!-- Text -->
  <text x="200" y="274" text-anchor="middle" font-family="serif" font-size="13" fill="#8fa3c0">Phân tích gen di truyền</text>
</svg>""", "Phân tích gen di truyền"),

    # Image 2: Blood glucose monitor
    ("""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300">
  <defs>
    <radialGradient id="g2" cx="30%" cy="30%" r="70%">
      <stop offset="0%" stop-color="#112240"/>
      <stop offset="100%" stop-color="#0b1628"/>
    </radialGradient>
  </defs>
  <rect width="400" height="300" fill="url(#g2)"/>
  <!-- Monitor device -->
  <rect x="110" y="60" width="180" height="140" rx="16" fill="rgba(17,34,64,0.9)" stroke="#0abfbc" stroke-width="1.5"/>
  <!-- Screen -->
  <rect x="125" y="75" width="150" height="90" rx="8" fill="#091622"/>
  <!-- Glucose reading -->
  <text x="200" y="115" text-anchor="middle" font-family="serif" font-size="34" font-weight="700" fill="#0abfbc">126</text>
  <text x="200" y="135" text-anchor="middle" font-size="11" fill="#8fa3c0">mg/dL  ·  Đường huyết</text>
  <!-- Mini chart inside screen -->
  <polyline points="132,155 148,148 164,152 180,140 196,145 212,132 228,138 244,128 260,133 268,128"
            fill="none" stroke="#e4b95b" stroke-width="1.8"/>
  <!-- Button row -->
  <circle cx="200" cy="224" r="12" fill="rgba(10,191,188,0.15)" stroke="#0abfbc" stroke-width="1"/>
  <text x="200" y="229" text-anchor="middle" font-size="11" fill="#0abfbc">⏻</text>
  <!-- Side LED -->
  <rect x="285" y="100" width="6" height="6" rx="3" fill="#e05c6e"/>
  <!-- Label -->
  <text x="200" y="274" text-anchor="middle" font-family="serif" font-size="13" fill="#8fa3c0">Kiểm soát đường huyết</text>
</svg>""", "Kiểm soát đường huyết"),

    # Image 3: Heart / Pulse
    ("""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300">
  <rect width="400" height="300" fill="#0b1628"/>
  <!-- Pulse line -->
  <polyline points="20,150 80,150 100,100 120,180 140,150 160,150 180,80 200,200 220,150 240,150 260,120 280,160 300,150 380,150"
            fill="none" stroke="#e05c6e" stroke-width="2.5" stroke-linejoin="round"/>
  <!-- Glow duplicate -->
  <polyline points="20,150 80,150 100,100 120,180 140,150 160,150 180,80 200,200 220,150 240,150 260,120 280,160 300,150 380,150"
            fill="none" stroke="#e05c6e" stroke-width="6" stroke-linejoin="round" opacity="0.12"/>
  <!-- Heart icon -->
  <path d="M200,95 C200,95 188,84 178,84 C165,84 157,93 157,104 C157,118 173,130 200,148 C227,130 243,118 243,104 C243,93 235,84 222,84 C212,84 200,95 200,95 Z"
        fill="rgba(224,92,110,0.15)" stroke="#e05c6e" stroke-width="2"/>
  <!-- BPM label -->
  <text x="200" y="232" text-anchor="middle" font-family="serif" font-size="26" font-weight="700" fill="#e05c6e">72 BPM</text>
  <text x="200" y="252" text-anchor="middle" font-size="11" fill="#8fa3c0">Nhịp tim bình thường</text>
  <text x="200" y="274" text-anchor="middle" font-family="serif" font-size="13" fill="#8fa3c0">Theo dõi tim mạch</text>
</svg>""", "Theo dõi tim mạch"),

    # Image 4: Neural Network
    ("""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300">
  <rect width="400" height="300" fill="#0b1628"/>
  <!-- Connections -->
  <g stroke="#0abfbc" stroke-width="0.8" opacity="0.25">
    <line x1="60" y1="60" x2="170" y2="80"/>
    <line x1="60" y1="60" x2="170" y2="150"/>
    <line x1="60" y1="150" x2="170" y2="80"/>
    <line x1="60" y1="150" x2="170" y2="150"/>
    <line x1="60" y1="150" x2="170" y2="220"/>
    <line x1="60" y1="240" x2="170" y2="150"/>
    <line x1="60" y1="240" x2="170" y2="220"/>
    <line x1="170" y1="80" x2="280" y2="60"/>
    <line x1="170" y1="80" x2="280" y2="150"/>
    <line x1="170" y1="150" x2="280" y2="60"/>
    <line x1="170" y1="150" x2="280" y2="150"/>
    <line x1="170" y1="150" x2="280" y2="240"/>
    <line x1="170" y1="220" x2="280" y2="150"/>
    <line x1="170" y1="220" x2="280" y2="240"/>
    <line x1="280" y1="60" x2="360" y2="150"/>
    <line x1="280" y1="150" x2="360" y2="150"/>
    <line x1="280" y1="240" x2="360" y2="150"/>
  </g>
  <!-- Active connections -->
  <g stroke="#0abfbc" stroke-width="1.5" opacity="0.7">
    <line x1="60" y1="150" x2="170" y2="150"/>
    <line x1="170" y1="150" x2="280" y2="150"/>
    <line x1="280" y1="150" x2="360" y2="150"/>
  </g>
  <!-- Input nodes -->
  <g fill="#112240" stroke="#e4b95b" stroke-width="1.5">
    <circle cx="60" cy="60" r="12"/>
    <circle cx="60" cy="150" r="14" fill="rgba(10,191,188,0.2)" stroke="#0abfbc" stroke-width="2"/>
    <circle cx="60" cy="240" r="12"/>
  </g>
  <!-- Hidden layer -->
  <g fill="#112240" stroke="#0abfbc" stroke-width="1.5">
    <circle cx="170" cy="80" r="12"/>
    <circle cx="170" cy="150" r="14" fill="rgba(10,191,188,0.25)" stroke-width="2"/>
    <circle cx="170" cy="220" r="12"/>
  </g>
  <!-- Second hidden -->
  <g fill="#112240" stroke="#0abfbc" stroke-width="1.5">
    <circle cx="280" cy="60" r="12"/>
    <circle cx="280" cy="150" r="14" fill="rgba(10,191,188,0.25)" stroke-width="2"/>
    <circle cx="280" cy="240" r="12"/>
  </g>
  <!-- Output node -->
  <circle cx="360" cy="150" r="16" fill="rgba(10,191,188,0.3)" stroke="#0abfbc" stroke-width="2.5"/>
  <text x="360" y="155" text-anchor="middle" font-size="11" fill="#0abfbc">AI</text>
  <!-- Label -->
  <text x="200" y="274" text-anchor="middle" font-family="serif" font-size="13" fill="#8fa3c0">Mạng nơ-ron nhân tạo</text>
</svg>""", "Mạng nơ-ron nhân tạo"),

    # Image 5: BMI / Body metrics
    ("""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300">
  <rect width="400" height="300" fill="#0b1628"/>
  <!-- Circle gauge -->
  <circle cx="200" cy="140" r="90" fill="none" stroke="rgba(255,255,255,0.05)" stroke-width="16"/>
  <!-- BMI arc (normal range ~22) -->
  <circle cx="200" cy="140" r="90" fill="none" stroke="#0abfbc" stroke-width="16"
          stroke-dasharray="283 565" stroke-dashoffset="0" stroke-linecap="round"
          transform="rotate(-90 200 140)" opacity="0.85"/>
  <!-- Danger arc -->
  <circle cx="200" cy="140" r="90" fill="none" stroke="#e05c6e" stroke-width="16"
          stroke-dasharray="100 565" stroke-dashoffset="-283" stroke-linecap="round"
          transform="rotate(-90 200 140)" opacity="0.5"/>
  <!-- Center text -->
  <text x="200" y="128" text-anchor="middle" font-family="serif" font-size="38" font-weight="700" fill="#f5f7fa">22.8</text>
  <text x="200" y="150" text-anchor="middle" font-size="13" fill="#0abfbc" font-weight="600">BMI · Bình thường</text>
  <!-- Tick marks -->
  <text x="112" y="235" font-size="10" fill="#8fa3c0">Gầy</text>
  <text x="178" y="244" font-size="10" fill="#0abfbc">Bình thường</text>
  <text x="275" y="235" font-size="10" fill="#e05c6e">Béo phì</text>
  <text x="200" y="274" text-anchor="middle" font-family="serif" font-size="13" fill="#8fa3c0">Chỉ số BMI cơ thể</text>
</svg>""", "Chỉ số BMI cơ thể"),

    # Image 6: Lab / Blood test
    ("""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300">
  <rect width="400" height="300" fill="#0b1628"/>
  <!-- Test tubes -->
  <g>
    <!-- Tube 1 (teal) -->
    <rect x="100" y="70" width="30" height="120" rx="4" fill="rgba(17,34,64,0.9)" stroke="#0abfbc" stroke-width="1.5"/>
    <rect x="104" y="100" width="22" height="90" rx="3" fill="rgba(10,191,188,0.3)"/>
    <rect x="100" y="70" width="30" height="12" rx="2" fill="#0abfbc"/>
    <!-- Tube 2 (gold) -->
    <rect x="155" y="90" width="30" height="100" rx="4" fill="rgba(17,34,64,0.9)" stroke="#e4b95b" stroke-width="1.5"/>
    <rect x="159" y="130" width="22" height="60" rx="3" fill="rgba(228,185,91,0.3)"/>
    <rect x="155" y="90" width="30" height="12" rx="2" fill="#e4b95b"/>
    <!-- Tube 3 (rose) -->
    <rect x="210" y="80" width="30" height="110" rx="4" fill="rgba(17,34,64,0.9)" stroke="#e05c6e" stroke-width="1.5"/>
    <rect x="214" y="100" width="22" height="90" rx="3" fill="rgba(224,92,110,0.25)"/>
    <rect x="210" y="80" width="30" height="12" rx="2" fill="#e05c6e"/>
    <!-- Tube 4 (muted) -->
    <rect x="265" y="100" width="30" height="90" rx="4" fill="rgba(17,34,64,0.9)" stroke="#8fa3c0" stroke-width="1.5"/>
    <rect x="269" y="140" width="22" height="50" rx="3" fill="rgba(143,163,192,0.2)"/>
    <rect x="265" y="100" width="30" height="12" rx="2" fill="#8fa3c0"/>
    <!-- Base rack -->
    <rect x="85" y="190" width="230" height="10" rx="5" fill="#112240" stroke="#1d3461" stroke-width="1"/>
  </g>
  <!-- Labels -->
  <text x="115" y="216" text-anchor="middle" font-size="10" fill="#0abfbc">HbA1c</text>
  <text x="170" y="216" text-anchor="middle" font-size="10" fill="#e4b95b">INS</text>
  <text x="225" y="216" text-anchor="middle" font-size="10" fill="#e05c6e">GLU</text>
  <text x="280" y="216" text-anchor="middle" font-size="10" fill="#8fa3c0">LDL</text>
  <text x="200" y="274" text-anchor="middle" font-family="serif" font-size="13" fill="#8fa3c0">Xét nghiệm máu lâm sàng</text>
</svg>""", "Xét nghiệm máu lâm sàng"),
]


def _get_image_srcs():
    """Load real image files if present (anh_1.*, anh_2.*, …) else use SVG."""
    asset_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets")
    imgs = []
    for i in range(1, 20):
        for ext in ("jpg", "jpeg", "png", "webp"):
            path = os.path.join(asset_dir, f"anh_{i}.{ext}")
            if os.path.exists(path):
                with open(path, "rb") as f:
                    b64 = base64.b64encode(f.read()).decode()
                mime = "image/jpeg" if ext in ("jpg", "jpeg") else f"image/{ext}"
                imgs.append((f"data:{mime};base64,{b64}", f"Ảnh {i}"))
                break
    return imgs if imgs else None  # None → use SVG fallback


def show():
    _load_css()

    user = st.session_state.get("user_name", "Người dùng")
    initial = user[0].upper() if user else "U"

    # ---- Top Navigation ----
    st.markdown(f"""
    <div class="topnav">
        <div class="topnav-brand">🏥 Health<span>AI</span></div>
        <div class="topnav-user">
            <span>Xin chào, {user}</span>
            <div class="topnav-avatar">{initial}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ---- Hero Banner ----
    st.markdown("""
    <div class="hero-banner">
        <div>
            <div class="hero-badge">✦ Ứng dụng y tế thông minh</div>
            <h1 class="hero-title">Dự Đoán & Tư Vấn<br><span>Bệnh Tiểu Đường</span></h1>
            <p class="hero-sub">
                Hệ thống AI phân tích 8 chỉ số lâm sàng, đánh giá nguy cơ tiểu đường
                và đưa ra khuyến nghị sức khỏe cá nhân hoá theo tiêu chuẩn y tế.
            </p>
            <div style="margin-top:24px; display:flex; gap:16px; flex-wrap:wrap; justify-content:center;">
                <span class="stat-pill">🧬 Mô hình Neural Network</span>
                <span class="stat-pill">📊 94% Độ chính xác</span>
                <span class="stat-pill">⚡ Phân tích tức thì</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="page-wrap">', unsafe_allow_html=True)

    # ---- Feature Cards ----
    st.markdown("<div style='height:32px'></div>", unsafe_allow_html=True)
    st.markdown("""
    <h2 style="font-family:'Playfair Display',serif;font-size:24px;color:#f5f7fa;margin-bottom:8px;">
        Tính năng nổi bật
    </h2>
    <p class="section-sub">Nền tảng AI toàn diện hỗ trợ chẩn đoán và tư vấn sức khỏe</p>
    """, unsafe_allow_html=True)

    fc1, fc2, fc3, fc4 = st.columns(4)
    for col, icon, title, desc in [
        (fc1, "🧠", "AI Phân tích", "Mạng nơ-ron học sâu phân tích đa chỉ số sinh tồn cùng lúc"),
        (fc2, "📋", "Tư vấn lâm sàng", "Lời khuyên được cá nhân hoá theo từng mức độ nguy cơ"),
        (fc3, "🔒", "Bảo mật dữ liệu", "Thông tin bệnh nhân được mã hoá và bảo vệ tuyệt đối"),
        (fc4, "📱", "Đa nền tảng", "Truy cập từ máy tính, điện thoại hoặc máy tính bảng"),
    ]:
        with col:
            st.markdown(f"""
            <div class="feature-card anim-card">
                <span class="feature-icon">{icon}</span>
                <div class="feature-title">{title}</div>
                <div class="feature-desc">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    # ---- Image Gallery ----
    st.markdown("<div style='height:40px'></div>", unsafe_allow_html=True)
    st.markdown("""
    <h2 style="font-family:'Playfair Display',serif;font-size:24px;color:#f5f7fa;margin-bottom:8px;">
        Thư viện Y tế
    </h2>
    <p class="section-sub">Hình ảnh minh hoạ các khía cạnh chẩn đoán và theo dõi sức khỏe</p>
    """, unsafe_allow_html=True)

    real_imgs = _get_image_srcs()
    gallery_items = []
    if real_imgs:
        gallery_items = [(f'<img src="{src}" style="width:100%;height:100%;object-fit:cover;">', cap)
                         for src, cap in real_imgs]
    else:
        gallery_items = [(svg, cap) for svg, cap in GALLERY_SVG]

    # Render 3-column gallery rows
    for row_start in range(0, len(gallery_items), 3):
        row = gallery_items[row_start:row_start+3]
        cols = st.columns(len(row))
        for col, (content, caption) in zip(cols, row):
            with col:
                st.markdown(f"""
                <div class="gallery-img-card" style="aspect-ratio:4/3;overflow:hidden;
                     border-radius:16px;position:relative;background:#112240;
                     box-shadow:0 8px 40px rgba(0,0,0,0.40);">
                    {content}
                    <div style="position:absolute;bottom:0;left:0;right:0;
                         background:linear-gradient(transparent,rgba(11,22,40,0.85));
                         padding:20px 16px 14px;font-size:13px;color:#f5f7fa;font-weight:500;">
                        {caption}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    # ---- CTA ----
    st.markdown("<div style='height:40px'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div style="background:linear-gradient(135deg,rgba(10,191,188,0.12),rgba(17,34,64,0.8));
         border:1px solid rgba(10,191,188,0.25);border-radius:20px;padding:40px;text-align:center;">
        <h2 style="font-family:'Playfair Display',serif;font-size:26px;color:#f5f7fa;margin-bottom:12px;">
            Sẵn sàng kiểm tra sức khỏe?
        </h2>
        <p style="color:#8fa3c0;font-size:15px;max-width:480px;margin:0 auto 24px;">
            Nhập các chỉ số lâm sàng của bạn và nhận kết quả phân tích AI chỉ trong vài giây.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
    col_cta1, col_cta2, col_cta3 = st.columns([2, 2, 2])
    with col_cta2:
        if st.button("🩺  Bắt đầu kiểm tra ngay", type="primary", use_container_width=True):
            st.session_state["page"] = "predict"
            st.rerun()

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
    col_l1, col_l2, col_l3 = st.columns([2, 2, 2])
    with col_l2:
        if st.button("🚪  Đăng xuất", use_container_width=True):
            for k in ["logged_in", "user_email", "user_name", "page"]:
                st.session_state.pop(k, None)
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)
