# WebAPI_App

Ứng dụng Web API hoàn chỉnh để truy vấn danh sách ứng viên từ Base.vn API.

## Tính năng

- **REST API Server**: FastAPI server với đầy đủ endpoints để truy vấn ứng viên
- **Streamlit Web UI**: Giao diện web tương tác để test và sử dụng API
- **Xử lý dữ liệu**: Tự động xử lý và format dữ liệu ứng viên từ Base.vn
- **API Documentation**: Tự động tạo Swagger/OpenAPI documentation
- **Validation**: Kiểm tra dữ liệu đầu vào với Pydantic
- **Error Handling**: Xử lý lỗi đầy đủ và trả về response rõ ràng

## Quickstart

```bash
# 1. Clone repository
git clone https://github.com/HoangThinh2024/WebAPI_App.git
cd WebAPI_App

# 2. Cài đặt dependencies
pip install -r requirements.txt

# 3. Tạo file .env từ template
cp .env.example .env
# Chỉnh sửa .env và thêm BASE_TOKEN của bạn

# 4. Chạy API server
python api_server.py

# Hoặc sử dụng make
make run-api
```

## Cài đặt

### Yêu cầu
- Python 3.8+
- pip
- (Optional) Docker & Docker Compose

### Cài đặt dependencies

```bash
pip install -r requirements.txt
```

hoặc sử dụng Makefile:

```bash
make install
```

## Cấu hình

Tạo file `.env` trong thư mục gốc với nội dung:

```env
BASE_TOKEN=your_base_vn_access_token_here
OPENING_ID=9346
STAGE_ID=75440
NUM_PER_PAGE=50
API_HOST=0.0.0.0
API_PORT=8000
```

## Sử dụng

### 1. Chạy REST API Server (FastAPI)

```bash
python api_server.py
```

hoặc với uvicorn:

```bash
uvicorn api_server:app --host 0.0.0.0 --port 8000 --reload
```

API server sẽ chạy tại: `http://localhost:8000`

**API Documentation:**
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### 2. Chạy Streamlit Web UI

```bash
streamlit run app.py
```

Web UI sẽ mở tại: `http://localhost:8501`

## API Endpoints

### 1. Root Endpoint
```
GET /
```
Trả về thông tin cơ bản về API.

**Response:**
```json
{
  "message": "Base.vn Candidate API Wrapper",
  "version": "1.0.0",
  "docs": "/docs",
  "health": "/health"
}
```

### 2. Health Check
```
GET /health
```
Kiểm tra trạng thái của API server.

**Response:**
```json
{
  "status": "healthy",
  "message": "API đang hoạt động bình thường"
}
```

### 3. Lấy danh sách ứng viên (POST)
```
POST /api/v1/candidates
Content-Type: application/json
```

**Request Body:**
```json
{
  "access_token": "your_access_token",
  "opening_id": "9346",
  "stage": "75440",
  "page": 1,
  "num_per_page": 50
}
```

**Response:**
```json
{
  "success": true,
  "message": "Lấy danh sách ứng viên thành công",
  "data": {
    "metrics": {
      "total": 100,
      "count": 50,
      "page": 1
    },
    "candidates": [
      {
        "ID": 12345,
        "Họ & Tên": "Nguyễn Văn A",
        "Email": "email@example.com",
        "SĐT": "0123456789",
        "Vị trí ứng tuyển": "Backend Developer",
        "Giai đoạn": "Interview",
        "Nguồn": "LinkedIn",
        "CV Link": "https://..."
      }
    ],
    "count": 50
  },
  "status_code": 200
}
```

### 4. Lấy danh sách ứng viên (GET)
```
GET /api/v1/candidates?access_token=xxx&opening_id=9346&stage=75440&page=1&num_per_page=50
```

**Query Parameters:**
- `access_token` (required): Token xác thực Base.vn API
- `opening_id` (required): ID của vị trí tuyển dụng
- `stage` (required): ID của giai đoạn tuyển dụng
- `page` (optional, default=1): Số trang
- `num_per_page` (optional, default=50): Số lượng kết quả mỗi trang (1-100)

