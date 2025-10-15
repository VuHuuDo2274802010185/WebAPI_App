# data_processor.py

import pandas as pd

def process_candidate_data(json_data):
    """
    Xử lý JSON phản hồi từ API Base.vn và trả về một Dict chứa
    DataFrame ứng viên và các chỉ số quan trọng.
    """
    
    candidates_list = json_data.get('candidates', [])
    
    # 1. Trích xuất chỉ số tổng quan
    metrics = {
        "total": json_data.get('total', 'N/A'),
        "count": json_data.get('count', 'N/A'),
        "page": json_data.get('page', 'N/A'),
    }

    if not candidates_list:
        return {"metrics": metrics, "dataframe": pd.DataFrame(), "count_candidates": 0}

    # 2. Chuẩn bị dữ liệu cho DataFrame
    display_data = []
    for c in candidates_list:
        # Xử lý CV link an toàn
        cvs = c.get('cvs', [])
        cv_link = cvs[0] if cvs and len(cvs) > 0 else 'Không có'
        
        display_data.append({
            "ID": c.get('id'),
            "Họ & Tên": c.get('name'),
            "Email": c.get('email'),
            "SĐT": c.get('phone'),
            "Vị trí ứng tuyển": c.get('opening_export', {}).get('name', 'N/A'),
            "Giai đoạn": c.get('stage_name', 'N/A'),
            "Nguồn": c.get('source', 'N/A'),
            "CV Link": cv_link
        })
        
    # 3. Tạo DataFrame
    df = pd.DataFrame(display_data)
    
    return {
        "metrics": metrics, 
        "dataframe": df, 
        "count_candidates": len(candidates_list)
    }