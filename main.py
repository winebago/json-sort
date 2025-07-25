from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import httpx

app = FastAPI()

def sort_json(obj):
    if isinstance(obj, dict):
        return {k: sort_json(obj[k]) for k in sorted(obj.keys())}
    elif isinstance(obj, list):
        return [sort_json(item) for item in obj]
    else:
        return obj

@app.post("/sort")
async def sort_endpoint(request: Request):
    data = await request.json()
    sorted_data = sort_json(data)
    return JSONResponse(content=sorted_data)

@app.get("/sort_url")
async def sort_from_url(url: str):
    """
    Fetch JSON from a public URL, sort its keys recursively, and return the sorted JSON.
    Usage: GET /sort_url?url=<encoded_json_url>
    """
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
        resp.raise_for_status()
        data = resp.json()
    sorted_data = sort_json(data)
    return JSONResponse(content=sorted_data)

@app.get("/")
async def read_root():
    return {"message": "POST JSON to /sort or GET /sort_url?url=<json_url>"}
