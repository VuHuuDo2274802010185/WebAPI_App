from typing import Optional
import os
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from api_client import fetch_openings_list, fetch_opening, fetch_candidates
from data_processor import process_candidate_data
from api_client import fetch_candidate_detail, fetch_candidate_messages

app = FastAPI(title="Base.vn Proxy API", version="0.1.0")


@app.get("/")
def read_root():
    """Root endpoint with a short message and pointer to interactive docs."""
    return {"message": "Base.vn proxy API running.", "docs": "/docs"}


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
