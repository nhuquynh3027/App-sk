"""
pages/predict.py — Trang dự đoán (logic giữ nguyên, giao diện mới + popup kết quả)
"""
import streamlit as st
import numpy as np
import os

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
        # Try both import paths for compatibility
        try:
            from tensorflow.keras.models import load_model as km_load
        except ImportError:
            from keras.models import load_model as km_load

        base        = os.path.dirname(os.path.dirname(__file__))
        model_path  = os.path.join(base, "models", "diabetes_model.h5")
        scaler_path = os.path.join(base, "models", "scaler.pkl")
        try:
            _model = km_load(model_path)
            with open(scaler_path, "rb") as f:
                _scaler = pickle.load(f)
        except Exception as e:
            st.error(f"Không tìm thấy file mô hình. Chi tiết: {e}")
            st.warning(f"Đường dẫn: {model_path}")
    return _model, _scaler


def _risk(prob):
    if prob < 0.3:  return "#0abfbc", "NGUY CƠ THẤP",        "🟢"
    if prob < 0.7:  return "#e4b95b", "NGUY CƠ TRUNG BÌNH",  "🟡"
    return               "#e05c6e", "NGUY CƠ CAO",           "🔴"


def show():
    _load_css()

    user    = st.session_state.get("user_name", "Người dùng")
    initial = user[0].upper() if user else "U"

    # ── Topnav ─────────────────────────────────────────────────────────────
    st.markdown(f"""
    <div class="topnav">
        <div class="topnav-brand">🏥 Health<span>AI</span></div>
        <div class="topnav-user">
            <span>{user}</span>
            <div class="topnav-avatar">{initial}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Page header ────────────────────────────────────────────────────────
    st.markdown("""
    <div style="padding:28px 32px 0; max-width:1060px; margin:0 auto;">
        <div style="display:flex;align-items:center;gap:10px;margin-bottom:4px;">
            <span style="font-size:26px;">🩺</span>
            <h1 style="font-family:'Playfair Display',serif;font-size:26px;color:#eef2f7;">
                Kiểm Tra Nguy Cơ Tiểu Đường
            </h1>
        </div>
        <p style="color:#7a93b4;font-size:13px;margin-left:36px;margin-bottom:22px;">
            Nhập các chỉ số lâm sàng — AI sẽ phân tích và hiển thị kết quả ngay
        </p>
        <hr>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="page-wrap">', unsafe_allow_html=True)

    # ── Two-column form ────────────────────────────────────────────────────
    left, gap, right = st.columns([5, 1, 5])

    with left:
        st.markdown('<div class="section-header">📋 Thông số lâm sàng</div>', unsafe_allow_html=True)

        pregnancies = st.number_input(
            "Số lần mang thai (Pregnancies)", min_value=0, max_value=20, value=1, step=1)
        st.markdown('<p class="field-hint">Nhập 0 nếu chưa từng mang thai</p>', unsafe_allow_html=True)

        glucose = st.slider("Đường huyết (Glucose) — mg/dL", 0, 200, 120)
        st.markdown(f'<p class="field-hint">Bình thường: 70–99 · Hiện tại: <b style="color:#0abfbc">{glucose}</b></p>', unsafe_allow_html=True)

        blood_pressure = st.slider("Huyết áp tâm trương (BloodPressure) — mmHg", 0, 130, 70)
        st.markdown(f'<p class="field-hint">Bình thường: 60–80 · Hiện tại: <b style="color:#0abfbc">{blood_pressure}</b></p>', unsafe_allow_html=True)

        skin_thickness = st.slider("Độ dày nếp gấp da (SkinThickness) — mm", 0, 100, 20)
        st.markdown('<p class="field-hint">Cơ đầu tam đầu; bình thường: 10–35 mm</p>', unsafe_allow_html=True)

        insulin = st.slider("Insulin huyết thanh — μU/mL", 0, 900, 80)
        st.markdown('<p class="field-hint">Bình thường lúc đói: 16–166 μU/mL</p>', unsafe_allow_html=True)

    with right:
        st.markdown('<div class="section-header">📏 Nhân trắc học</div>', unsafe_allow_html=True)

        weight    = st.number_input("Cân nặng (Weight) — kg",  min_value=1.0,  max_value=200.0, value=70.0, step=0.5)
        height_cm = st.number_input("Chiều cao (Height) — cm", min_value=50.0, max_value=250.0, value=165.0, step=0.5)

        height_m = height_cm / 100.0
        bmi      = weight / (height_m ** 2) if height_m > 0 else 0.0
        bmi_col  = "#0abfbc" if 18.5 <= bmi < 25 else ("#e4b95b" if bmi < 30 else "#e05c6e")
        bmi_lbl  = ("Bình thường" if 18.5 <= bmi < 25
                    else ("Thừa cân" if bmi < 30
                          else ("Béo phì" if bmi >= 30 else "Gầy")))

        st.markdown(f"""
        <div style="background:#1a2e4a;border:1px solid rgba(10,191,188,0.18);
             border-radius:12px;padding:14px 18px;display:flex;
             align-items:center;justify-content:space-between;margin-bottom:14px;">
            <div>
                <div style="font-size:11px;color:#7a93b4;margin-bottom:2px;">Chỉ số BMI (tính tự động)</div>
                <div style="font-family:'Playfair Display',serif;font-size:30px;
                     color:{bmi_col};font-weight:700;">{bmi:.1f}</div>
            </div>
            <div style="text-align:right;">
                <div style="font-size:13px;color:{bmi_col};font-weight:600;">{bmi_lbl}</div>
                <div style="font-size:11px;color:#7a93b4;margin-top:3px;">{weight:.1f} kg / {height_cm:.0f} cm</div>
            </div>
        </div>
        <div style="height:8px;background:rgba(255,255,255,0.07);border-radius:4px;
             overflow:hidden;margin-bottom:18px;">
            <div style="height:100%;width:{min(bmi/40*100,100):.0f}%;
                 background:linear-gradient(90deg,#0abfbc,{bmi_col});border-radius:4px;"></div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="section-header" style="margin-top:18px;">🧬 Di truyền & tuổi</div>',
                    unsafe_allow_html=True)

        dpf = st.number_input("Chức năng phả hệ tiểu đường (DPF)",
                               min_value=0.0, max_value=3.0, value=0.5, step=0.01)
        st.markdown('<p class="field-hint">Điểm cao = tiền sử gia đình nặng hơn</p>', unsafe_allow_html=True)

        age = st.number_input("Tuổi (Age)", min_value=1, max_value=120, value=30, step=1)

        # Summary chips
        st.markdown(f"""
        <div style="background:rgba(10,191,188,0.06);border:1px solid rgba(10,191,188,0.14);
             border-radius:10px;padding:12px 16px;margin-top:18px;">
            <div style="font-size:11px;color:#7a93b4;margin-bottom:8px;
                 font-weight:600;text-transform:uppercase;letter-spacing:0.06em;">Tóm tắt</div>
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:4px 14px;
                 font-size:12px;color:#c8d6e8;">
                <span>🩸 Glucose: <b style="color:#eef2f7">{glucose}</b></span>
                <span>💉 Insulin: <b style="color:#eef2f7">{insulin}</b></span>
                <span>❤️ BP: <b style="color:#eef2f7">{blood_pressure}</b></span>
                <span>📐 Skin: <b style="color:#eef2f7">{skin_thickness}</b></span>
                <span>🧬 DPF: <b style="color:#eef2f7">{dpf}</b></span>
                <span>🎂 Tuổi: <b style="color:#eef2f7">{age}</b></span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── Buttons ────────────────────────────────────────────────────────────
    st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
    _, btn_col, _ = st.columns([2, 4, 2])
    with btn_col:
        predict_btn = st.button("🚀  Phân tích & Xem kết quả AI", type="primary", use_container_width=True)

    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
    _, back_col, _ = st.columns([2, 4, 2])
    with back_col:
        if st.button("← Quay về trang chủ", use_container_width=True):
            st.session_state["page"] = "home"
            st.rerun()

    # ── Popup result ───────────────────────────────────────────────────────
    if predict_btn:
        model, scaler = _load_model_scaler()
        if model and scaler:
            arr   = np.array([[pregnancies, glucose, blood_pressure,
                                skin_thickness, insulin, bmi, dpf, age]])
            prob  = float(model.predict(scaler.transform(arr))[0][0])
            color, level_txt, emoji = _risk(prob)
            pct   = prob * 100

            # Advice
            if prob < 0.3:
                advice = """
                <ul style="padding-left:18px;color:#c8d6e8;font-size:13px;line-height:1.9;margin-top:10px;">
                    <li><b style="color:#eef2f7">Duy trì phong độ:</b> Chỉ số đang ở trạng thái lý tưởng. Tiếp tục chế độ ăn cân bằng.</li>
                    <li><b style="color:#eef2f7">Hoạt động thể chất:</b> Duy trì ≥150 phút/tuần (chạy bộ, bơi, đạp xe).</li>
                    <li><b style="color:#eef2f7">Kiểm tra định kỳ:</b> Đo đường huyết trong các kỳ khám tổng quát hàng năm.</li>
                </ul>"""
            elif prob < 0.7:
                advice = """
                <ul style="padding-left:18px;color:#c8d6e8;font-size:13px;line-height:1.9;margin-top:10px;">
                    <li><b style="color:#eef2f7">Cảnh báo sớm:</b> Chỉ số nằm trong vùng tiền tiểu đường. Cần thay đổi lối sống ngay.</li>
                    <li><b style="color:#eef2f7">Điều chỉnh ăn uống:</b> Hạn chế carbohydrate tinh chế; tăng rau xanh và chất xơ.</li>
                    <li><b style="color:#eef2f7">Kiểm soát cân nặng:</b> Giảm 5–7% trọng lượng nếu BMI đang thừa cân.</li>
                </ul>"""
            else:
                advice = """
                <ul style="padding-left:18px;color:#c8d6e8;font-size:13px;line-height:1.9;margin-top:10px;">
                    <li><b style="color:#eef2f7">Chế độ ăn:</b> Không tăng đường huyết đột ngột; chia nhỏ bữa ăn.</li>
                    <li><b style="color:#eef2f7">Cân đối dinh dưỡng:</b> Tăng rau xanh, ngũ cốc nguyên hạt; giảm tinh bột trắng.</li>
                    <li><b style="color:#eef2f7">Theo dõi:</b> Đo đường huyết sau mỗi bữa ăn và ghi chép.</li>
                    <li style="color:#e05c6e;"><b>⚠️ Khẩn cấp:</b> Gặp bác sĩ hoặc chuyên gia dinh dưỡng ngay lập tức.</li>
                </ul>"""

            st.markdown(f"""
            <div style="
                position:fixed; inset:0; z-index:9999;
                background:rgba(5,12,28,0.80); backdrop-filter:blur(5px);
                display:flex; align-items:center; justify-content:center;
                animation:fadeIn 0.2s ease;">
                <div style="
                    background:#1a2e4a; border:1.5px solid rgba(10,191,188,0.22);
                    border-radius:22px; padding:36px 32px; max-width:500px; width:92vw;
                    box-shadow:0 20px 70px rgba(0,0,0,0.55);
                    animation:slideUp 0.28s ease;">

                    <!-- Header -->
                    <div style="text-align:center; margin-bottom:22px;">
                        <div style="font-size:40px; margin-bottom:8px;">{emoji}</div>
                        <div style="font-family:'Playfair Display',serif; font-size:21px;
                             color:{color}; font-weight:700;">{level_txt}</div>
                        <div style="font-size:12px; color:#7a93b4; margin-top:3px;">
                            Xác suất mắc bệnh tiểu đường
                        </div>
                    </div>

                    <!-- Big number -->
                    <div style="text-align:center; margin-bottom:18px;">
                        <span style="font-family:'Playfair Display',serif; font-size:52px;
                               font-weight:700; color:{color};">{pct:.1f}%</span>
                    </div>

                    <!-- Risk bar -->
                    <div style="margin-bottom:18px;">
                        <div style="display:flex; justify-content:space-between;
                             font-size:10px; color:#7a93b4; margin-bottom:5px;">
                            <span>Thấp</span><span>Trung bình</span><span>Cao</span>
                        </div>
                        <div style="height:9px; background:rgba(255,255,255,0.08);
                             border-radius:5px; overflow:hidden;">
                            <div style="height:100%; width:{min(pct,100):.1f}%;
                                 background:linear-gradient(90deg,#0abfbc,{color});
                                 border-radius:5px;"></div>
                        </div>
                    </div>

                    <!-- Chips -->
                    <div style="display:flex; flex-wrap:wrap; gap:7px; margin-bottom:16px;">
                        {"".join(f'<span style="background:rgba(10,191,188,0.09);border:1px solid rgba(10,191,188,0.20);border-radius:999px;padding:4px 11px;font-size:11.5px;color:#7a93b4;">{v}</span>' for v in [f"BMI {bmi:.1f}", f"Glucose {glucose}", f"Tuổi {age}", f"Insulin {insulin}"])}
                    </div>

                    <!-- Advice -->
                    <div style="background:rgba(11,22,40,0.55); border-radius:12px; padding:14px 16px;">
                        <div style="font-size:12.5px; font-weight:600; color:#eef2f7; margin-bottom:4px;">
                            📋 Lời khuyên sức khỏe
                        </div>
                        {advice}
                    </div>

                    <div style="margin-top:14px; font-size:11px; color:#7a93b4; text-align:center;">
                        ⚠️ Kết quả AI — không thay thế chẩn đoán y tế chuyên nghiệp.
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
            _, close_col, _ = st.columns([2, 4, 2])
            with close_col:
                if st.button("✕  Đóng kết quả", key="close_modal", use_container_width=True):
                    st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)
