from fastapi import FastAPI, HTTPException, APIRouter, Response
import requests
from aiocache import cached, Cache
import aiohttp

app = FastAPI()
router = APIRouter()

@router.get("/proxy/instagram")
@cached(ttl=3600, cache=Cache.MEMORY)
async def proxy_instagram(url: str):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status != 200:
                    raise HTTPException(status_code=response.status, detail="Failed to fetch the content")
                content = await response.read()
                return Response(content=content, media_type=response.headers['Content-Type'])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

app.include_router(router)
