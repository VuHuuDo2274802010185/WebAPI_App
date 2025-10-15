# app.py

import os
import json
from datetime import datetime
from pathlib import Path

import requests
import streamlit as st
import streamlit.components.v1 as components
from dotenv import dotenv_values, load_dotenv, set_key

from api_client import (
    fetch_candidate_detail,
    fetch_candidate_messages,
    fetch_candidates,
    fetch_openings_list,
    fetch_opening,
)
from data_processor import process_candidate_data


ENV_PATH = Path(__file__).resolve().parent / ".env"

# Define SimpleResp at module level
class SimpleResp:
    def __init__(self, status_code, json_data, text):
        self.status_code = status_code
        self._json = json_data
        self.text = text
    
    def json(self):
        return self._json

def display_metrics(metrics):
    """Hiển thị các chỉ số tổng quan."""
    col_total, col_count, col_page = st.columns(3)
    col_total.metric("Tổng số ứng viên", metrics.get("total"))
    col_count.metric("Số lượng trên trang", metrics.get("count"))
    col_page.metric("Trang hiện tại", metrics.get("page"))


def load_env_file():
    """Đọc file .env nếu tồn tại và trả về dict giá trị."""
    if ENV_PATH.exists():
        load_dotenv(ENV_PATH, override=True)
        return dotenv_values(ENV_PATH)
    return {}


def _format_timestamp(value):
    """Chuyển timestamp dạng chuỗi/int thành định dạng ngày giờ dễ đọc."""
    if value in (None, "", 0, "0"):
        return "-"
    try:
        ts = int(value)
        if ts <= 0:
            return "-"
        return datetime.fromtimestamp(ts).strftime("%d/%m/%Y %H:%M")
    except (ValueError, TypeError):
        return "-"


def _format_text(value, default="-"):
    if value in (None, ""):
        return default
    return str(value)


def _render_badges(items):
    if not items:
        return "<span class='candidate-label muted'>Không có</span>"
    tags_html = "".join(
        f"<span class='candidate-badge'>{_format_text(tag.get('name') if isinstance(tag, dict) else tag)}</span>"
        for tag in items
    )
    return tags_html


