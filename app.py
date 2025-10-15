# app.py

import os
import streamlit as st
import json
from dotenv import load_dotenv, set_key
from api_client import fetch_candidates
from data_processor import process_candidate_data

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
            help="Nhập access_token được cấp", 
            value=os.getenv("BASE_TOKEN", "")
        )

        col1, col2 = st.columns(2)
        with col1:
            opening_id = st.text_input("Opening ID:", value=os.getenv("OPENING_ID", "9346"))
            page = st.number_input("Trang (page):", min_value=1, value=1)
            
        with col2:
            stage = st.text_input("Stage ID:", value=os.getenv("STAGE_ID", "75440"))
            num_per_page = st.number_input("Số lượng/trang (num_per_page):", min_value=1, max_value=100, value=int(os.getenv("NUM_PER_PAGE", "50") if os.getenv("NUM_PER_PAGE") else 50))

        submitted = st.form_submit_button("Gửi Yêu cầu API (POST)")

    # --- 2. Logic Gọi API và Xử lý ---
    if submitted:
        st.info("Đang gửi yêu cầu và xử lý dữ liệu...")
        
        try:
            # Gọi hàm API từ module api_client.py
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
                    st.dataframe(processed_data["dataframe"], use_container_width=True)
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


if __name__ == "__main__":
    main()