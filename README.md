# 🏥 HealthAI — Hệ Thống Dự Đoán Tiểu Đường

Ứng dụng Streamlit đa trang với giao diện **Luxury Medical Dark** (Navy + Teal).

## Cấu trúc thư mục

```
diabetes_app/
│
├── main.py                  ← Entry point (chạy file này)
│
├── assets/
│   ├── style.css            ← Toàn bộ CSS/thiết kế chung
│   ├── anh_1.jpg            ← (tuỳ chọn) Ảnh thực tế cho gallery
│   ├── anh_2.jpg
│   └── anh_n.jpg            ← Thêm bao nhiêu ảnh cũng được
│
├── models/
│   ├── diabetes_model.h5    ← Mô hình Keras đã train
│   └── scaler.pkl           ← StandardScaler đã fit
│
└── pages/
    ├── __init__.py
    ├── login.py             ← Trang đăng nhập
    ├── home.py              ← Trang chủ + gallery ảnh
    └── predict.py           ← Form nhập liệu + popup kết quả
```

## Cách chạy

```bash
# Cài dependencies
pip install streamlit keras tensorflow scikit-learn pandas numpy

# Chạy ứng dụng
streamlit run main.py
```

## Tài khoản demo

| Email                  | Mật khẩu    | Vai trò      |
|------------------------|-------------|--------------|
| admin@health.ai        | health2024  | Quản trị     |
| doctor@health.ai       | doctor123   | Bác sĩ demo  |
| patient@health.ai      | patient123  | Bệnh nhân    |

## Thêm ảnh vào gallery

Đặt file ảnh vào thư mục `assets/` với tên `anh_1.jpg`, `anh_2.jpg`, … `anh_n.jpg`  
(hỗ trợ `.jpg`, `.jpeg`, `.png`, `.webp`).

Nếu không có ảnh thực, hệ thống tự động hiển thị **6 ảnh SVG minh hoạ** chủ đề y tế.

## Luồng điều hướng

```
Login page  ─(đăng nhập thành công)→  Home page
Home page   ─(bấm "Bắt đầu kiểm tra")→  Predict page
Predict page ─(bấm "Phân tích")→  Popup kết quả (overlay)
Predict page ─(bấm "Quay về")→  Home page
Home page   ─(bấm "Đăng xuất")→  Login page
```

## Ghi chú

- **Logic dự đoán giữ nguyên** so với `app.py` gốc — chỉ giao diện được thiết kế lại.
- Kết quả AI hiển thị dưới dạng **popup overlay** với thanh tiến trình nguy cơ.
- CSS hoàn toàn override giao diện mặc định của Streamlit.
