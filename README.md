# WebAPI_App

Ứng dụng Streamlit để truy vấn Base.vn Candidate List API và hiển thị dữ liệu ứng viên.

## Yêu cầu Hệ thống

- **Python**: 3.12 hoặc cao hơn
- **Package Manager**: `uv` (khuyến nghị) hoặc `pip`

## Cài đặt

### 1. Cài đặt uv (khuyến nghị)

`uv` là một package manager Python hiện đại, nhanh hơn và hiệu quả hơn pip.

```bash
pip install uv
```

### 2. Tạo Virtual Environment

```bash
# Sử dụng uv (khuyến nghị)
uv venv

# Hoặc sử dụng venv truyền thống
python -m venv .venv
```

### 3. Kích hoạt Virtual Environment

**Linux/macOS:**
```bash
source .venv/bin/activate
```

**Windows:**
```cmd
.venv\Scripts\activate
```

### 4. Cài đặt Dependencies

```bash
# Sử dụng uv (nhanh hơn)
uv pip install -r requirements.txt

# Hoặc sử dụng pip truyền thống
pip install -r requirements.txt
```

## Cấu hình

1. Tạo file `.env` trong thư mục gốc của dự án (file này sẽ không được commit)
2. Thêm các biến môi trường sau:

```env
BASE_TOKEN=your_api_token_here
OPENING_ID=9346
STAGE_ID=75440
NUM_PER_PAGE=50
```

**Lưu ý:** File `.env` đã được thêm vào `.gitignore` để bảo vệ thông tin nhạy cảm.

## Chạy Ứng dụng

```bash
# Đảm bảo virtual environment đã được kích hoạt
streamlit run app.py
```

Ứng dụng sẽ mở tự động trong trình duyệt tại địa chỉ `http://localhost:8501`

## Cấu trúc Dự án

```
WebAPI_App/
├── app.py              # File chính của ứng dụng Streamlit
├── api_client.py       # Module xử lý API requests
├── data_processor.py   # Module xử lý và format dữ liệu
├── requirements.txt    # Danh sách dependencies
├── .env               # File cấu hình (không commit)
├── .gitignore         # Loại trừ các file không cần thiết
└── README.md          # Tài liệu hướng dẫn
```

## Tính năng

- ✅ Truy vấn API Base.vn để lấy danh sách ứng viên
- ✅ Hiển thị dữ liệu dưới dạng bảng với pandas DataFrame
- ✅ Lưu cấu hình vào file `.env`
- ✅ Giao diện thân thiện với Streamlit
- ✅ Xử lý lỗi và validation

## Dependencies

- `streamlit`: Framework web app
- `requests`: HTTP client
- `pandas`: Data processing
- `numpy`: Numerical computing
- `python-dotenv`: Environment variable management

## Phát triển

Để đóng góp vào dự án:

1. Fork repository
2. Tạo branch mới (`git checkout -b feature/AmazingFeature`)
3. Commit thay đổi (`git commit -m 'Add some AmazingFeature'`)
4. Push lên branch (`git push origin feature/AmazingFeature`)
5. Tạo Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.

