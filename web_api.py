from typing import Optional
import os
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from api_client import fetch_openings_list, fetch_opening, fetch_candidates
from data_processor import process_candidate_data
from api_client import fetch_candidate_detail, fetch_candidate_messages

app = FastAPI(title="Base.vn Proxy API", version="0.1.0")


@app.get("/html", response_class=HTMLResponse)
def read_root_html():
    """HTML landing page with complete API documentation."""
    html_content = """
    <!DOCTYPE html>
    <html lang="vi">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Base.vn Proxy API - Complete API Documentation</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
            }
            .container {
                max-width: 1200px;
                margin: 0 auto;
            }
            .header {
                background: white;
                padding: 40px;
                border-radius: 20px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                margin-bottom: 30px;
                text-align: center;
            }
            .header h1 {
                color: #667eea;
                font-size: 2.5em;
                margin-bottom: 10px;
            }
            .header .version {
                color: #666;
                font-size: 1.1em;
            }
            .header p {
                color: #444;
                margin-top: 15px;
                font-size: 1.2em;
            }
            .features {
                background: white;
                padding: 30px;
                border-radius: 15px;
                box-shadow: 0 10px 40px rgba(0,0,0,0.2);
                margin-bottom: 30px;
            }
            .features h2 {
                color: #667eea;
                margin-bottom: 20px;
                border-bottom: 3px solid #667eea;
                padding-bottom: 10px;
            }
            .features ul {
                list-style: none;
            }
            .features li {
                padding: 10px 0;
                color: #444;
                font-size: 1.1em;
            }
            .features li:before {
                content: "✓ ";
                color: #667eea;
                font-weight: bold;
                margin-right: 10px;
            }
            .endpoints {
                background: white;
                padding: 30px;
                border-radius: 15px;
                box-shadow: 0 10px 40px rgba(0,0,0,0.2);
                margin-bottom: 30px;
            }
            .endpoints h2 {
                color: #667eea;
                margin-bottom: 20px;
                border-bottom: 3px solid #667eea;
                padding-bottom: 10px;
            }
            .endpoint-group {
                margin-bottom: 30px;
            }
            .endpoint-group h3 {
                color: #764ba2;
                margin-bottom: 15px;
                font-size: 1.5em;
            }
            .endpoint {
                background: #f8f9fa;
                padding: 20px;
                border-radius: 10px;
                margin-bottom: 15px;
                border-left: 4px solid #667eea;
            }
            .endpoint .method {
                display: inline-block;
                background: #667eea;
                color: white;
                padding: 5px 15px;
                border-radius: 5px;
                font-weight: bold;
                margin-right: 10px;
            }
            .endpoint .path {
                color: #764ba2;
                font-family: 'Courier New', monospace;
                font-weight: bold;
                font-size: 1.1em;
            }
            .endpoint .description {
                margin: 10px 0;
                color: #555;
            }
            .endpoint .params {
                margin: 10px 0;
                color: #666;
                font-size: 0.95em;
            }
            .endpoint .params strong {
                color: #333;
            }
            .endpoint .example {
                background: #2d3748;
                color: #68d391;
                padding: 15px;
                border-radius: 5px;
                margin-top: 10px;
                font-family: 'Courier New', monospace;
                font-size: 0.9em;
                overflow-x: auto;
                white-space: pre-wrap;
                word-break: break-all;
            }
            .docs-links {
                background: white;
                padding: 30px;
                border-radius: 15px;
                box-shadow: 0 10px 40px rgba(0,0,0,0.2);
                text-align: center;
            }
            .docs-links h2 {
                color: #667eea;
                margin-bottom: 20px;
            }
            .docs-links a {
                display: inline-block;
                background: #667eea;
                color: white;
                padding: 15px 30px;
                margin: 10px;
                border-radius: 10px;
                text-decoration: none;
                font-weight: bold;
                transition: all 0.3s;
            }
            .docs-links a:hover {
                background: #764ba2;
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(0,0,0,0.2);
            }
            .footer {
                text-align: center;
                color: white;
                margin-top: 30px;
                padding: 20px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🚀 Base.vn Proxy API</h1>
                <div class="version">Version 0.1.0</div>
                <p>Complete REST API Wrapper cho Base.vn Hiring Platform</p>
            </div>

            <div class="features">
                <h2>✨ Tính năng</h2>
                <ul>
                    <li>Proxy hoàn chỉnh cho Base.vn Public APIs</li>
                    <li>Tự động xử lý và format dữ liệu ứng viên</li>
                    <li>Xử lý lỗi và validation đầy đủ</li>
                    <li>Interactive API documentation (Swagger UI)</li>
                    <li>Thiết kế RESTful endpoints chuẩn</li>
                </ul>
            </div>

            <div class="endpoints">
                <h2>📡 API Endpoints</h2>
                
                <div class="endpoint-group">
                    <h3>👔 Openings (Vị trí tuyển dụng)</h3>
                    
                    <div class="endpoint">
                        <div>
                            <span class="method">POST</span>
                            <span class="path">/openings</span>
                        </div>
                        <div class="description">Lấy danh sách các vị trí tuyển dụng</div>
                        <div class="params">
                            <strong>Parameters:</strong> access_token, page, num_per_page, order_by
                        </div>
                        <div class="example">curl -X POST 'http://localhost:8000/openings?access_token=token&page=1&num_per_page=50&order_by=starred'</div>
                    </div>
                    
                    <div class="endpoint">
                        <div>
                            <span class="method">POST</span>
                            <span class="path">/opening/{opening_id}</span>
                        </div>
                        <div class="description">Lấy chi tiết của một vị trí tuyển dụng</div>
                        <div class="params">
                            <strong>Parameters:</strong> access_token, opening_id
                        </div>
                        <div class="example">curl -X POST 'http://localhost:8000/opening/9346?access_token=token'</div>
                    </div>
                </div>

                <div class="endpoint-group">
                    <h3>👥 Candidates (Ứng viên)</h3>
                    
                    <div class="endpoint">
                        <div>
                            <span class="method">POST</span>
                            <span class="path">/candidates</span>
                        </div>
                        <div class="description">Lấy danh sách ứng viên với dữ liệu đã được xử lý</div>
                        <div class="params">
                            <strong>Parameters:</strong> access_token, opening_id, page, num_per_page, stage
                        </div>
                        <div class="example">curl -X POST 'http://localhost:8000/candidates?access_token=token&opening_id=9346&page=1&num_per_page=50&stage=75440'</div>
                    </div>
                    
                    <div class="endpoint">
                        <div>
                            <span class="method">POST</span>
                            <span class="path">/candidate/{candidate_id}</span>
                        </div>
                        <div class="description">Lấy chi tiết của một ứng viên</div>
                        <div class="params">
                            <strong>Parameters:</strong> access_token, candidate_id
                        </div>
                        <div class="example">curl -X POST 'http://localhost:8000/candidate/518156?access_token=token'</div>
                    </div>
                    
                    <div class="endpoint">
                        <div>
                            <span class="method">POST</span>
                            <span class="path">/candidate/{candidate_id}/messages</span>
                        </div>
                        <div class="description">Lấy lịch sử tin nhắn của một ứng viên</div>
                        <div class="params">
                            <strong>Parameters:</strong> access_token, candidate_id
                        </div>
                        <div class="example">curl -X POST 'http://localhost:8000/candidate/510943/messages?access_token=token'</div>
                    </div>
                </div>
            </div>

            <div class="docs-links">
                <h2>📚 Tài liệu API</h2>
                <a href="/docs" target="_blank">Interactive API Docs (Swagger UI)</a>
                <a href="/openapi.json" target="_blank">OpenAPI Schema</a>
                <a href="/" target="_blank">JSON API Info</a>
            </div>

            <div class="footer">
                <p>Built with ❤️ using FastAPI | Base.vn Proxy API v0.1.0</p>
            </div>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)


@app.get("/")
def read_root():
    """Root endpoint with comprehensive API information and examples."""
    return {
        "message": "Base.vn Proxy API - Complete API Wrapper",
        "version": "0.1.0",
        "description": "A complete REST API wrapper for Base.vn hiring platform public APIs",
        "documentation": {
            "interactive_docs": "/docs",
            "openapi_schema": "/openapi.json"
        },
        "endpoints": {
            "openings": {
                "list": {
                    "method": "POST",
                    "path": "/openings",
                    "description": "Get list of job openings",
                    "parameters": ["access_token", "page", "num_per_page", "order_by"],
                    "example": "curl -X POST 'http://localhost:8000/openings?access_token=token&page=1&num_per_page=50&order_by=starred'"
                },
                "get": {
                    "method": "POST",
                    "path": "/opening/{opening_id}",
                    "description": "Get details of a specific opening",
                    "parameters": ["access_token", "opening_id"],
                    "example": "curl -X POST 'http://localhost:8000/opening/9346?access_token=token'"
                }
            },
            "candidates": {
                "list": {
                    "method": "POST",
                    "path": "/candidates",
                    "description": "Get list of candidates with processed data",
                    "parameters": ["access_token", "opening_id", "page", "num_per_page", "stage"],
                    "example": "curl -X POST 'http://localhost:8000/candidates?access_token=token&opening_id=9346&page=1&num_per_page=50&stage=75440'"
                },
                "get": {
                    "method": "POST",
                    "path": "/candidate/{candidate_id}",
                    "description": "Get details of a specific candidate",
                    "parameters": ["access_token", "candidate_id"],
                    "example": "curl -X POST 'http://localhost:8000/candidate/518156?access_token=token'"
                },
                "messages": {
                    "method": "POST",
                    "path": "/candidate/{candidate_id}/messages",
                    "description": "Get message history for a candidate",
                    "parameters": ["access_token", "candidate_id"],
                    "example": "curl -X POST 'http://localhost:8000/candidate/510943/messages?access_token=token'"
                }
            }
        },
        "features": [
            "Complete proxy for Base.vn public APIs",
            "Automatic data processing for candidate lists",
            "Error handling and validation",
            "Interactive API documentation",
            "RESTful endpoint design"
        ]
    }


class OpeningsListParams(BaseModel):
    access_token: str
    page: Optional[int] = 1
    num_per_page: Optional[int] = 50
    order_by: Optional[str] = "starred"


@app.post("/openings")
def openings_list(access_token: str = Query(...), page: int = Query(1), num_per_page: int = Query(50), order_by: str = Query("starred")):
    """Proxy to Base.vn /opening/list endpoint. Returns JSON from upstream."""
    try:
        resp = fetch_openings_list(access_token, page=page, num_per_page=num_per_page, order_by=order_by)
    except ConnectionError as e:
        raise HTTPException(status_code=502, detail=str(e))

    try:
        return resp.json()
    except Exception:
        # return raw text if not JSON
        return {"status_code": resp.status_code, "text": resp.text}


@app.post("/opening/{opening_id}")
def opening_get(opening_id: int, access_token: str = Query(...)):
    """Proxy to Base.vn /opening/get endpoint."""
    try:
        resp = fetch_opening(access_token, opening_id)
    except ConnectionError as e:
        raise HTTPException(status_code=502, detail=str(e))

    try:
        return resp.json()
    except Exception:
        return {"status_code": resp.status_code, "text": resp.text}


@app.post("/candidates")
def candidates(access_token: str = Query(...), opening_id: int = Query(...), page: int = Query(1), num_per_page: int = Query(50), stage: Optional[str] = Query(None)):
    """Get candidate list for an opening and return processed DataFrame summary and raw JSON."""
    try:
        resp = fetch_candidates(access_token, opening_id, page, num_per_page, stage)
    except ConnectionError as e:
        raise HTTPException(status_code=502, detail=str(e))

    if resp.status_code != 200:
        raise HTTPException(status_code=resp.status_code, detail=resp.text)

    try:
        json_data = resp.json()
    except Exception:
        raise HTTPException(status_code=500, detail="Upstream returned non-JSON")

    processed = process_candidate_data(json_data)

    return {
        "metrics": processed.get("metrics"),
        "count_candidates": processed.get("count_candidates"),
        "candidates_table": processed.get("dataframe").to_dict(orient="records") if not processed.get("dataframe").empty else [],
        "raw": json_data
    }


@app.post("/candidate/{candidate_id}")
def candidate_get(candidate_id: int, access_token: str = Query(...)):
    """Proxy to /candidate/get"""
    try:
        resp = fetch_candidate_detail(access_token, candidate_id)
    except ConnectionError as e:
        raise HTTPException(status_code=502, detail=str(e))

    try:
        return resp.json()
    except Exception:
        return {"status_code": resp.status_code, "text": resp.text}


@app.post("/candidate/{candidate_id}/messages")
def candidate_messages(candidate_id: int, access_token: str = Query(...)):
    """Proxy to /candidate/messages"""
    try:
        resp = fetch_candidate_messages(access_token, candidate_id)
    except ConnectionError as e:
        raise HTTPException(status_code=502, detail=str(e))

    try:
        return resp.json()
    except Exception:
        return {"status_code": resp.status_code, "text": resp.text}
