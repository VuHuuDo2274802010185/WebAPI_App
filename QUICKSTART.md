# Quick Start Guide - WebAPI_App

## Hướng dẫn Nhanh cho Người mới bắt đầu

### Option 1: Sử dụng Setup Script (Khuyến nghị)

#### Linux/macOS:
```bash
./setup.sh
```

#### Windows:
```cmd
setup.bat
```

Script sẽ tự động:
- Kiểm tra Python version
- Cài đặt uv (nếu chưa có)
- Tạo virtual environment
- Cài đặt dependencies
- Tạo file .env từ template

### Option 2: Setup Thủ công

#### Bước 1: Cài đặt uv
```bash
pip install uv
```

#### Bước 2: Tạo Virtual Environment
```bash
uv venv
```

#### Bước 3: Kích hoạt Virtual Environment

**Linux/macOS:**
```bash
source .venv/bin/activate
```

**Windows:**
```cmd
.venv\Scripts\activate
```

#### Bước 4: Cài đặt Dependencies
```bash
uv pip install -r requirements.txt
```

#### Bước 5: Cấu hình Environment
```bash
cp .env.example .env
# Sau đó chỉnh sửa .env với credentials thực tế của bạn
```

### Chạy Ứng dụng

```bash
streamlit run app.py
```

Ứng dụng sẽ mở tại: http://localhost:8501

## Troubleshooting

### Lỗi: Python version không đủ
```
Solution: Cài đặt Python 3.12 hoặc cao hơn
```

### Lỗi: Module not found
```
Solution: Đảm bảo virtual environment đã được kích hoạt và dependencies đã được cài đặt
source .venv/bin/activate
uv pip install -r requirements.txt
```

### Lỗi: API Token không hợp lệ
```
Solution: Kiểm tra file .env và đảm bảo BASE_TOKEN đã được set đúng
```

### Lỗi: Port 8501 đã được sử dụng
```
Solution: Chạy Streamlit trên port khác
streamlit run app.py --server.port 8502
```

## Tài liệu Chi tiết

Xem [README.md](README.md) để biết thông tin chi tiết về:
- Cấu trúc dự án
- Tính năng
- API documentation
- Hướng dẫn phát triển

## Liên hệ & Hỗ trợ

Nếu gặp vấn đề, vui lòng tạo issue trên GitHub repository.
