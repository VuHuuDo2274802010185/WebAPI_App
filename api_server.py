# api_server.py
"""
FastAPI Server - Web API hoàn chỉnh cho việc truy vấn Base.vn Candidate API
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
import os
from dotenv import load_dotenv
from api_client import fetch_candidates
from data_processor import process_candidate_data
import json

# Load environment variables
load_dotenv()

# Khởi tạo FastAPI app
app = FastAPI(
    title="Base.vn Candidate API Wrapper",
    description="API hoàn chỉnh để truy vấn danh sách ứng viên từ Base.vn",
    version="1.0.0"
)


# Pydantic Models cho request/response validation
class CandidateQueryRequest(BaseModel):
    """Model cho request query ứng viên"""
    access_token: str = Field(..., description="Token xác thực Base.vn API")
    opening_id: str = Field(..., description="ID của vị trí tuyển dụng")
    stage: str = Field(..., description="ID của giai đoạn tuyển dụng")
    page: int = Field(default=1, ge=1, description="Số trang (bắt đầu từ 1)")
    num_per_page: int = Field(default=50, ge=1, le=100, description="Số lượng kết quả mỗi trang (1-100)")


class CandidateResponse(BaseModel):
    """Model cho response chứa thông tin ứng viên"""
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None
    status_code: int


class HealthResponse(BaseModel):
    """Model cho health check response"""
    status: str
    message: str


# API Endpoints

@app.get("/", response_model=Dict[str, str])
async def root():
    """
    Root endpoint - Thông tin về API
    """
    return {
        "message": "Base.vn Candidate API Wrapper",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint - Kiểm tra trạng thái của API
    """
    return HealthResponse(
        status="healthy",
        message="API đang hoạt động bình thường"
    )


@app.post("/api/v1/candidates", response_model=CandidateResponse)
async def get_candidates(request: CandidateQueryRequest):
    """
    Lấy danh sách ứng viên từ Base.vn API
    
    Args:
        request: CandidateQueryRequest chứa các tham số truy vấn
        
    Returns:
        CandidateResponse chứa danh sách ứng viên đã được xử lý
    """
    try:
        # Gọi API Base.vn
        response = fetch_candidates(
            access_token=request.access_token,
            opening_id=request.opening_id,
            page=request.page,
            num_per_page=request.num_per_page,
            stage=request.stage
        )
        
        # Kiểm tra status code
        if response.status_code != 200:
            return CandidateResponse(
                success=False,
                message=f"Lỗi từ Base.vn API: {response.status_code}",
                data={"error": response.text},
                status_code=response.status_code
            )
        
        # Parse JSON response
        json_data = response.json()
        
        # Xử lý dữ liệu
        processed_data = process_candidate_data(json_data)
        
        # Chuyển DataFrame thành dict để trả về JSON
        candidates_list = processed_data["dataframe"].to_dict('records') if not processed_data["dataframe"].empty else []
        
        return CandidateResponse(
            success=True,
            message="Lấy danh sách ứng viên thành công",
            data={
                "metrics": processed_data["metrics"],
                "candidates": candidates_list,
                "count": processed_data["count_candidates"]
            },
            status_code=200
        )
        
    except ConnectionError as e:
        raise HTTPException(
            status_code=503,
            detail=f"Không thể kết nối đến Base.vn API: {str(e)}"
        )
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=500,
            detail="Lỗi giải mã JSON từ Base.vn API"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Lỗi server: {str(e)}"
        )


@app.get("/api/v1/candidates", response_model=CandidateResponse)
async def get_candidates_query(
    access_token: str = Query(..., description="Token xác thực Base.vn API"),
    opening_id: str = Query(..., description="ID của vị trí tuyển dụng"),
    stage: str = Query(..., description="ID của giai đoạn tuyển dụng"),
    page: int = Query(default=1, ge=1, description="Số trang (bắt đầu từ 1)"),
    num_per_page: int = Query(default=50, ge=1, le=100, description="Số lượng kết quả mỗi trang (1-100)")
):
    """
    Lấy danh sách ứng viên từ Base.vn API (GET method với query parameters)
    
    Args:
        access_token: Token xác thực
        opening_id: ID vị trí tuyển dụng
        stage: ID giai đoạn tuyển dụng
        page: Số trang
        num_per_page: Số lượng mỗi trang
        
    Returns:
        CandidateResponse chứa danh sách ứng viên đã được xử lý
    """
    # Tạo request object và sử dụng lại logic từ POST endpoint
    request = CandidateQueryRequest(
        access_token=access_token,
        opening_id=opening_id,
        stage=stage,
        page=page,
        num_per_page=num_per_page
    )
    return await get_candidates(request)


# Exception handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Custom handler cho HTTP exceptions"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": exc.detail,
            "status_code": exc.status_code
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Custom handler cho các exceptions khác"""
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": f"Lỗi server không mong đợi: {str(exc)}",
            "status_code": 500
        }
    )


if __name__ == "__main__":
    import uvicorn
    
    # Lấy cấu hình từ environment variables
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", "8000"))
    
    print(f"🚀 Starting API Server on {host}:{port}")
    print(f"📚 API Documentation: http://{host}:{port}/docs")
    print(f"🔍 Alternative Docs: http://{host}:{port}/redoc")
    
    uvicorn.run(app, host=host, port=port)
