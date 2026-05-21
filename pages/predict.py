"""
pages/predict.py — Trang dự đoán (giữ nguyên logic, chỉ thay đổi giao diện)
Kết quả hiển thị dạng popup modal thay vì inline.
"""
import streamlit as st
import numpy as np
import os

# Lazy-load model & scaler (only when actually predicting)
_model  = None
_scaler = None

def _load_css():
    css_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "style.css")
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def _load_model_scaler():
    global _model, _scaler
    if _model is None or _scaler is None:
        import pickle
        from keras.models import load_model as km_load

        base = os.path.dirname(os.path.dirname(__file__))
        model_path  = os.path.join(base, "models", "diabetes_model.h5")
        scaler_path = os.path.join(base, "models", "scaler.pkl")
        try:
            _model = km_load(model_path)
            with open(scaler_path, "rb") as f:
                _scaler = pickle.load(f)
        except Exception as e:
            st.error(f"Không tìm thấy file mô hình. Chi tiết: {e}")
            st.warning(f"Đường dẫn tìm kiếm: {model_path}")
    return _model, _scaler


def _risk_color(prob):
    if prob < 0.3:   return "#0abfbc", "NGUY CƠ THẤP",    "🟢"
    if prob < 0.7:   return "#e4b95b", "NGUY CƠ TRUNG BÌNH", "🟡"
    return               "#e05c6e", "NGUY CƠ CAO",      "🔴"


