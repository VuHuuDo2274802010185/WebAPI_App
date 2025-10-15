# api_client.py

import requests
from urllib.parse import urlencode

API_URL = "https://hiring.base.vn/publicapi/v2/candidate/list"
OPENING_LIST_URL = "https://hiring.base.vn/publicapi/v2/opening/list"
OPENING_GET_URL = "https://hiring.base.vn/publicapi/v2/opening/get"
CANDIDATE_LIST_URL = "https://hiring.base.vn/publicapi/v2/candidate/list"
CANDIDATE_GET_URL = "https://hiring.base.vn/publicapi/v2/candidate/get"
CANDIDATE_MESSAGES_URL = "https://hiring.base.vn/publicapi/v2/candidate/messages"

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


def fetch_openings_list(access_token, page=1, num_per_page=50, order_by="starred"):
    """
    Gọi endpoint /opening/list của Base.vn (dùng POST form-encoded)
    Trả về đối tượng Response của requests.
    """
    payload_params = {
        "access_token": access_token,
        "page": page,
        "num_per_page": num_per_page,
        "order_by": order_by
    }

    payload = urlencode(payload_params)

    try:
        response = requests.request(
            "POST",
            OPENING_LIST_URL,
            data=payload,
            headers=FIXED_HEADERS
        )
        return response
    except requests.exceptions.RequestException as e:
        raise ConnectionError(f"Lỗi kết nối API (opening/list): {e}")


def fetch_opening(access_token, opening_id):
    """
    Gọi endpoint /opening/get để lấy chi tiết opening theo id.
    """
    payload_params = {
        "access_token": access_token,
        "id": opening_id
    }
    payload = urlencode(payload_params)

    try:
        response = requests.request(
            "POST",
            OPENING_GET_URL,
            data=payload,
            headers=FIXED_HEADERS
        )
        return response
    except requests.exceptions.RequestException as e:
        raise ConnectionError(f"Lỗi kết nối API (opening/get): {e}")


def fetch_candidate_detail(access_token, candidate_id):
    """Gọi endpoint /candidate/get để lấy chi tiết ứng viên."""
    payload_params = {
        "access_token": access_token,
        "id": candidate_id
    }
    payload = urlencode(payload_params)

    try:
        response = requests.request(
            "POST",
            CANDIDATE_GET_URL,
            data=payload,
            headers=FIXED_HEADERS
        )
        return response
    except requests.exceptions.RequestException as e:
        raise ConnectionError(f"Lỗi kết nối API (candidate/get): {e}")


def fetch_candidate_messages(access_token, candidate_id):
    """Gọi endpoint /candidate/messages để lấy lịch sử tin nhắn/notes của ứng viên."""
    payload_params = {
        "access_token": access_token,
        "id": candidate_id
    }
    payload = urlencode(payload_params)

    try:
        response = requests.request(
            "POST",
            CANDIDATE_MESSAGES_URL,
            data=payload,
            headers=FIXED_HEADERS
        )
        return response
    except requests.exceptions.RequestException as e:
        raise ConnectionError(f"Lỗi kết nối API (candidate/messages): {e}")