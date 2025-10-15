# app.py

import os
import streamlit as st
import json
import requests
from dotenv import load_dotenv, set_key
from api_client import fetch_candidates, fetch_openings_list, fetch_opening, fetch_candidate_detail, fetch_candidate_messages
from data_processor import process_candidate_data

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

def main():
    # load .env if exists
    ENV_PATH = os.path.join(os.getcwd(), ".env")
    load_dotenv(ENV_PATH)

    st.title("Ứng dụng Truy vấn Base.vn Candidate List API")
    st.markdown("---")

    # --- Cấu hình lưu vào .env (không commit) ---
    with st.expander("Cấu hình (lưu vào .env, không commit)"):
        with st.form("config_form"):
            st.write("Nhập token và các cấu hình mặc định. Các giá trị này sẽ được lưu vào `.env`.")
            token_input = st.text_input("BASE_TOKEN", value=os.getenv("BASE_TOKEN", ""))
            opening_input = st.text_input("OPENING_ID", value=os.getenv("OPENING_ID", "9346"))
            stage_input = st.text_input("STAGE_ID", value=os.getenv("STAGE_ID", "75440"))
            num_per_page_default = int(os.getenv("NUM_PER_PAGE", "50") if os.getenv("NUM_PER_PAGE") else 50)
            num_per_page_input = st.number_input("NUM_PER_PAGE", min_value=1, max_value=100, value=num_per_page_default)
            save_cfg = st.form_submit_button("Lưu cấu hình vào .env")

        if save_cfg:
            # tạo/ghi .env bằng python-dotenv
            try:
                set_key(ENV_PATH, "BASE_TOKEN", token_input)
                set_key(ENV_PATH, "OPENING_ID", opening_input)
                set_key(ENV_PATH, "STAGE_ID", stage_input)
                set_key(ENV_PATH, "NUM_PER_PAGE", str(num_per_page_input))
                load_dotenv(ENV_PATH, override=True)
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
            value=os.getenv("BASE_TOKEN", "")
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
                    stage = st.text_input("Stage ID:", value=os.getenv("STAGE_ID", "75440"))
                    st.info("ℹ️ Opening này chưa có stages, vui lòng nhập thủ công")
            else:
                st.info("👆 Nhấn 'Tải danh sách Opening & Stage' ở trên để load dropdown")
                opening_id = st.text_input("Opening ID:", value=os.getenv("OPENING_ID", "9346"))
                stage = st.text_input("Stage ID:", value=os.getenv("STAGE_ID", "75440"))
            
            page = st.number_input("Trang (page):", min_value=1, value=1)
            
        with col2:
            num_per_page = st.number_input(
                "Số lượng/trang:", 
                min_value=1, 
                max_value=100, 
                value=int(os.getenv("NUM_PER_PAGE", "50") if os.getenv("NUM_PER_PAGE") else 50)
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
            value=os.getenv("BASE_TOKEN", "")
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
            value=os.getenv("BASE_TOKEN", "")
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