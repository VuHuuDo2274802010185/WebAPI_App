# 🎯 Hướng dẫn Sử dụng Tính năng Dropdown Opening & Stage

## ✨ Tính năng mới

Thay vì phải nhập thủ công Opening ID và Stage ID, bạn có thể chọn từ dropdown được load tự động từ API Base.vn.

## 📋 Cách sử dụng

### Bước 1: Nhập Access Token
- Mở ứng dụng Streamlit
- Nhập `Access Token` của bạn vào ô đầu tiên
- (Hoặc đã cấu hình sẵn trong `.env`)

### Bước 2: Tải danh sách Opening & Stage
- Nhấn nút **"🔄 Tải danh sách Opening & Stage"**
- Hệ thống sẽ gọi API để lấy tất cả openings (tối đa 100)
- Danh sách sẽ được lưu vào session state

### Bước 3: Chọn Opening từ Dropdown
- Sau khi load thành công, dropdown **"🎯 Chọn Opening"** sẽ hiển thị
- Chọn opening theo format: `ID - Tên vị trí`
- Ví dụ: `9346 - Backend Developer`

### Bước 4: Chọn Stage
- Nếu opening có stages, dropdown **"📊 Chọn Stage"** sẽ tự động hiển thị
- Chọn stage theo format: `ID - Tên giai đoạn`
- Ví dụ: `75440 - Phỏng vấn vòng 1`
- Nếu không có stages, bạn có thể nhập thủ công

### Bước 5: Gửi request
- Điền thêm thông tin: `Trang`, `Số lượng/trang`
- Nhấn **"🚀 Gửi Yêu cầu API"**

## 🔄 Fallback Mode

Nếu không muốn dùng dropdown, bạn vẫn có thể:
1. Không nhấn nút "Tải danh sách Opening & Stage"
2. Nhập thủ công vào ô text input như trước

## 💡 Lợi ích

✅ **Không cần nhớ ID**: Chọn từ danh sách thay vì phải nhớ/tìm ID
✅ **Giảm lỗi**: Chọn từ dropdown đảm bảo ID hợp lệ
✅ **Hiển thị tên**: Thấy rõ tên opening/stage thay vì chỉ có số
✅ **Stages tự động**: Stages được load tự động theo opening đã chọn
✅ **Session State**: Chỉ cần load 1 lần, dùng cho nhiều query

## ⚙️ Technical Details

### API Endpoints được sử dụng:
- `POST /publicapi/v2/opening/list` - Lấy danh sách openings
- Mỗi opening object chứa:
  - `id`: Opening ID
  - `name`: Tên vị trí
  - `stages`: Array các stages của opening đó

### Session State:
- Danh sách openings được lưu trong `st.session_state['openings']`
- Không cần load lại khi switch giữa các query
- Chỉ reset khi refresh page hoặc nhấn lại nút "Tải danh sách"

## 🐛 Troubleshooting

### Dropdown không hiển thị
- ✅ Đảm bảo đã nhập Access Token hợp lệ
- ✅ Nhấn nút "Tải danh sách Opening & Stage"
- ✅ Kiểm tra thông báo lỗi (nếu có)

### Không có stages
- Một số openings có thể chưa có stages được config
- Ứng dụng sẽ tự động fallback sang text input

### API lỗi 401/403
- Token không hợp lệ hoặc đã hết hạn
- Kiểm tra lại token trong `.env` hoặc nhập lại

## 📸 Screenshots

```
┌─────────────────────────────────────────┐
│ Access Token: [*********************]   │
│ [🔄 Tải danh sách Opening & Stage]     │
└─────────────────────────────────────────┘
         ↓ (Nhấn nút)
┌─────────────────────────────────────────┐
│ ✅ Đã tải 25 openings                   │
│                                         │
│ 🎯 Chọn Opening:                        │
│ [9346 - Backend Developer        ▼]    │
│                                         │
│ 📊 Chọn Stage:                          │
│ [75440 - Phỏng vấn vòng 1       ▼]    │
│                                         │
│ Trang: [1]  Số lượng/trang: [50]      │
│ [🚀 Gửi Yêu cầu API]                   │
└─────────────────────────────────────────┘
```