def display_candidate_detail_view(json_data):
    """Render giao diện chi tiết ứng viên với bố cục thân thiện."""
    candidate = {}
    if isinstance(json_data, dict):
        candidate = json_data.get("candidate") or {}
        if not candidate and isinstance(json_data.get("data"), dict):
            candidate = json_data["data"].get("candidate") or json_data.get("data") or {}
    if not candidate or not isinstance(candidate, dict):
        st.info("Không tìm thấy dữ liệu ứng viên.")
        return

    opening_info = candidate.get("opening_export", {}) or {}
    stage_name = candidate.get("stage_name") or opening_info.get("stage_name")
    stage_name = stage_name or "Chưa xác định"
    time_apply = _format_timestamp(candidate.get("time_apply"))

    st.markdown(
        """
        <style>
        .candidate-card {background-color:#f8fafc; border:1px solid #e2e8f0; border-radius:16px; padding:1.5rem; margin-bottom:1rem;}
        .candidate-header {display:flex; flex-wrap:wrap; align-items:center; justify-content:space-between; gap:0.5rem;}
        .candidate-title {font-size:1.4rem; font-weight:600; color:#0f172a; margin:0;}
        .candidate-subtitle {font-size:0.95rem; color:#475569;}
        .candidate-badge {display:inline-block; padding:0.25rem 0.75rem; border-radius:999px; background:#e0f2fe; color:#0369a1; font-size:0.8rem; margin:0.15rem 0.4rem 0.15rem 0;}
        .candidate-label {font-weight:600; color:#0f172a;}
        .candidate-label.muted {color:#94a3b8; font-weight:500;}
        .candidate-section {margin-top:1.35rem;}
        .candidate-section h4 {margin-bottom:0.6rem; color:#1e293b;}
        .candidate-divider {margin:1.3rem 0; border-top:1px dashed #cbd5f5;}
        </style>
        """,
        unsafe_allow_html=True,
    )

    with st.container():
        st.markdown("<div class='candidate-card'>", unsafe_allow_html=True)
        header_cols = st.columns([3, 2])
        with header_cols[0]:
            st.markdown(
                f"<div class='candidate-header'>"
                f"<div><p class='candidate-title'>{_format_text(candidate.get('disp_name') or candidate.get('name'))}</p>"
                f"<p class='candidate-subtitle'>ID: {_format_text(candidate.get('id'))} · Stage: {stage_name}</p></div>"
                f"</div>",
                unsafe_allow_html=True,
            )
        with header_cols[1]:
            metric_cols = st.columns(2)
            metric_cols[0].metric("Đánh giá", _format_text(candidate.get("score", "0")))
            metric_cols[1].metric("Trạng thái", _format_text(candidate.get("status", "default")))

        st.markdown("<div class='candidate-divider'></div>", unsafe_allow_html=True)

        # Thông tin liên hệ
        st.markdown("<div class='candidate-section'><h4>Thông tin liên hệ</h4></div>", unsafe_allow_html=True)
        contact_cols = st.columns(3)
        contact_cols[0].markdown(f"**Email**\n\n{_format_text(candidate.get('email'))}")
        contact_cols[1].markdown(f"**Điện thoại**\n\n{_format_text(candidate.get('phone'))}")
        contact_cols[2].markdown(f"**Ngày sinh**\n\n{_format_text(candidate.get('dob'))}")

        st.markdown("<div class='candidate-divider'></div>", unsafe_allow_html=True)

        # Thông tin bổ sung
        st.markdown("<div class='candidate-section'><h4>Thông tin bổ sung</h4></div>", unsafe_allow_html=True)
        extra_cols = st.columns(3)
        gender_label = candidate.get("gender_text") or {
            "0": "Nữ",
            "1": "Nam",
            "2": "Khác",
            "-1": "Không xác định",
        }.get(str(candidate.get("gender")), "Không xác định")
        extra_cols[0].markdown(f"**Giới tính**\n\n{_format_text(gender_label)}")
        extra_cols[1].markdown(f"**Địa chỉ**\n\n{_format_text(candidate.get('address'))}")
        extra_cols[2].markdown(
            f"**Nguồn**\n\n{_format_text(candidate.get('source'))}"
        )

        st.markdown("<div class='candidate-divider'></div>", unsafe_allow_html=True)

        # Opening & trạng thái
        st.markdown("<div class='candidate-section'><h4>Thông tin tuyển dụng</h4></div>", unsafe_allow_html=True)
        opening_cols = st.columns(4)
        opening_cols[0].markdown(
            f"**Vị trí**\n\n{_format_text(opening_info.get('name'))}"
        )
        opening_cols[1].markdown(
            f"**Mã vị trí**\n\n{_format_text(opening_info.get('codename'))}"
        )
        opening_cols[2].markdown(
            f"**Stage ID**\n\n{_format_text(candidate.get('stage_id'))}"
        )
        opening_cols[3].markdown(
            f"**Thời gian nộp**\n\n{time_apply}"
        )

        st.markdown("<div class='candidate-divider'></div>", unsafe_allow_html=True)

        # CV và tags
        st.markdown("<div class='candidate-section'><h4>Hồ sơ & nhãn</h4></div>", unsafe_allow_html=True)
        cvs = candidate.get("cvs") or []
        if cvs:
            for idx, cv_url in enumerate(cvs, start=1):
                url = cv_url if isinstance(cv_url, str) else (
                    cv_url.get("url") if isinstance(cv_url, dict) else None
                )
                if url:
                    st.markdown(f"- [CV {idx}]({url})")
                else:
                    st.markdown(f"- CV {idx}: {_format_text(cv_url)}")
        else:
            st.markdown("<span class='candidate-label muted'>Chưa có CV đính kèm</span>", unsafe_allow_html=True)

        tags = candidate.get("tags") or []
        st.markdown("**Tags**")
        st.markdown(_render_badges(tags), unsafe_allow_html=True)

        # Timeline / Changelog
        timelines = candidate.get("timelines") or []
        changelogs = candidate.get("changelogs") or []
        if timelines or changelogs:
            st.markdown("<div class='candidate-divider'></div>", unsafe_allow_html=True)
            st.markdown("<div class='candidate-section'><h4>Lịch sử cập nhật</h4></div>", unsafe_allow_html=True)
            if changelogs:
                for log in changelogs:
                    log_time = _format_timestamp(log.get("since"))
                    st.markdown(
                        f"- **{_format_text(log.get('name'))}**\n\n"
                        f"  · Thời gian: {log_time}"
                    )
            if timelines:
                for timeline in timelines:
                    timeline_time = _format_timestamp(
                        timeline.get("created_at") or timeline.get("time")
                    )
                    title = timeline.get("title") or timeline.get("description")
                    st.markdown(
                        f"- {_format_text(title)} ({timeline_time})"
                    )

        st.markdown("</div>", unsafe_allow_html=True)


