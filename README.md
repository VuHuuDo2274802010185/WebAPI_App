# WebAPI_App

This repository contains utilities and a small proxy web API for the public Base.vn hiring API.

Files of interest:

- `api_client.py` - helper functions that call Base.vn public endpoints.
- `data_processor.py` - transforms candidate JSON into a pandas DataFrame and metrics.
- `web_api.py` - FastAPI application that exposes three endpoints:
	- POST `/openings` - proxies `/opening/list` on hiring.base.vn
	- POST `/opening/{id}` - proxies `/opening/get` for a given opening id
	- POST `/candidates` - fetches candidate list and returns processed table + raw JSON

Requirements and run
--------------------

Install dependencies (prefer virtualenv):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Run the FastAPI server with uvicorn:

```powershell
uvicorn web_api:app --reload --port 8000
```

Examples (curl):

```powershell
curl -X POST "http://127.0.0.1:8000/openings" -d "access_token=token&page=1&num_per_page=50&order_by=starred"

curl -X POST "http://127.0.0.1:8000/opening/9346" -d "access_token=token"

curl -X POST "http://127.0.0.1:8000/candidates" -d "access_token=token&opening_id=9346&page=1&num_per_page=50&stage=75440"
```

Candidate detail & messages examples:

```powershell
curl -X POST "http://127.0.0.1:8000/candidate/518156" -d "access_token=token"

curl -X POST "http://127.0.0.1:8000/candidate/510943/messages" -d "access_token=token"
```
```

Notes
-----
- Keep your access tokens secret. Consider using `.env` for local development (existing `app.py` uses python-dotenv).
- The `web_api.py` is a lightweight proxy — it does not add authentication. Add auth or rate-limiting for production.