**Response:** Giống như POST endpoint

## Ví dụ sử dụng

### Python với requests

```python
import requests

# POST request
url = "http://localhost:8000/api/v1/candidates"
data = {
    "access_token": "your_token",
    "opening_id": "9346",
    "stage": "75440",
    "page": 1,
    "num_per_page": 50
}

response = requests.post(url, json=data)
result = response.json()

if result["success"]:
    print(f"Tìm thấy {result['data']['count']} ứng viên")
    for candidate in result['data']['candidates']:
        print(f"- {candidate['Họ & Tên']}: {candidate['Email']}")
```

### cURL

```bash
# POST request
curl -X POST "http://localhost:8000/api/v1/candidates" \
  -H "Content-Type: application/json" \
  -d '{
    "access_token": "your_token",
    "opening_id": "9346",
    "stage": "75440",
    "page": 1,
    "num_per_page": 50
  }'

# GET request
curl "http://localhost:8000/api/v1/candidates?access_token=your_token&opening_id=9346&stage=75440&page=1&num_per_page=50"
```

### JavaScript/Node.js

```javascript
// POST request
const response = await fetch('http://localhost:8000/api/v1/candidates', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    access_token: 'your_token',
    opening_id: '9346',
    stage: '75440',
    page: 1,
    num_per_page: 50
  })
});

const result = await response.json();
console.log(result);
```

## Cấu trúc dự án

```
WebAPI_App/
├── api_server.py          # FastAPI REST API server
├── app.py                 # Streamlit web UI
├── api_client.py          # Client để gọi Base.vn API
├── data_processor.py      # Xử lý và format dữ liệu
├── requirements.txt       # Python dependencies
├── .env                   # Cấu hình (không commit)
├── .gitignore            # Git ignore rules
└── README.md             # Documentation
```

## Error Handling

API sẽ trả về các HTTP status codes phù hợp:

- `200`: Success
- `400`: Bad Request (tham số không hợp lệ)
- `500`: Internal Server Error
- `503`: Service Unavailable (không kết nối được Base.vn API)

**Error Response Format:**
```json
{
  "success": false,
  "message": "Mô tả lỗi",
  "status_code": 500
}
```

## Development

### Chạy với auto-reload

```bash
uvicorn api_server:app --reload --host 0.0.0.0 --port 8000
```

### Testing API

```bash
# Chạy test suite
make test
# hoặc
python test_api.py

# Chạy ví dụ sử dụng
make example
# hoặc
python example_usage.py
```

Sử dụng Swagger UI tại `http://localhost:8000/docs` để test các endpoints interactively.

## Docker Deployment

### Build và chạy với Docker

```bash
# Build image
docker build -t webapi-app .

# Chạy container
docker run -p 8000:8000 --env-file .env webapi-app
```

### Sử dụng Docker Compose

```bash
# Khởi động
docker-compose up -d

# Xem logs
docker-compose logs -f

# Dừng
docker-compose down
```

hoặc sử dụng Makefile:

```bash
make docker-build
make docker-run
make docker-stop
```

## Makefile Commands

```bash
make help          # Hiển thị tất cả commands
make install       # Cài đặt dependencies
make run-api       # Chạy API server
make run-ui        # Chạy Streamlit UI
make test          # Chạy tests
make example       # Chạy ví dụ
make docker-build  # Build Docker image
make docker-run    # Chạy với Docker Compose
make docker-stop   # Dừng containers
make clean         # Dọn dẹp cache files
```

## Troubleshooting

### API không kết nối được Base.vn
- Kiểm tra `BASE_TOKEN` trong file `.env` có đúng không
- Kiểm tra internet connection
- Kiểm tra Base.vn API có đang hoạt động không

### Port 8000 đã được sử dụng
```bash
# Thay đổi port trong .env
API_PORT=8080

# Hoặc khi chạy
API_PORT=8080 python api_server.py
```

### Import errors
```bash
# Đảm bảo tất cả dependencies đã được cài đặt
pip install -r requirements.txt
```

## License

MIT License - xem file LICENSE để biết thêm chi tiết.