def display_candidate_messages_view(json_data):
    """Render giao diện danh sách tin nhắn ứng viên."""
    messages = []
    meta = {}
    if isinstance(json_data, dict):
        messages = json_data.get("messages") or []
        meta = {k: v for k, v in json_data.items() if k not in {"messages", "data"}}
        if not messages and isinstance(json_data.get("data"), dict):
            data_block = json_data["data"]
            messages = data_block.get("messages") or []
            if not meta:
                meta = {k: v for k, v in data_block.items() if k != "messages"}
    if not messages:
        st.info("Không có tin nhắn để hiển thị.")
        return

    st.markdown(
        """
        <style>
        .message-card {background:#ffffff; border:1px solid #e2e8f0; border-radius:14px; padding:1.2rem; margin-bottom:1rem; box-shadow:0 1px 2px rgba(15,23,42,0.05);}
        .message-title {font-size:1.05rem; font-weight:600; color:#0f172a; margin-bottom:0.35rem;}
        .message-meta {font-size:0.9rem; color:#475569; margin-bottom:0.2rem;}
        .message-meta.align-right {text-align:right;}
        .message-body {font-family:'Segoe UI',sans-serif; color:#0f172a; line-height:1.55;}
        .message-body img {max-width:100%; border-radius:10px; margin:0.3rem 0;}
        .message-body ul {padding-left:1.2rem;}
        .message-section-header {display:flex; align-items:center; justify-content:space-between; margin-bottom:0.5rem;}
        .badge-pill {display:inline-flex; align-items:center; padding:0.25rem 0.75rem; background:#e0f2fe; color:#0369a1; border-radius:999px; font-size:0.8rem; margin-left:0.4rem;}
        </style>
        """,
        unsafe_allow_html=True,
    )

    header_text = "Danh sách tin nhắn"
    count_badge = f"<span class='badge-pill'>Tổng {len(messages)}</span>"
    st.markdown(
        f"<div class='message-section-header'><h4>{header_text}</h4>{count_badge}</div>",
        unsafe_allow_html=True,
    )

    if meta:
        meta_cols = st.columns(3)
        meta_cols[0].markdown(
            f"**Candidate ID**\n\n{_format_text(meta.get('candidate_id'))}"
        )
        meta_cols[1].markdown(
            f"**Opening ID**\n\n{_format_text(meta.get('opening_id'))}"
        )
        meta_cols[2].markdown(
            f"**Thời gian cập nhật**\n\n{_format_timestamp(meta.get('since'))}"
        )

    for idx, message in enumerate(messages, start=1):
        user = message.get("user") or {}
        author_name = user.get("name") or user.get("username") or user.get("email") or "Không rõ"
        author_type = user.get("type") or ""
        subject = message.get("subject") or "Không có tiêu đề"
        time_sent = _format_timestamp(message.get("since"))
        thread_id = message.get("thread_id") or "-"
        message_id = message.get("id") or "-"

        st.markdown("<div class='message-card'>", unsafe_allow_html=True)
        header_cols = st.columns([3, 1])
        with header_cols[0]:
            st.markdown(
                f"<div class='message-title'>{idx}. {_format_text(subject)}</div>",
                unsafe_allow_html=True,
            )
            st.markdown(
                f"<div class='message-meta'>Từ: {_format_text(author_name)}"
                f" · Loại: {_format_text(author_type)}</div>",
                unsafe_allow_html=True,
            )
            st.markdown(
                f"<div class='message-meta'>Message ID: {_format_text(message_id)} · Thread: {_format_text(thread_id)}</div>",
                unsafe_allow_html=True,
            )
        with header_cols[1]:
            st.markdown(
                f"<div class='message-meta align-right'>Thời gian: {time_sent}</div>",
                unsafe_allow_html=True,
            )

        content_html = message.get("content") or message.get("body") or ""
        if isinstance(content_html, str):
            content_html = content_html.replace("\\r\\n", "\n")
        content_html = content_html or "<p>Không có nội dung.</p>"

        components.html(
            f"""
            <div class='message-body'>
                {content_html}
            </div>
            """,
            height=420,
            scrolling=True,
        )

        attachments = message.get("attachments") or []
        if attachments:
            st.markdown("**Tệp đính kèm**")
            for attachment in attachments:
                name = attachment.get("name") or attachment.get("filename") or "Tệp"
                url = attachment.get("url") or attachment.get("download_url")
                if url:
                    st.markdown(f"- [{_format_text(name)}]({url})")
                else:
                    st.markdown(f"- {_format_text(name)}")

        tracking_events = message.get("tracking_events") or []
        if tracking_events:
            with st.expander("Lịch sử gửi/đọc"):
                for event in tracking_events:
                    event_name = event.get("event") or "unknown"
                    event_time = _format_timestamp(event.get("since"))
                    st.markdown(
                        f"- **{_format_text(event_name)}** · {event_time}"
                    )

        st.markdown("</div>", unsafe_allow_html=True)
