# 🚀 Hướng dẫn Nhanh

## Bước 1: Tạo Virtual Environment
```powershell
uv venv --python 3.12
```

## Bước 2: Cài đặt Dependencies
```powershell
uv pip install -r requirements.txt
```

## Bước 3: Cấu hình Token
Chỉnh sửa file `.streamlit/secrets.toml`:
```toml
BASE_TOKEN = "your_actual_token_here"
```

## Bước 4: Chạy Ứng dụng
```powershell
.venv\Scripts\python.exe -m streamlit run app.py
```

Hoặc nếu đã kích hoạt venv:
```powershell
.venv\Scripts\activate
streamlit run app.py
```

## 🌐 Mở trình duyệt
Truy cập: http://localhost:8501

---

## ⚡ Lệnh One-liner (không cần kích hoạt venv)

**Windows PowerShell:**
```powershell
.venv\Scripts\python.exe -m streamlit run app.py
```

**Linux/Mac:**
```bash
.venv/bin/python -m streamlit run app.py
```
