# WebAPI_App

Ứng dụng Streamlit để truy vấn Base.vn Candidate List API.

## 📋 Yêu cầu

- Python 3.12.x (khuyến nghị)
- `uv` package manager (hoặc `pip`)

**Lưu ý:** Python 3.14+ có thể gặp vấn đề tương thích với một số packages (đặc biệt là `pyarrow`).

## 🚀 Cài đặt

### 1. Clone repository

```bash
git clone <repository-url>
cd WebAPI_App
```

### 2. Tạo virtual environment

Sử dụng `uv`:
```bash
uv venv --python 3.12
```

Hoặc sử dụng `python`:
```bash
python -m venv .venv
```

### 3. Kích hoạt virtual environment

**Windows (PowerShell):**
```powershell
.venv\Scripts\activate
```

**Linux/Mac:**
```bash
source .venv/bin/activate
```

### 4. Cài đặt dependencies

Sử dụng `uv`:
```bash
uv pip install -r requirements.txt
```

Hoặc sử dụng `pip`:
```bash
pip install -r requirements.txt
```

## ⚙️ Cấu hình

### Thiết lập Access Token

1. Tạo file `.streamlit/secrets.toml` (nếu chưa có)
2. Thêm access token của bạn:

```toml
BASE_TOKEN = "your_actual_access_token_here"
```

**⚠️ Quan trọng:** File `secrets.toml` đã được thêm vào `.gitignore` để bảo vệ thông tin nhạy cảm.

## 🎯 Chạy ứng dụng

### Cách 1: Với virtual environment đã kích hoạt

```bash
streamlit run app.py
```

### Cách 2: Không cần kích hoạt venv (Windows)

```powershell
.venv\Scripts\python.exe -m streamlit run app.py
```

### Cách 3: Không cần kích hoạt venv (Linux/Mac)

```bash
.venv/bin/python -m streamlit run app.py
```

Ứng dụng sẽ chạy tại: http://localhost:8501

## 📂 Cấu trúc dự án

```
WebAPI_App/
├── app.py                 # Ứng dụng Streamlit chính
├── api_client.py          # Module gọi API
├── data_processor.py      # Module xử lý dữ liệu
├── requirements.txt       # Dependencies với version cụ thể
├── README.md             # File này
├── .gitignore            # Danh sách file/folder không commit
├── .streamlit/
│   └── secrets.toml      # Lưu trữ API tokens (không commit)
└── .venv/                # Virtual environment (không commit)
```

## 🔧 Tính năng

- ✅ Truy vấn Base.vn Candidate List API
- ✅ Hiển thị danh sách ứng viên dạng bảng
- ✅ Hiển thị các chỉ số tổng quan (total, count, page)
- ✅ Xem JSON response thô
- ✅ Form tương tác để nhập tham số API
- ✅ Xử lý lỗi API và kết nối

## 📦 Dependencies

- `requests==2.32.5` - HTTP client
- `pandas==2.3.3` - Data processing
- `numpy==2.3.3` - Numerical computing
- `streamlit==1.50.0` - Web framework

## 🐛 Debug

Nếu gặp lỗi khi cài đặt:

1. **Lỗi `pyarrow` không build được:**
   - Đảm bảo dùng Python 3.12.x thay vì 3.14+
   - Tạo lại venv: `uv venv --python 3.12`

2. **Lỗi `streamlit` không tìm thấy:**
   - Đảm bảo đã kích hoạt virtual environment
   - Hoặc chạy trực tiếp: `.venv\Scripts\python.exe -m streamlit run app.py`

3. **Lỗi API 401/403:**
   - Kiểm tra access token trong `.streamlit/secrets.toml`
   - Đảm bảo token còn hiệu lực

## 📝 License

Xem file `LICENSE` để biết thêm chi tiết.
```