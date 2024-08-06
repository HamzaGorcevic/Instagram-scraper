
from fastapi import APIRouter,HTTPException
from models.scraperequest import ScrapeRequest
from crud.media import post_media,get_media,get_single_media
from models.media import Media
router = APIRouter()

@router.post("/scrape/")
async def scrape(request: ScrapeRequest):
    response = await post_media(request)
    return response
    
@router.get("/media")
async def get_media_data():
    response = await get_media()
    if response:
        return response
    raise HTTPException(404, f"There is no medias")
    
@router.get("/media/{id}",response_model=Media)
async def get_media_by_id(id):
    response = await get_single_media(id)
    if response:
        return response
    raise HTTPException(404, f"There is no media")

    