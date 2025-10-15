# api_client.py

import requests
from urllib.parse import urlencode

API_URL = "https://hiring.base.vn/publicapi/v2/candidate/list"

# Headers cố định cho yêu cầu POST
FIXED_HEADERS = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "User-Agent": "EchoapiRuntime/1.1.0",
    "Connection": "keep-alive"
}

def fetch_candidates(access_token, opening_id, page, num_per_page, stage):
    """
    Thực hiện cuộc gọi API POST đến Base.vn để lấy danh sách ứng viên.
    Trả về đối tượng Response của requests.
    """
    # Chuẩn bị tham số payload
    payload_params = {
        "access_token": access_token,
        "opening_id": opening_id,
        "page": page,
        "num_per_page": num_per_page,
        "stage": stage
    }
    
    # Mã hóa payload
    payload = urlencode(payload_params)

    try:
        response = requests.request(
            "POST", 
            API_URL, 
            data=payload, 
            headers=FIXED_HEADERS
        )
        return response
    except requests.exceptions.RequestException as e:
        # Xử lý các lỗi kết nối/yêu cầu cơ bản
        raise ConnectionError(f"Lỗi kết nối API: {e}")