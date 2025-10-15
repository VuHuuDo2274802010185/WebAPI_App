# 🚀 Hướng dẫn Nhanh

## Bước 1: Tạo Virtual Environment
```bash
# Sử dụng uv (khuyến nghị)
uv venv --python 3.12

# Hoặc sử dụng python
python -m venv .venv
```

## Bước 2: Kích hoạt Virtual Environment

**Windows PowerShell:**
```powershell
.venv\Scripts\activate
```

**Linux/Mac:**
```bash
source .venv/bin/activate
```

## Bước 3: Cài đặt Dependencies
```bash
# Sử dụng uv
uv pip install -r requirements.txt

# Hoặc sử dụng pip
pip install -r requirements.txt
```

---

## 🎯 Hai cách sử dụng

### Option 1: Web API (FastAPI) - ⭐ Khuyến nghị

Chạy REST API server để tích hợp với các ứng dụng khác:

```bash
uvicorn web_api:app --reload --port 8000
```

**Truy cập:**
- 🌐 HTML Documentation: http://localhost:8000/html
- 📄 JSON API Info: http://localhost:8000/
- 📚 Interactive Swagger UI: http://localhost:8000/docs

**Ví dụ sử dụng:**
```bash
# Lấy danh sách openings
curl -X POST 'http://localhost:8000/openings?access_token=YOUR_TOKEN&page=1&num_per_page=50'

# Lấy danh sách candidates
curl -X POST 'http://localhost:8000/candidates?access_token=YOUR_TOKEN&opening_id=9346&page=1'
```

### Option 2: Streamlit App (UI Dashboard)

Chạy giao diện web tương tác với Streamlit:

#### Cấu hình Token
Tạo file `.streamlit/secrets.toml`:
```toml
BASE_TOKEN = "your_actual_token_here"
```

#### Chạy ứng dụng
```bash
streamlit run app.py
```

**Truy cập:** http://localhost:8501

---

## ⚡ Lệnh One-liner (không cần kích hoạt venv)

### Web API (FastAPI)
**Windows:**
```powershell
.venv\Scripts\python.exe -m uvicorn web_api:app --reload --port 8000
```

**Linux/Mac:**
```bash
.venv/bin/python -m uvicorn web_api:app --reload --port 8000
```

### Streamlit App
**Windows:**
```powershell
.venv\Scripts\python.exe -m streamlit run app.py
```

**Linux/Mac:**
```bash
.venv/bin/python -m streamlit run app.py
```

---

## 📚 Tài liệu chi tiết

- **API Guide**: Xem file `API_GUIDE.md` để biết chi tiết về tất cả endpoints
- **README**: Xem file `README.md` để biết thông tin tổng quan
- **Interactive Docs**: Truy cập `/docs` khi chạy Web API
