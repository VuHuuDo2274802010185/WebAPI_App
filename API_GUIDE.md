# Base.vn Proxy API - Complete Guide

## 🎯 Overview

This is a complete REST API wrapper for Base.vn hiring platform public APIs. It provides a clean, well-documented interface to access all Base.vn hiring endpoints.

## 🚀 Quick Start

### Starting the Server

```bash
# Install dependencies
pip install -r requirements.txt

# Start the server
uvicorn web_api:app --reload --port 8000
```

### Access Points

1. **HTML Documentation Page**: http://localhost:8000/html
   - Beautiful, interactive documentation
   - All endpoints with examples
   - Vietnamese language support

2. **JSON API Information**: http://localhost:8000/
   - Complete API structure in JSON format
   - Programmatic access to endpoint information

3. **Interactive Swagger UI**: http://localhost:8000/docs
   - Try out API calls directly
   - Auto-generated from OpenAPI schema

4. **OpenAPI Schema**: http://localhost:8000/openapi.json
   - Machine-readable API specification

## 📡 API Endpoints

### Openings (Vị trí tuyển dụng)

#### 1. List Openings
```bash
POST /openings
```

**Description**: Get list of job openings

**Parameters**:
- `access_token` (required): Your Base.vn API access token
- `page` (optional, default: 1): Page number
- `num_per_page` (optional, default: 50): Results per page
- `order_by` (optional, default: "starred"): Sort order

**Example**:
```bash
curl -X POST 'http://localhost:8000/openings?access_token=YOUR_TOKEN&page=1&num_per_page=50&order_by=starred'
```

**Response**: JSON object containing list of openings

---

#### 2. Get Opening Details
```bash
POST /opening/{opening_id}
```

**Description**: Get detailed information about a specific job opening

**Parameters**:
- `access_token` (required): Your Base.vn API access token
- `opening_id` (required, in path): The ID of the opening

**Example**:
```bash
curl -X POST 'http://localhost:8000/opening/9346?access_token=YOUR_TOKEN'
```

**Response**: JSON object with opening details

---

### Candidates (Ứng viên)

#### 3. List Candidates
```bash
POST /candidates
```

**Description**: Get list of candidates with automatic data processing

**Parameters**:
- `access_token` (required): Your Base.vn API access token
- `opening_id` (required): The ID of the job opening
- `page` (optional, default: 1): Page number
- `num_per_page` (optional, default: 50): Results per page
- `stage` (optional): Filter by recruitment stage ID

**Example**:
```bash
curl -X POST 'http://localhost:8000/candidates?access_token=YOUR_TOKEN&opening_id=9346&page=1&num_per_page=50&stage=75440'
```

**Response**: JSON object containing:
- `metrics`: Summary statistics (total, count, page)
- `count_candidates`: Number of candidates in response
- `candidates_table`: Processed candidate data in table format
- `raw`: Raw API response from Base.vn

---

#### 4. Get Candidate Details
```bash
POST /candidate/{candidate_id}
```

**Description**: Get detailed information about a specific candidate

**Parameters**:
- `access_token` (required): Your Base.vn API access token
- `candidate_id` (required, in path): The ID of the candidate

**Example**:
```bash
curl -X POST 'http://localhost:8000/candidate/518156?access_token=YOUR_TOKEN'
```

**Response**: JSON object with candidate details

---

#### 5. Get Candidate Messages
```bash
POST /candidate/{candidate_id}/messages
```

**Description**: Get message/note history for a specific candidate

**Parameters**:
- `access_token` (required): Your Base.vn API access token
- `candidate_id` (required, in path): The ID of the candidate

**Example**:
```bash
curl -X POST 'http://localhost:8000/candidate/510943/messages?access_token=YOUR_TOKEN'
```

**Response**: JSON object with message history

---

## 🔒 Authentication

All endpoints require a valid `access_token` from Base.vn. You can obtain this token from your Base.vn account settings.

**Important**: 
- Keep your access token secure
- Do not commit tokens to version control
- Use environment variables or secrets management in production

## 📝 Response Format

### Success Response
```json
{
  // Endpoint-specific data
}
```

### Error Response
```json
{
  "detail": "Error message describing what went wrong"
}
```

### HTTP Status Codes
- `200`: Success
- `502`: Bad Gateway (connection error to Base.vn API)
- `4xx`: Client error (invalid parameters, authentication failed, etc.)
- `5xx`: Server error

## 🛠️ Features

✅ **Complete API Coverage**
- All 5 Base.vn public API endpoints are wrapped

✅ **Data Processing**
- Automatic candidate data transformation
- Formatted tables for easy consumption

✅ **Error Handling**
- Comprehensive error messages
- Proper HTTP status codes

✅ **Documentation**
- Multiple documentation formats
- Interactive testing via Swagger UI

✅ **RESTful Design**
- Standard HTTP methods
- Intuitive URL structure
- Consistent response formats

## 🧪 Testing

Run the test suite to verify all endpoints:

```bash
python test_api.py
```

Or test individual endpoints using curl (see examples above).

## 📚 Additional Resources

- **Base.vn API Documentation**: Check Base.vn official documentation
- **FastAPI Documentation**: https://fastapi.tiangolo.com/
- **OpenAPI Specification**: https://swagger.io/specification/

## 🤝 Contributing

This is a proxy API that wraps Base.vn public APIs. For issues related to:
- The proxy API itself: Open an issue in this repository
- Base.vn API behavior: Contact Base.vn support

## 📄 License

See LICENSE file for details.

---

**Built with ❤️ using FastAPI | Version 0.1.0**
