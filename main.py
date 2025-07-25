# main.py
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

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