def show():
    _load_css()

    user    = st.session_state.get("user_name", "Người dùng")
    initial = user[0].upper() if user else "U"

    # ---- Top Navigation ----
    st.markdown(f"""
    <div class="topnav">
        <div class="topnav-brand">🏥 Health<span>AI</span></div>
        <div class="topnav-user">
            <span>{user}</span>
            <div class="topnav-avatar">{initial}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ---- Page header ----
    st.markdown("""
    <div style="padding:32px 32px 0; max-width:1100px; margin:0 auto;">
        <div style="display:flex;align-items:center;gap:12px;margin-bottom:6px;">
            <span style="font-size:28px;">🩺</span>
            <h1 style="font-family:'Playfair Display',serif;font-size:28px;color:#f5f7fa;">
                Kiểm Tra Nguy Cơ Tiểu Đường
            </h1>
        </div>
        <p style="color:#8fa3c0;font-size:14px;margin-left:40px;margin-bottom:24px;">
            Nhập các chỉ số lâm sàng bên dưới — AI sẽ phân tích và hiển thị kết quả trong popup
        </p>
        <hr style="border:none;border-top:1px solid rgba(10,191,188,0.15);margin-bottom:28px;">
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div style="padding:0 32px 48px;max-width:1100px;margin:0 auto;">', unsafe_allow_html=True)

    # ---- Two-column input form ----
    left, gap, right = st.columns([5, 1, 5])

    with left:
        st.markdown('<div class="section-header">📋 Thông số lâm sàng</div>', unsafe_allow_html=True)

        pregnancies = st.number_input(
            "Số lần mang thai (Pregnancies)", min_value=0, max_value=20, value=1, step=1,
            help="Tổng số lần mang thai")
        st.markdown('<p class="field-hint">0 nếu chưa từng mang thai</p>', unsafe_allow_html=True)

        glucose = st.slider(
            "Đường huyết (Glucose) — mg/dL", min_value=0, max_value=200, value=120,
            help="Nồng độ glucose huyết tương sau 2h nghiệm pháp dung nạp glucose")
        st.markdown(f'<p class="field-hint">Bình thường: 70–99 mg/dL · Hiện tại: <b style="color:#0abfbc">{glucose}</b></p>', unsafe_allow_html=True)

        blood_pressure = st.slider(
            "Huyết áp tâm trương (BloodPressure) — mmHg", min_value=0, max_value=130, value=70)
        st.markdown(f'<p class="field-hint">Bình thường: 60–80 mmHg · Hiện tại: <b style="color:#0abfbc">{blood_pressure}</b></p>', unsafe_allow_html=True)

        skin_thickness = st.slider(
            "Độ dày nếp gấp da (SkinThickness) — mm", min_value=0, max_value=100, value=20)
        st.markdown(f'<p class="field-hint">Cơ đầu tam đầu; bình thường: 10–35 mm</p>', unsafe_allow_html=True)

        insulin = st.slider(
            "Insulin huyết thanh — μU/mL", min_value=0, max_value=900, value=80)
        st.markdown(f'<p class="field-hint">Mức bình thường lúc đói: 16–166 μU/mL</p>', unsafe_allow_html=True)

    with right:
        st.markdown('<div class="section-header">📏 Thông số nhân trắc học</div>', unsafe_allow_html=True)

        weight = st.number_input(
            "Cân nặng (Weight) — kg", min_value=1.0, max_value=200.0, value=70.0, step=0.5)

        height_cm = st.number_input(
            "Chiều cao (Height) — cm", min_value=50.0, max_value=250.0, value=165.0, step=0.5)

        height_m = height_cm / 100.0
        bmi = weight / (height_m ** 2) if height_m > 0 else 0.0

        # BMI display card
        bmi_color = "#0abfbc" if 18.5 <= bmi < 25 else ("#e4b95b" if bmi < 30 else "#e05c6e")
        bmi_label = "Bình thường" if 18.5 <= bmi < 25 else ("Thừa cân" if bmi < 30 else "Béo phì" if bmi >= 30 else "Gầy")
        st.markdown(f"""
        <div style="background:rgba(17,34,64,0.7);border:1px solid rgba(10,191,188,0.15);
             border-radius:12px;padding:14px 18px;display:flex;align-items:center;justify-content:space-between;margin-bottom:16px;">
            <div>
                <div style="font-size:12px;color:#8fa3c0;margin-bottom:2px;">Chỉ số BMI (tính tự động)</div>
                <div style="font-family:'Playfair Display',serif;font-size:28px;color:{bmi_color};font-weight:700;">{bmi:.1f}</div>
            </div>
            <div style="text-align:right;">
                <div style="font-size:13px;color:{bmi_color};font-weight:600;">{bmi_label}</div>
                <div style="font-size:11px;color:#8fa3c0;margin-top:4px;">{weight:.1f} kg / {height_cm:.0f} cm</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # BMI bar
        bmi_pct = min(bmi / 40 * 100, 100)
        st.markdown(f"""
        <div class="risk-bar-wrap">
            <div class="risk-bar-fill" style="width:{bmi_pct:.0f}%;
                 background:linear-gradient(90deg, #0abfbc, {bmi_color});"></div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

        st.markdown('<div class="section-header" style="margin-top:24px;">🧬 Yếu tố di truyền & tuổi</div>', unsafe_allow_html=True)

        dpf = st.number_input(
            "Chức năng phả hệ tiểu đường (DPF)", min_value=0.0, max_value=3.0, value=0.5, step=0.01,
            help="Điểm số phản ánh tiền sử gia đình mắc tiểu đường")
        st.markdown('<p class="field-hint">Điểm cao = tiền sử gia đình nặng hơn</p>', unsafe_allow_html=True)

        age = st.number_input(
            "Tuổi (Age)", min_value=1, max_value=120, value=30, step=1)

        # Summary row
        st.markdown(f"""
        <div style="background:rgba(10,191,188,0.06);border:1px solid rgba(10,191,188,0.12);
             border-radius:10px;padding:12px 16px;margin-top:20px;">
            <div style="font-size:11px;color:#8fa3c0;margin-bottom:8px;font-weight:600;text-transform:uppercase;letter-spacing:0.06em;">Tóm tắt nhập liệu</div>
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:4px 16px;font-size:12px;color:#f5f7fa;">
                <span>🩸 Glucose: <b>{glucose}</b></span>
                <span>💉 Insulin: <b>{insulin}</b></span>
                <span>❤️ BP: <b>{blood_pressure}</b></span>
                <span>📐 Skin: <b>{skin_thickness}</b></span>
                <span>🧬 DPF: <b>{dpf}</b></span>
                <span>🎂 Tuổi: <b>{age}</b></span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ---- Predict button (centered) ----
    st.markdown("<div style='height:32px'></div>", unsafe_allow_html=True)
    _, btn_col, _ = st.columns([3, 4, 3])
    with btn_col:
        predict_btn = st.button("🚀  Phân tích & Xem kết quả AI", type="primary", use_container_width=True)

    # ---- Back button ----
    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
    _, back_col, _ = st.columns([3, 4, 3])
    with back_col:
        if st.button("← Quay về trang chủ", use_container_width=True):
            st.session_state["page"] = "home"
            st.rerun()

    # ---- POPUP / Modal result ----
    if predict_btn:
        model, scaler = _load_model_scaler()
        if model and scaler:
            user_data        = np.array([[pregnancies, glucose, blood_pressure,
                                           skin_thickness, insulin, bmi, dpf, age]])
            user_data_scaled = scaler.transform(user_data)
            prob             = float(model.predict(user_data_scaled)[0][0])
            color, level_txt, emoji = _risk_color(prob)
            pct = prob * 100
            bar_pct = min(pct, 100)

            # Advice content (mirrors original app.py logic)
            if prob < 0.3:
                advice_html = """
                <div style="margin-top:16px;">
                    <div style="font-size:13px;font-weight:600;color:#f5f7fa;margin-bottom:10px;">📋 Lời khuyên sức khỏe</div>
                    <ul style="padding-left:18px;color:#8fa3c0;font-size:13px;line-height:1.9;">
                        <li><b style="color:#f5f7fa;">Duy trì phong độ:</b> Chỉ số sinh tồn đang ở trạng thái lý tưởng. Tiếp tục duy trì chế độ ăn cân bằng.</li>
                        <li><b style="color:#f5f7fa;">Hoạt động thể chất:</b> Duy trì ít nhất 150 phút/tuần (chạy bộ, bơi lội, đạp xe).</li>
                        <li><b style="color:#f5f7fa;">Kiểm tra định kỳ:</b> Kiểm tra đường huyết trong các kỳ khám tổng quát hàng năm.</li>
                    </ul>
                </div>
                """
            elif prob < 0.7:
                advice_html = """
                <div style="margin-top:16px;">
                    <div style="font-size:13px;font-weight:600;color:#f5f7fa;margin-bottom:10px;">📋 Lời khuyên sức khỏe</div>
                    <ul style="padding-left:18px;color:#8fa3c0;font-size:13px;line-height:1.9;">
                        <li><b style="color:#f5f7fa;">Cảnh báo sớm:</b> Các chỉ số đang trong vùng tiền tiểu đường. Cần thay đổi lối sống ngay.</li>
                        <li><b style="color:#f5f7fa;">Điều chỉnh chế độ ăn:</b> Hạn chế carbohydrate tinh chế; bổ sung chất xơ từ rau xanh và ngũ cốc nguyên hạt.</li>
                        <li><b style="color:#f5f7fa;">Kiểm soát cân nặng:</b> Nếu BMI thừa cân, lên kế hoạch giảm 5–7% trọng lượng cơ thể.</li>
                    </ul>
                </div>
                """
            else:
                advice_html = """
                <div style="margin-top:16px;">
                    <div style="font-size:13px;font-weight:600;color:#f5f7fa;margin-bottom:10px;">📋 Tư vấn y khoa (Chế độ dinh dưỡng nghiêm ngặt)</div>
                    <ul style="padding-left:18px;color:#8fa3c0;font-size:13px;line-height:1.9;">
                        <li><b style="color:#f5f7fa;">Chế độ ăn:</b> Đảm bảo đủ chất dinh dưỡng, không làm tăng đường huyết đột ngột sau ăn.</li>
                        <li><b style="color:#f5f7fa;">Cân đối dinh dưỡng:</b> Tăng rau xanh, ngũ cốc nguyên hạt; giảm carbohydrate tinh chế và chất béo.</li>
                        <li><b style="color:#f5f7fa;">Theo dõi thường xuyên:</b> Đo đường huyết sau các bữa ăn và ghi chép kết quả.</li>
                        <li><b style="color:#e05c6e;">⚠️ Khẩn cấp:</b> Tham khảo bác sĩ hoặc chuyên gia dinh dưỡng <u>ngay lập tức</u>.</li>
                    </ul>
                </div>
                """

            st.markdown(f"""
            <div style="
                position:fixed; inset:0; z-index:9999;
                background:rgba(0,0,0,0.75); backdrop-filter:blur(6px);
                display:flex; align-items:center; justify-content:center;
                animation:fadeIn 0.2s ease;
            ">
                <div style="
                    background:#112240; border:1px solid rgba(10,191,188,0.18);
                    border-radius:24px; padding:40px 36px; max-width:520px; width:90vw;
                    box-shadow:0 24px 80px rgba(0,0,0,0.6);
                    animation:slideUp 0.3s ease; position:relative;
                ">
                    <!-- Close hint -->
                    <div style="position:absolute;top:18px;right:24px;font-size:11px;
                         color:#8fa3c0;cursor:default;">↓ cuộn xuống để đóng</div>

                    <!-- Header -->
                    <div style="text-align:center;margin-bottom:24px;">
                        <div style="font-size:44px;margin-bottom:8px;">{emoji}</div>
                        <div style="font-family:'Playfair Display',serif;font-size:22px;
                             color:{color};font-weight:700;">{level_txt}</div>
                        <div style="font-size:13px;color:#8fa3c0;margin-top:4px;">
                            Xác suất mắc bệnh tiểu đường
                        </div>
                    </div>

                    <!-- Big probability number -->
                    <div style="text-align:center;margin-bottom:20px;">
                        <span style="font-family:'Playfair Display',serif;font-size:56px;
                               font-weight:700;color:{color};">{pct:.1f}%</span>
                    </div>

                    <!-- Risk progress bar -->
                    <div style="margin-bottom:20px;">
                        <div style="display:flex;justify-content:space-between;
                             font-size:11px;color:#8fa3c0;margin-bottom:6px;">
                            <span>Thấp</span><span>Trung bình</span><span>Cao</span>
                        </div>
                        <div style="height:10px;background:rgba(255,255,255,0.08);border-radius:5px;overflow:hidden;">
                            <div style="height:100%;width:{bar_pct:.1f}%;
                                 background:linear-gradient(90deg,#0abfbc,{color});
                                 border-radius:5px;transition:width 0.8s;"></div>
                        </div>
                        <div style="display:flex;justify-content:space-between;
                             font-size:10px;color:#8fa3c0;margin-top:4px;">
                            <span>0%</span><span>30%</span><span>70%</span><span>100%</span>
                        </div>
                    </div>

                    <!-- Input summary chips -->
                    <div style="display:flex;flex-wrap:wrap;gap:8px;margin-bottom:16px;">
                        <span style="background:rgba(10,191,188,0.1);border:1px solid rgba(10,191,188,0.2);
                              border-radius:999px;padding:4px 12px;font-size:12px;color:#8fa3c0;">
                            BMI {bmi:.1f}
                        </span>
                        <span style="background:rgba(10,191,188,0.1);border:1px solid rgba(10,191,188,0.2);
                              border-radius:999px;padding:4px 12px;font-size:12px;color:#8fa3c0;">
                            Glucose {glucose}
                        </span>
                        <span style="background:rgba(10,191,188,0.1);border:1px solid rgba(10,191,188,0.2);
                              border-radius:999px;padding:4px 12px;font-size:12px;color:#8fa3c0;">
                            Tuổi {age}
                        </span>
                        <span style="background:rgba(10,191,188,0.1);border:1px solid rgba(10,191,188,0.2);
                              border-radius:999px;padding:4px 12px;font-size:12px;color:#8fa3c0;">
                            Insulin {insulin}
                        </span>
                    </div>

                    <!-- Advice -->
                    <div style="background:rgba(11,22,40,0.6);border-radius:12px;padding:16px;">
                        {advice_html}
                    </div>

                    <div style="margin-top:16px;font-size:11px;color:#8fa3c0;text-align:center;">
                        ⚠️ Đây là kết quả từ mô hình AI — không thay thế chẩn đoán y tế chuyên nghiệp.
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Streamlit close button (appears below the modal visually, user scrolls down or uses button)
            st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
            _, close_col, _ = st.columns([3, 4, 3])
            with close_col:
                if st.button("✕  Đóng kết quả", key="close_modal", use_container_width=True):
                    st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)