def main():
    env_values = load_env_file()
    env_num_per_page = env_values.get("NUM_PER_PAGE") or os.getenv("NUM_PER_PAGE")
    try:
        default_num_per_page = int(env_num_per_page) if env_num_per_page else 50
    except ValueError:
        default_num_per_page = 50

    st.title("Ứng dụng Truy vấn Base.vn Candidate List API")
    st.markdown("---")

    env_status = st.empty()
    if ENV_PATH.exists():
        env_status.success(
            f"Đã nạp {len(env_values)} biến cấu hình từ `{ENV_PATH.name}`"
        )
    else:
        env_status.warning(
            "Không tìm thấy file `.env`. Vui lòng cấu hình để tạo mới hoặc kiểm tra đường dẫn."
        )

    # --- Cấu hình lưu vào .env (không commit) ---
    with st.expander("Cấu hình (lưu vào .env, không commit)"):
        with st.form("config_form"):
            st.write("Nhập token và các cấu hình mặc định. Các giá trị này sẽ được lưu vào `.env`.")
            token_input = st.text_input(
                "BASE_TOKEN",
                value=env_values.get("BASE_TOKEN") or os.getenv("BASE_TOKEN", ""),
            )
            opening_input = st.text_input(
                "OPENING_ID",
                value=env_values.get("OPENING_ID") or os.getenv("OPENING_ID", "9346"),
            )
            stage_input = st.text_input(
                "STAGE_ID",
                value=env_values.get("STAGE_ID") or os.getenv("STAGE_ID", "75440"),
            )
            num_per_page_input = st.number_input(
                "NUM_PER_PAGE",
                min_value=1,
                max_value=100,
                value=default_num_per_page,
            )
            save_cfg = st.form_submit_button("Lưu cấu hình vào .env")

        if save_cfg:
            # tạo/ghi .env bằng python-dotenv
            try:
                set_key(str(ENV_PATH), "BASE_TOKEN", token_input)
                set_key(str(ENV_PATH), "OPENING_ID", opening_input)
                set_key(str(ENV_PATH), "STAGE_ID", stage_input)
                set_key(str(ENV_PATH), "NUM_PER_PAGE", str(num_per_page_input))
                env_values = load_env_file()
                env_num_per_page = env_values.get("NUM_PER_PAGE") or os.getenv("NUM_PER_PAGE")
                try:
                    default_num_per_page = int(env_num_per_page) if env_num_per_page else 50
                except ValueError:
                    default_num_per_page = 50
                env_status.success(
                    f"Đã cập nhật {len(env_values)} biến cấu hình trong `{ENV_PATH.name}`"
                )
                st.success("Đã lưu vào .env. Đảm bảo không commit file .env lên git.")
            except Exception as e:
                st.error(f"Không thể lưu .env: {e}")

    # --- 1. Form Nhập Tham số Tương tác ---
    with st.form("api_query_form"):
        st.subheader("Tham số API")

        # Access Token lấy từ .env nếu có
        access_token = st.text_input(
            "Access Token:", 
            help="Nhập access_token được cấp từ Base.vn", 
            value=env_values.get("BASE_TOKEN") or os.getenv("BASE_TOKEN", "")
        )

        # Nút để load danh sách openings
        load_openings = st.form_submit_button("🔄 Tải danh sách Opening & Stage")

    # Xử lý load openings ngoài form
    openings_data = []
    opening_options = {}
    
    if load_openings and access_token:
        with st.spinner("Đang tải danh sách openings..."):
            try:
                resp = fetch_openings_list(access_token, page=1, num_per_page=100)
                if resp.status_code == 200:
                    data = resp.json()
                    openings_data = data.get("openings", [])
                    
                    if openings_data:
                        # Tạo dict: "ID - Tên" -> opening object
                        for opening in openings_data:
                            key = f"{opening.get('id')} - {opening.get('name', 'N/A')}"
                            opening_options[key] = opening
                        st.success(f"✅ Đã tải {len(openings_data)} openings")
                        # Lưu vào session state
                        st.session_state['openings'] = opening_options
                    else:
                        st.warning("Không tìm thấy opening nào")
                else:
                    st.error(f"Lỗi API: {resp.status_code} - {resp.text}")
            except Exception as e:
                st.error(f"Lỗi: {e}")
    
    # Load từ session state nếu đã có
    if 'openings' in st.session_state:
        opening_options = st.session_state['openings']

    # Form chính để query candidates
    with st.form("candidate_query_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            if opening_options:
                # Dropdown để chọn opening
                selected_opening_key = st.selectbox(
                    "🎯 Chọn Opening:",
                    options=list(opening_options.keys()),
                    help="Chọn vị trí tuyển dụng từ danh sách"
                )
                
                # Lấy opening_id từ key đã chọn
                selected_opening = opening_options[selected_opening_key]
                opening_id = str(selected_opening.get('id'))
                
                # Hiển thị stages nếu có
                stages = selected_opening.get('stages', [])
                if stages:
                    stage_options = {f"{s.get('id')} - {s.get('name', 'N/A')}": s.get('id') for s in stages}
                    selected_stage_key = st.selectbox(
                        "📊 Chọn Stage:",
                        options=list(stage_options.keys()),
                        help="Chọn giai đoạn tuyển dụng"
                    )
                    stage = str(stage_options[selected_stage_key])
                else:
                    stage = st.text_input(
                        "Stage ID:",
                        value=env_values.get("STAGE_ID") or os.getenv("STAGE_ID", "75440"),
                    )
                    st.info("ℹ️ Opening này chưa có stages, vui lòng nhập thủ công")
            else:
                st.info("👆 Nhấn 'Tải danh sách Opening & Stage' ở trên để load dropdown")
                opening_id = st.text_input(
                    "Opening ID:",
                    value=env_values.get("OPENING_ID") or os.getenv("OPENING_ID", "9346"),
                )
                stage = st.text_input(
                    "Stage ID:",
                    value=env_values.get("STAGE_ID") or os.getenv("STAGE_ID", "75440"),
                )
            
            page = st.number_input("Trang (page):", min_value=1, value=1)
            
        with col2:
            num_per_page = st.number_input(
                "Số lượng/trang:", 
                min_value=1, 
                max_value=100, 
                value=default_num_per_page
            )

        submitted = st.form_submit_button("🚀 Gửi Yêu cầu API")
    
    use_local_proxy = st.checkbox(
        "🔄 Sử dụng Proxy Server Local",
        value=False,
        help="""
        Khi bật: Gửi request qua FastAPI proxy server local (http://127.0.0.1:8000/candidates)
        - Proxy sẽ xử lý và forward request đến Base.vn API
        - Có thể thêm logging, caching, hoặc transform data trước khi trả về
        - Hữu ích cho development và debugging
        
        Khi tắt: Gửi request trực tiếp đến Base.vn API (https://hiring.base.vn/publicapi/v2/candidate/list)
        - Kết nối trực tiếp, không qua trung gian
        - Thích hợp cho production hoặc khi không cần proxy
        """
    )

    # --- 2. Logic Gọi API và Xử lý ---
    if submitted:
        st.info("Đang gửi yêu cầu và xử lý dữ liệu...")
        
        try:
            # Nếu chọn dùng proxy local, gọi endpoint /candidates trên FastAPI server
            if use_local_proxy:
                proxy_url = os.getenv("LOCAL_PROXY_URL", "http://127.0.0.1:8000/candidates")
                proxy_payload = {
                    "access_token": access_token,
                    "opening_id": opening_id,
                    "page": page,
                    "num_per_page": num_per_page,
                    "stage": stage
                }
                proxy_resp = requests.post(proxy_url, data=proxy_payload)
                # proxy returns JSON with processed data and raw
                if proxy_resp.status_code == 200:
                    proxy_json = proxy_resp.json()
                    # adapt shape used later: set response-like object
                    response = SimpleResp(200, proxy_json.get("raw", {}), json.dumps(proxy_json))
                else:
                    response = SimpleResp(proxy_resp.status_code, {}, proxy_resp.text)
            else:
                # Gọi hàm API từ module api_client.py trực tiếp
                response = fetch_candidates(access_token, opening_id, page, num_per_page, stage)
            
            st.subheader("Kết quả Phản hồi")
            st.write(f"**Mã Trạng thái (Status Code):** `{response.status_code}`")

            if response.status_code == 200:
                json_data = response.json()

                # Xử lý và trích xuất dữ liệu từ module data_processor.py
                processed_data = process_candidate_data(json_data)
                
                # Hiển thị kết quả
                display_metrics(processed_data["metrics"])
                
                st.subheader(f"Danh sách Ứng viên (Tìm thấy: {processed_data['count_candidates']})")
                
                if not processed_data["dataframe"].empty:
                    st.dataframe(processed_data["dataframe"], width="stretch")
                else:
                    st.warning("Không tìm thấy ứng viên nào.")
                    
                if st.checkbox("Xem toàn bộ JSON phản hồi thô"):
                    st.json(json_data)
                    
            else:
                st.error(f"Lỗi: API trả về mã trạng thái {response.status_code}.")
                st.code(response.text, language="text")

        except ConnectionError as e:
            st.error(str(e))
        except json.JSONDecodeError:
            st.error("Lỗi giải mã JSON. API có thể đã trả về dữ liệu không hợp lệ.")

    # --- 3. Get Candidate Details ---
    st.markdown("---")
    st.subheader("🔍 Lấy Chi tiết Ứng viên")
    
    with st.form("candidate_detail_form"):
        candidate_id_detail = st.text_input(
            "Candidate ID:",
            help="Nhập ID của ứng viên cần xem chi tiết",
            value=""
        )
        access_token_detail = st.text_input(
            "Access Token:",
            help="Nhập access_token được cấp từ Base.vn",
            value=env_values.get("BASE_TOKEN") or os.getenv("BASE_TOKEN", "")
        )
        use_proxy_detail = st.checkbox("🔄 Sử dụng Proxy Server Local", value=False)
        submitted_detail = st.form_submit_button("🔍 Lấy Chi tiết Ứng viên")
    
    if submitted_detail and candidate_id_detail:
        st.info("Đang lấy chi tiết ứng viên...")
        
        try:
            if use_proxy_detail:
                proxy_url = os.getenv("LOCAL_PROXY_URL", f"http://127.0.0.1:8000/candidate/{candidate_id_detail}")
                if not proxy_url.startswith("http://127.0.0.1:8000/candidate/"):
                    proxy_url = f"http://127.0.0.1:8000/candidate/{candidate_id_detail}"
                params = {"access_token": access_token_detail}
                response = requests.post(proxy_url, params=params)
            else:
                response = fetch_candidate_detail(access_token_detail, candidate_id_detail)
            
            st.subheader("Kết quả Phản hồi")
            st.write(f"**Mã Trạng thái (Status Code):** `{response.status_code}`")
            
            if response.status_code == 200:
                json_data = response.json()
                st.success("✅ Lấy chi tiết ứng viên thành công!")
                display_candidate_detail_view(json_data)
                with st.expander("Xem JSON gốc"):
                    st.json(json_data)
            else:
                st.error(f"Lỗi: API trả về mã trạng thái {response.status_code}.")
                st.code(response.text, language="text")
        
        except ConnectionError as e:
            st.error(str(e))
        except json.JSONDecodeError:
            st.error("Lỗi giải mã JSON. API có thể đã trả về dữ liệu không hợp lệ.")
        except Exception as e:
            st.error(f"Lỗi: {e}")
    elif submitted_detail and not candidate_id_detail:
        st.warning("⚠️ Vui lòng nhập Candidate ID")

    # --- 4. Get Candidate Messages ---
    st.markdown("---")
    st.subheader("💬 Lấy Tin nhắn Ứng viên")
    
    with st.form("candidate_messages_form"):
        candidate_id_messages = st.text_input(
            "Candidate ID:",
            help="Nhập ID của ứng viên cần xem tin nhắn",
            value=""
        )
        access_token_messages = st.text_input(
            "Access Token:",
            help="Nhập access_token được cấp từ Base.vn",
            value=env_values.get("BASE_TOKEN") or os.getenv("BASE_TOKEN", "")
        )
        use_proxy_messages = st.checkbox("🔄 Sử dụng Proxy Server Local", value=False)
        submitted_messages = st.form_submit_button("💬 Lấy Tin nhắn")
    
    if submitted_messages and candidate_id_messages:
        st.info("Đang lấy tin nhắn ứng viên...")
        
        try:
            if use_proxy_messages:
                proxy_url = os.getenv("LOCAL_PROXY_URL", f"http://127.0.0.1:8000/candidate/{candidate_id_messages}/messages")
                if not proxy_url.startswith("http://127.0.0.1:8000/candidate/"):
                    proxy_url = f"http://127.0.0.1:8000/candidate/{candidate_id_messages}/messages"
                params = {"access_token": access_token_messages}
                response = requests.post(proxy_url, params=params)
            else:
                response = fetch_candidate_messages(access_token_messages, candidate_id_messages)
            
            st.subheader("Kết quả Phản hồi")
            st.write(f"**Mã Trạng thái (Status Code):** `{response.status_code}`")
            
            if response.status_code == 200:
                json_data = response.json()
                st.success("✅ Lấy tin nhắn ứng viên thành công!")
                display_candidate_messages_view(json_data)
                with st.expander("Xem JSON gốc"):
                    st.json(json_data)
            else:
                st.error(f"Lỗi: API trả về mã trạng thái {response.status_code}.")
                st.code(response.text, language="text")
        
        except ConnectionError as e:
            st.error(str(e))
        except json.JSONDecodeError:
            st.error("Lỗi giải mã JSON. API có thể đã trả về dữ liệu không hợp lệ.")
        except Exception as e:
            st.error(f"Lỗi: {e}")
    elif submitted_messages and not candidate_id_messages:
        st.warning("⚠️ Vui lòng nhập Candidate ID")


if __name__ == "__main__":
    main()