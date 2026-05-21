"""
pages/predict.py — Trang dự đoán, giao diện sáng + fix keras import
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
        
        try:
            from tensorflow.keras.models import load_model
            km_load = load_model
        except ImportError:
            try:
                from keras.models import load_model
                km_load = load_model
            except ImportError as e:
                st.error(f"❌ Không thể import Keras/TensorFlow. Lỗi: {e}")
                return None, None

        base = os.path.dirname(os.path.dirname(__file__))
        model_path = os.path.join(base, "models", "diabetes_model.h5")
        scaler_path = os.path.join(base, "models", "scaler.pkl")

        if not os.path.exists(model_path):
            st.error(f"❌ Không tìm thấy file mô hình tại: `{model_path}`")
            return None, None
        if not os.path.exists(scaler_path):
            st.error(f"❌ Không tìm thấy scaler tại: `{scaler_path}`")
            return None, None

        try:
            _model = km_load(model_path)
            with open(scaler_path, "rb") as f:
                _scaler = pickle.load(f)
        except Exception as e:
            st.error(f"Lỗi tải mô hình: {e}")
            return None, None

    return _model, _scaler


def _risk(prob):
    if prob < 0.3:  return "#10b981", "#d1fae5", "NGUY CƠ THẤP", "✅", "Thấp"
    if prob < 0.7:  return "#f59e0b", "#fef3c7", "NGUY CƠ TRUNG BÌNH", "⚠️", "Trung bình"
    return "#ef4444", "#fee2e2", "NGUY CƠ CAO", "🚨", "Cao"


def show():
    _load_css()

    user = st.session_state.get("user_name", "Người dùng")
    initial = user[0].upper() if user else "U"

    # Topnav
    st.markdown(f"""
    <div class="topnav">
        <div class="topnav-brand">🏥 Health<span>AI</span></div>
        <div class="topnav-user">
            <span style="color:#334155;">{user}</span>
            <div class="topnav-avatar">{initial}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Page header
    st.markdown("""
    <div style="background:linear-gradient(135deg,#e0f2fe,#f0fdf4);
         border-bottom:1px solid #e2e8f0;padding:32px 24px 28px;text-align:center;">
        <div style="font-family:'Lora',serif;font-size:26px;font-weight:700;color:#0f172a;">
            🩺 Kiểm Tra Nguy Cơ Tiểu Đường
        </div>
        <p style="font-size:13px;color:#64748b;margin-top:6px;">
            Nhập các chỉ số lâm sàng — AI sẽ phân tích và hiển thị kết quả ngay lập tức
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)

    # Form nhập liệu
    _, main_col, _ = st.columns([1, 8, 1])

    with main_col:
        left, gap, right = st.columns([5, 0.5, 5])

        with left:
            st.markdown('<div style="background:#fff;border:1.5px solid #e2e8f0;border-radius:16px;padding:24px 22px;box-shadow:0 2px 12px rgba(14,165,233,0.07);">', unsafe_allow_html=True)
            st.markdown('<div class="section-header">📋 Thông số lâm sàng</div>', unsafe_allow_html=True)

            pregnancies = st.number_input("Số lần mang thai (Pregnancies)", min_value=0, max_value=20, value=1, step=1)
            st.markdown('<p class="field-hint">Nhập 0 nếu chưa từng mang thai</p>', unsafe_allow_html=True)

            glucose = st.slider("Đường huyết (Glucose) — mg/dL", 0, 200, 120)
            st.markdown(f'<p class="field-hint">Bình thường: 70–99 · Hiện tại: <b style="color:#0ea5e9">{glucose}</b></p>', unsafe_allow_html=True)

            blood_pressure = st.slider("Huyết áp tâm trương (BloodPressure) — mmHg", 0, 130, 70)
            st.markdown(f'<p class="field-hint">Bình thường: 60–80 · Hiện tại: <b style="color:#0ea5e9">{blood_pressure}</b></p>', unsafe_allow_html=True)

            skin_thickness = st.slider("Độ dày nếp gấp da (SkinThickness) — mm", 0, 100, 20)
            st.markdown('<p class="field-hint">Cơ đầu tam đầu; bình thường: 10–35 mm</p>', unsafe_allow_html=True)

            insulin = st.slider("Insulin huyết thanh — μU/mL", 0, 900, 80)
            st.markdown('<p class="field-hint">Bình thường lúc đói: 16–166 μU/mL</p>', unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)

        with right:
            st.markdown('<div style="background:#fff;border:1.5px solid #e2e8f0;border-radius:16px;padding:24px 22px;box-shadow:0 2px 12px rgba(14,165,233,0.07);">', unsafe_allow_html=True)
            st.markdown('<div class="section-header">📏 Nhân trắc học</div>', unsafe_allow_html=True)

            weight = st.number_input("Cân nặng (Weight) — kg", min_value=1.0, max_value=200.0, value=70.0, step=0.5)
            height_cm = st.number_input("Chiều cao (Height) — cm", min_value=50.0, max_value=250.0, value=165.0, step=0.5)

            height_m = height_cm / 100.0
            bmi = weight / (height_m ** 2) if height_m > 0 else 0.0
            bmi_col = "#10b981" if 18.5 <= bmi < 25 else ("#f59e0b" if bmi < 30 else "#ef4444")
            bmi_bg = "#d1fae5" if 18.5 <= bmi < 25 else ("#fef3c7" if bmi < 30 else "#fee2e2")
            bmi_lbl = ("Bình thường" if 18.5 <= bmi < 25
                       else ("Thừa cân" if bmi < 30
                             else ("Béo phì" if bmi >= 30 else "Thiếu cân")))

            st.markdown(f"""
            <div style="background:{bmi_bg};border:1.5px solid {bmi_col}33;
                 border-radius:12px;padding:14px 18px;display:flex;
                 align-items:center;justify-content:space-between;margin-bottom:14px;">
                <div>
                    <div style="font-size:11px;color:#64748b;margin-bottom:2px;">Chỉ số BMI (tự động)</div>
                    <div style="font-family:'Lora',serif;font-size:30px;
                         color:{bmi_col};font-weight:700;">{bmi:.1f}</div>
                </div>
                <div style="text-align:right;">
                    <div style="font-size:13px;color:{bmi_col};font-weight:700;">{bmi_lbl}</div>
                    <div style="font-size:11px;color:#64748b;margin-top:3px;">{weight:.1f} kg / {height_cm:.0f} cm</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown('<div class="section-header" style="margin-top:4px;">🧬 Di truyền & tuổi</div>', unsafe_allow_html=True)

            dpf = st.number_input("Chức năng phả hệ tiểu đường (DPF)", min_value=0.0, max_value=3.0, value=0.5, step=0.01)
            st.markdown('<p class="field-hint">Điểm cao = tiền sử gia đình nặng hơn</p>', unsafe_allow_html=True)

            age = st.number_input("Tuổi (Age)", min_value=1, max_value=120, value=30, step=1)

            st.markdown('</div>', unsafe_allow_html=True)

        # Buttons
        st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)
        _, btn_mid, _ = st.columns([1, 4, 1])
        with btn_mid:
            predict_btn = st.button("🚀 Phân tích & Xem kết quả AI", type="primary", use_container_width=True)

        _, back_mid, _ = st.columns([1, 4, 1])
        with back_mid:
            if st.button("← Quay về trang chủ", use_container_width=True):
                st.session_state["page"] = "home"
                st.rerun()

        # XỬ LÝ DỰ ĐOÁN - Dùng dialog
        if predict_btn:
            with st.spinner("🔬 AI đang phân tích..."):
                model, scaler = _load_model_scaler()

            if model and scaler:
                arr = np.array([[pregnancies, glucose, blood_pressure,
                                skin_thickness, insulin, bmi, dpf, age]])
                prob = float(model.predict(scaler.transform(arr))[0][0])
                color, bg_col, level_txt, emoji, risk_text = _risk(prob)
                pct = prob * 100

                # Lưu kết quả vào session state
                st.session_state['show_result_dialog'] = True
                st.session_state['result'] = {
                    'pct': pct, 'color': color, 'bg_col': bg_col,
                    'level_txt': level_txt, 'emoji': emoji,
                    'bmi': bmi, 'glucose': glucose, 'age': age,
                    'insulin': insulin, 'risk_text': risk_text
                }
                st.rerun()

