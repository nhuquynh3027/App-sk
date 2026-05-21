"""
pages/predict.py — Trang dự đoán, hiển thị kết quả trực tiếp
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
    if prob < 0.3:  
        return "#10b981", "#d1fae5", "NGUY CƠ THẤP", "✅", "Thấp"
    if prob < 0.7:  
        return "#f59e0b", "#fef3c7", "NGUY CƠ TRUNG BÌNH", "⚠️", "Trung bình"
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

    # Kiểm tra xem có đang hiển thị kết quả không
    if st.session_state.get("show_result", False):
        # HIỂN THỊ KẾT QUẢ
        result = st.session_state["result_data"]
        
        st.markdown("""
        <div style="background:linear-gradient(135deg,#e0f2fe,#f0fdf4);
             border-bottom:1px solid #e2e8f0;padding:32px 24px 28px;text-align:center;">
            <div style="font-family:'Lora',serif;font-size:26px;font-weight:700;color:#0f172a;">
                📊 Kết Quả Phân Tích
            </div>
            <p style="font-size:13px;color:#64748b;margin-top:6px;">
                Dựa trên các chỉ số bạn đã nhập
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)
        
        # Card kết quả chính
        _, main_col, _ = st.columns([1, 6, 1])
        with main_col:
            # Hiển thị kết quả
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.markdown(f"""
                <div style="background:{result['bg_col']}; border-radius:20px; padding:30px; text-align:center;">
                    <div style="font-size:64px;">{result['emoji']}</div>
                    <div style="font-size:28px; font-weight:700; color:{result['color']}; margin:10px 0;">
                        {result['level_txt']}
                    </div>
                    <div style="font-size:13px; color:#64748b;">Xác suất mắc bệnh tiểu đường</div>
                    <div style="font-size:64px; font-weight:700; color:{result['color']}; margin:15px 0;">
                        {result['pct']:.1f}%
                    </div>
                    <div style="background:#e2e8f0; border-radius:10px; height:10px; margin:15px 0; overflow:hidden;">
                        <div style="background:{result['color']}; width:{result['pct']}%; height:100%; border-radius:10px;"></div>
                    </div>
                    <div style="display:flex; justify-content:space-between; font-size:11px; color:#64748b;">
                        <span>Thấp</span><span>Trung bình</span><span>Cao</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div style="background:white; border:1px solid #e2e8f0; border-radius:20px; padding:30px;">
                    <div style="font-weight:700; margin-bottom:15px;">📊 Các chỉ số của bạn</div>
                    <div style="display:grid; grid-template-columns:1fr 1fr; gap:12px;">
                        <div><span style="color:#64748b;">BMI:</span><br><b>{result['bmi']:.1f}</b></div>
                        <div><span style="color:#64748b;">Glucose:</span><br><b>{result['glucose']}</b></div>
                        <div><span style="color:#64748b;">Huyết áp:</span><br><b>{result['bp']}</b></div>
                        <div><span style="color:#64748b;">Insulin:</span><br><b>{result['insulin']}</b></div>
                        <div><span style="color:#64748b;">Tuổi:</span><br><b>{result['age']}</b></div>
                        <div><span style="color:#64748b;">DPF:</span><br><b>{result['dpf']}</b></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            # Lời khuyên
            st.markdown("---")
            st.markdown("### 💡 Lời khuyên sức khỏe")
            
            advice_items = result['advice_items']
            for title, desc in advice_items:
                with st.expander(title):
                    st.write(desc)
            
            # Nút Kiểm tra lại
            st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
            col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
            with col_btn2:
                if st.button("🔄 Kiểm tra lại", type="primary", use_container_width=True):
                    st.session_state["show_result"] = False
                    st.session_state.pop("result_data", None)
                    st.rerun()
            
            # Nút về trang chủ
            _, back_col, _ = st.columns([1, 2, 1])
            with back_col:
                if st.button("🏠 Về trang chủ", use_container_width=True):
                    st.session_state["page"] = "home"
                    st.session_state["show_result"] = False
                    st.rerun()
    
    else:
        # HIỂN THỊ FORM NHẬP LIỆU BAN ĐẦU
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
                # Bỏ khung trắng, chỉ giữ tiêu đề
                st.markdown("""
                <div style="font-family:'Lora',serif; font-size:22px; font-weight:700; 
                     color:#0f172a; margin-bottom:20px; display:flex; align-items:center; gap:10px;">
                    📋 Thông số lâm sàng
                </div>
                """, unsafe_allow_html=True)

                pregnancies = st.number_input("Số lần mang thai", min_value=0, max_value=20, value=1, step=1)
                glucose = st.slider("Đường huyết (mg/dL)", 0, 200, 120)
                blood_pressure = st.slider("Huyết áp tâm trương (mmHg)", 0, 130, 70)
                skin_thickness = st.slider("Độ dày nếp gấp da (mm)", 0, 100, 20)
                insulin = st.slider("Insulin (μU/mL)", 0, 900, 80)

            with right:
                st.markdown("""
                <div style="font-family:'Lora',serif; font-size:22px; font-weight:700; 
                     color:#0f172a; margin-bottom:20px; display:flex; align-items:center; gap:10px;">
                    📏 Nhân trắc học &amp; Tuổi
                </div>
                """, unsafe_allow_html=True)

                weight = st.number_input("Cân nặng (kg)", min_value=1.0, max_value=200.0, value=70.0, step=0.5)
                height_cm = st.number_input("Chiều cao (cm)", min_value=50.0, max_value=250.0, value=165.0, step=0.5)

                height_m = height_cm / 100.0
                bmi = weight / (height_m ** 2) if height_m > 0 else 0.0
                
                # Tính màu cho BMI dựa vào giá trị
                if bmi < 18.5:
                    bmi_color = "#f59e0b"  # Vàng - Thiếu cân
                    bmi_bg = "#fef3c7"
                    bmi_label = "Thiếu cân"
                elif bmi < 25:
                    bmi_color = "#10b981"  # Xanh - Bình thường
                    bmi_bg = "#d1fae5"
                    bmi_label = "Bình thường"
                elif bmi < 30:
                    bmi_color = "#f59e0b"  # Vàng - Thừa cân
                    bmi_bg = "#fef3c7"
                    bmi_label = "Thừa cân"
                else:
                    bmi_color = "#ef4444"  # Đỏ - Béo phì
                    bmi_bg = "#fee2e2"
                    bmi_label = "Béo phì"
                
                st.markdown(f"""
                <div style="background:{bmi_bg}; border-radius:12px; padding:14px 18px; margin:10px 0;
                     display:flex; align-items:center; justify-content:space-between;">
                    <div>
                        <div style="font-size:11px; color:#64748b; margin-bottom:2px;">Chỉ số BMI (tự động)</div>
                        <div style="font-family:'Lora',serif; font-size:32px; font-weight:700; color:{bmi_color};">{bmi:.1f}</div>
                    </div>
                    <div style="text-align:right;">
                        <div style="font-size:13px; font-weight:700; color:{bmi_color};">{bmi_label}</div>
                        <div style="font-size:11px; color:#64748b; margin-top:3px;">{weight:.1f} kg / {height_cm:.0f} cm</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                dpf = st.number_input("Chức năng phả hệ tiểu đường (DPF)", min_value=0.0, max_value=3.0, value=0.5, step=0.01)
                age = st.number_input("Tuổi", min_value=1, max_value=120, value=30, step=1)
                
            
            # Nút phân tích
            st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)
            _, btn_mid, _ = st.columns([1, 4, 1])
            with btn_mid:
                predict_btn = st.button("🚀 Phân tích & Xem kết quả", type="primary", use_container_width=True)

            _, back_mid, _ = st.columns([1, 4, 1])
            with back_mid:
                if st.button("← Quay về trang chủ", use_container_width=True):
                    st.session_state["page"] = "home"
                    st.rerun()

            # Xử lý dự đoán
            if predict_btn:
                with st.spinner("🔬 AI đang phân tích..."):
                    model, scaler = _load_model_scaler()

                if model and scaler:
                    arr = np.array([[pregnancies, glucose, blood_pressure,
                                    skin_thickness, insulin, bmi, dpf, age]])
                    prob = float(model.predict(scaler.transform(arr))[0][0])
                    color, bg_col, level_txt, emoji, _ = _risk(prob)
                    pct = prob * 100

                    # Tạo lời khuyên
                    if prob < 0.3:
                        advice_items = [
                            ("✅ Duy trì phong độ", "Chỉ số đang lý tưởng. Tiếp tục chế độ ăn cân bằng."),
                            ("🏃 Hoạt động thể chất", "Duy trì ≥150 phút/tuần (chạy bộ, bơi, đạp xe)."),
                            ("🗓️ Kiểm tra định kỳ", "Đo đường huyết trong các kỳ khám tổng quát hàng năm."),
                        ]
                    elif prob < 0.7:
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

                    # Lưu kết quả vào session state
                    st.session_state["show_result"] = True
                    st.session_state["result_data"] = {
                        "pct": pct, "color": color, "bg_col": bg_col,
                        "level_txt": level_txt, "emoji": emoji,
                        "bmi": bmi, "glucose": glucose, "bp": blood_pressure,
                        "insulin": insulin, "age": age, "dpf": dpf,
                        "advice_items": advice_items
                    }
                    st.rerun()