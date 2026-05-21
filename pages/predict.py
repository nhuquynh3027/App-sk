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

        # Fix: thử nhiều đường dẫn import khác nhau
        km_load = None
        errors  = []
        for import_path in [
            "tensorflow.keras.models",
            "keras.models",
            "keras.saving",
        ]:
            try:
                import importlib
                mod = importlib.import_module(import_path)
                km_load = mod.load_model
                break
            except Exception as ex:
                errors.append(f"{import_path}: {ex}")

        if km_load is None:
            st.error(f"Không thể import Keras. Lỗi:\n" + "\n".join(errors))
            return None, None

        base        = os.path.dirname(os.path.dirname(__file__))
        model_path  = os.path.join(base, "models", "diabetes_model.h5")
        scaler_path = os.path.join(base, "models", "scaler.pkl")

        if not os.path.exists(model_path):
            st.error(f"❌ Không tìm thấy file mô hình tại: `{model_path}`\n\n"
                     f"Hãy đặt `diabetes_model.h5` vào thư mục `models/`")
            return None, None
        if not os.path.exists(scaler_path):
            st.error(f"❌ Không tìm thấy scaler tại: `{scaler_path}`\n\n"
                     f"Hãy đặt `scaler.pkl` vào thư mục `models/`")
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
    if prob < 0.3:  return "#10b981", "#d1fae5", "NGUY CƠ THẤP",       "✅"
    if prob < 0.7:  return "#f59e0b", "#fef3c7", "NGUY CƠ TRUNG BÌNH", "⚠️"
    return               "#ef4444", "#fee2e2", "NGUY CƠ CAO",          "🚨"


