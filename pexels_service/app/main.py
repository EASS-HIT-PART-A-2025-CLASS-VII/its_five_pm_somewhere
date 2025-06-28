import os
from fastapi import FastAPI, HTTPException
import httpx
from dotenv import load_dotenv
from app.models import ImageSearchRequest


load_dotenv()
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY", "")
PEXELS_BASE_URL = "https://api.pexels.com/v1/search"

app = FastAPI()


@app.post("/images", response_model=list[int])
async def fetch_images(request: ImageSearchRequest):
    headers = {"Authorization": PEXELS_API_KEY}
    params = {"query": request.name, "per_page": request.count, "page": request.page}
    async with httpx.AsyncClient() as client:
        response = await client.get(PEXELS_BASE_URL, headers=headers, params=params)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Pexels API error")
    photos = response.json().get("photos", [])
    return [photo["id"] for photo in photos]