# Hiển thị dialog kết quả bên ngoài form
if st.session_state.get('show_result_dialog', False):
    result = st.session_state['result']
    
    # Tạo lời khuyên
    if result['pct'] < 30:
        advice_items = [
            ("✅ Duy trì phong độ", "Chỉ số đang lý tưởng. Tiếp tục chế độ ăn cân bằng."),
            ("🏃 Hoạt động thể chất", "Duy trì ≥150 phút/tuần (chạy bộ, bơi, đạp xe)."),
            ("🗓️ Kiểm tra định kỳ", "Đo đường huyết trong các kỳ khám tổng quát hàng năm."),
        ]
    elif result['pct'] < 70:
        advice_items = [
            ("⚠️ Cảnh báo sớm", "Chỉ số nằm trong vùng tiền tiểu đường — cần thay đổi lối sống."),
            ("🥗 Điều chỉnh ăn uống", "Hạn chế carbs tinh chế; tăng rau xanh và chất xơ."),
            ("⚖️ Kiểm soát cân nặng", "Giảm 5–7% trọng lượng nếu BMI đang thừa cân."),
        ]
    else:
        advice_items = [
            ("🚨 Cần gặp bác sĩ ngay", "Mức nguy cơ cao — hãy đến cơ sở y tế sớm nhất."),
            ("🍽️ Chế độ ăn nghiêm ngặt", "Chia nhỏ bữa ăn, không để đường huyết tăng đột ngột."),
            ("📊 Theo dõi mỗi ngày", "Đo đường huyết sau mỗi bữa ăn và ghi chép."),
        ]
    
    # Hiển thị dialog
    with st.container():
        st.markdown("---")
        st.markdown(f"""
        <div style="position:fixed;top:50%;left:50%;transform:translate(-50%,-50%);
                    z-index:1000;width:450px;max-width:90%;
                    background:white;border-radius:20px;
                    box-shadow:0 20px 60px rgba(0,0,0,0.3);
                    padding:30px;">
            <div style="text-align:center;">
                <div style="font-size:60px;">{result['emoji']}</div>
                <div style="font-size:24px;font-weight:bold;color:{result['color']};margin:10px 0;">
                    {result['level_txt']}
                </div>
                <div style="font-size:13px;color:#64748b;">Xác suất mắc bệnh tiểu đường</div>
                <div style="font-size:56px;font-weight:bold;color:{result['color']};margin:15px 0;">
                    {result['pct']:.1f}%
                </div>
                <div style="background:#e2e8f0;border-radius:10px;height:10px;margin:15px 0;">
                    <div style="background:{result['color']};width:{result['pct']}%;height:100%;border-radius:10px;"></div>
                </div>
                <div style="display:flex;justify-content:space-between;font-size:11px;color:#64748b;margin-bottom:15px;">
                    <span>Thấp</span><span>Trung bình</span><span>Cao</span>
                </div>
                <div style="display:flex;flex-wrap:wrap;gap:8px;justify-content:center;margin:15px 0;">
                    <span style="background:#f1f5f9;border-radius:20px;padding:5px 12px;font-size:12px;">BMI {result['bmi']:.1f}</span>
                    <span style="background:#f1f5f9;border-radius:20px;padding:5px 12px;font-size:12px;">Glucose {result['glucose']}</span>
                    <span style="background:#f1f5f9;border-radius:20px;padding:5px 12px;font-size:12px;">Tuổi {result['age']}</span>
                    <span style="background:#f1f5f9;border-radius:20px;padding:5px 12px;font-size:12px;">Insulin {result['insulin']}</span>
                </div>
                <div style="background:#f8fafc;border-radius:12px;padding:15px;margin:15px 0;text-align:left;">
                    <div style="font-weight:bold;margin-bottom:10px;">📋 Lời khuyên sức khỏe</div>
                    {"".join(f'<div style="padding:8px 0;border-bottom:1px solid #e2e8f0;"><div style="font-weight:bold;font-size:13px;">{t}</div><div style="font-size:12px;color:#475569;">{d}</div></div>' for t,d in advice_items)}
                </div>
                <div style="font-size:10px;color:#94a3b8;text-align:center;">⚠️ Đây là kết quả AI — không thay thế chẩn đoán y tế</div>
            </div>
        </div>
        <div style="position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,0.5);z-index:999;"></div>
        """, unsafe_allow_html=True)
        
        # Nút đóng
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("✕ Đóng", use_container_width=True, key="close_dialog"):
                st.session_state['show_result_dialog'] = False
                st.rerun()