def show():
    _load_css()

    user    = st.session_state.get("user_name", "Người dùng")
    initial = user[0].upper() if user else "U"

    # ── Topnav ─────────────────────────────────────────────────────────────
    st.markdown(f"""
    <div class="topnav">
        <div class="topnav-brand">🏥 Health<span>AI</span></div>
        <div class="topnav-user">
            <span style="color:#334155;">{user}</span>
            <div class="topnav-avatar">{initial}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Page header ────────────────────────────────────────────────────────
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

    # ── Centered content wrapper ───────────────────────────────────────────
    _, main_col, _ = st.columns([1, 8, 1])

    with main_col:
        left, gap, right = st.columns([5, 0.5, 5])

        # ────────────────── LEFT COLUMN ──────────────────
        with left:
            st.markdown("""
            <div style="background:#fff;border:1.5px solid #e2e8f0;border-radius:16px;
                 padding:24px 22px 20px;box-shadow:0 2px 12px rgba(14,165,233,0.07);margin-bottom:16px;">
                <div class="section-header">📋 Thông số lâm sàng</div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown('<div style="background:#fff;border:1.5px solid #e2e8f0;border-radius:16px;padding:24px 22px;box-shadow:0 2px 12px rgba(14,165,233,0.07);">', unsafe_allow_html=True)
            st.markdown('<div class="section-header">📋 Thông số lâm sàng</div>', unsafe_allow_html=True)

            pregnancies = st.number_input(
                "Số lần mang thai (Pregnancies)", min_value=0, max_value=20, value=1, step=1)
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

        # ────────────────── RIGHT COLUMN ──────────────────
        with right:
            st.markdown('<div style="background:#fff;border:1.5px solid #e2e8f0;border-radius:16px;padding:24px 22px;box-shadow:0 2px 12px rgba(14,165,233,0.07);">', unsafe_allow_html=True)
            st.markdown('<div class="section-header">📏 Nhân trắc học</div>', unsafe_allow_html=True)

            weight    = st.number_input("Cân nặng (Weight) — kg",  min_value=1.0,  max_value=200.0, value=70.0, step=0.5)
            height_cm = st.number_input("Chiều cao (Height) — cm", min_value=50.0, max_value=250.0, value=165.0, step=0.5)

            height_m = height_cm / 100.0
            bmi      = weight / (height_m ** 2) if height_m > 0 else 0.0
            bmi_col  = "#10b981" if 18.5 <= bmi < 25 else ("#f59e0b" if bmi < 30 else "#ef4444")
            bmi_bg   = "#d1fae5" if 18.5 <= bmi < 25 else ("#fef3c7" if bmi < 30 else "#fee2e2")
            bmi_lbl  = ("Bình thường" if 18.5 <= bmi < 25
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
            <div style="height:8px;background:#f1f5f9;border-radius:4px;overflow:hidden;margin-bottom:18px;">
                <div style="height:100%;width:{min(bmi/40*100,100):.0f}%;
                     background:linear-gradient(90deg,#0ea5e9,{bmi_col});border-radius:4px;"></div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown('<div class="section-header" style="margin-top:4px;">🧬 Di truyền & tuổi</div>', unsafe_allow_html=True)

            dpf = st.number_input("Chức năng phả hệ tiểu đường (DPF)",
                                   min_value=0.0, max_value=3.0, value=0.5, step=0.01)
            st.markdown('<p class="field-hint">Điểm cao = tiền sử gia đình nặng hơn</p>', unsafe_allow_html=True)

            age = st.number_input("Tuổi (Age)", min_value=1, max_value=120, value=30, step=1)

            # Summary
            st.markdown(f"""
            <div style="background:#f8fafc;border:1px solid #e2e8f0;
                 border-radius:10px;padding:14px 16px;margin-top:16px;">
                <div style="font-size:11px;color:#64748b;margin-bottom:8px;
                     font-weight:700;text-transform:uppercase;letter-spacing:0.06em;">📊 Tóm tắt</div>
                <div style="display:grid;grid-template-columns:1fr 1fr;gap:5px 14px;font-size:12.5px;color:#334155;">
                    <span>🩸 Glucose: <b>{glucose}</b></span>
                    <span>💉 Insulin: <b>{insulin}</b></span>
                    <span>❤️ BP: <b>{blood_pressure}</b></span>
                    <span>📐 Skin: <b>{skin_thickness}</b></span>
                    <span>🧬 DPF: <b>{dpf}</b></span>
                    <span>🎂 Tuổi: <b>{age}</b></span>
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)

        # ── Action buttons ─────────────────────────────────────────────────
        st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)
        _, btn_mid, _ = st.columns([1, 4, 1])
        with btn_mid:
            predict_btn = st.button(
                "🚀  Phân tích & Xem kết quả AI",
                type="primary", use_container_width=True, key="do_predict")
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        _, back_mid, _ = st.columns([1, 4, 1])
        with back_mid:
            if st.button("← Quay về trang chủ", use_container_width=True, key="go_home"):
                st.session_state["page"] = "home"
                st.rerun()

        # ── Prediction result ──────────────────────────────────────────────
        if predict_btn:
            with st.spinner("🔬 AI đang phân tích..."):
                model, scaler = _load_model_scaler()

            if model and scaler:
                arr   = np.array([[pregnancies, glucose, blood_pressure,
                                    skin_thickness, insulin, bmi, dpf, age]])
                prob  = float(model.predict(scaler.transform(arr))[0][0])
                color, bg_col, level_txt, emoji = _risk(prob)
                pct   = prob * 100

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

                advice_html = "".join(
                    f'<div style="display:flex;gap:10px;padding:8px 0;border-bottom:1px solid #f1f5f9;">'
                    f'<div style="min-width:160px;font-weight:700;color:#0f172a;font-size:12.5px;">{t}</div>'
                    f'<div style="color:#475569;font-size:12.5px;">{d}</div></div>'
                    for t, d in advice_items
                )

                # Overlay popup
                st.markdown(f"""
                <div style="position:fixed;inset:0;z-index:9999;
                     background:rgba(15,23,42,0.55);backdrop-filter:blur(6px);
                     display:flex;align-items:center;justify-content:center;
                     animation:fadeIn 0.2s ease;">
                    <div style="background:#fff;border-radius:22px;padding:36px 32px;
                         max-width:480px;width:94vw;
                         box-shadow:0 24px 80px rgba(0,0,0,0.20);
                         animation:slideUp 0.28s ease;">

                        <!-- Result header -->
                        <div style="text-align:center;margin-bottom:24px;">
                            <div style="display:inline-flex;align-items:center;justify-content:center;
                                 width:64px;height:64px;border-radius:50%;background:{bg_col};
                                 font-size:28px;margin-bottom:12px;">{emoji}</div>
                            <div style="font-family:'Lora',serif;font-size:22px;
                                 color:{color};font-weight:700;">{level_txt}</div>
                            <div style="font-size:12px;color:#64748b;margin-top:4px;">
                                Xác suất mắc bệnh tiểu đường
                            </div>
                        </div>

                        <!-- Big percent -->
                        <div style="text-align:center;margin-bottom:20px;">
                            <span style="font-family:'Lora',serif;font-size:56px;
                                   font-weight:700;color:{color};">{pct:.1f}%</span>
                        </div>

                        <!-- Risk bar -->
                        <div style="margin-bottom:20px;">
                            <div style="display:flex;justify-content:space-between;
                                 font-size:10px;color:#94a3b8;margin-bottom:5px;">
                                <span>Thấp</span><span>Trung bình</span><span>Cao</span>
                            </div>
                            <div style="height:9px;background:#f1f5f9;border-radius:5px;overflow:hidden;">
                                <div style="height:100%;width:{min(pct,100):.1f}%;
                                     background:linear-gradient(90deg,#10b981,{color});
                                     border-radius:5px;transition:width 0.5s;"></div>
                            </div>
                        </div>

                        <!-- Chips -->
                        <div style="display:flex;flex-wrap:wrap;gap:7px;margin-bottom:18px;">
                            {"".join(f'<span style="background:#f1f5f9;border:1px solid #e2e8f0;border-radius:999px;padding:4px 12px;font-size:11.5px;color:#475569;">{v}</span>' for v in [f"BMI {bmi:.1f}", f"Glucose {glucose}", f"Tuổi {age}", f"Insulin {insulin}"])}
                        </div>

                        <!-- Advice -->
                        <div style="background:#f8fafc;border:1px solid #e2e8f0;
                             border-radius:12px;padding:14px 16px;margin-bottom:16px;">
                            <div style="font-size:12px;font-weight:700;color:#0f172a;margin-bottom:4px;">
                                📋 Lời khuyên sức khỏe
                            </div>
                            {advice_html}
                        </div>

                        <div style="font-size:11px;color:#94a3b8;text-align:center;">
                            ⚠️ Đây là kết quả AI — không thay thế chẩn đoán y tế chuyên nghiệp.
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
                _, close_col, _ = st.columns([1, 4, 1])
                with close_col:
                    if st.button("✕  Đóng kết quả", key="close_modal", use_container_width=True):
                        st.rerun()
