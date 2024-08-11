
from fastapi import APIRouter,HTTPException
from models.scraperequest import ScrapeRequest
from crud.media import post_media,get_media,get_single_media
from models.media import Media
from  helper.instagramdata import scraper
from helper.scrapepost import scrape_post

router = APIRouter()


@router.post("/scrape/")
async def scrape(request: ScrapeRequest):
    response = await post_media(request)
    return response
    
# @router.get("/media")
# async def get_media_data():
#     response = await get_media()
#     if response:
#         return response
#     raise HTTPException(404, f"There is no medias")

@router.get("/media/{profile_name}")
async def get_media_data(profile_name):
    response = scraper(profile_name,5)
    mediaCollection = []
    if response:
        for post in response:
             media = {
                "post_id":post.post_id,
                "media": post.media,
                "description": post.description,
                "thumbnail": post.thumbnail,
                "video_url":post.video_url
            }
             mediaCollection.append(media)
        return mediaCollection
    raise HTTPException(404, f"There is no medias")
    
    
@router.get("/media/post/{post_id}")
async def get_media_post(post_id):
    response = scrape_post(post_id)
    if response:
        return response
    raise HTTPException(404, f"There is no media")

    
    
@router.get("/media/{id}",response_model=Media)
async def get_media_by_id(id):
    response = await get_single_media(id)
    if response:
        return response
    raise HTTPException(404, f"There is no media")

    