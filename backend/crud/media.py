from models.media import Media
from database import mediaCollection
from helper.instagramdata import scraper
from bson import ObjectId
import logging

async def post_media(request):
    try:
        post_details = scraper(request.profile_id, request.num_posts)
        if not post_details:
            logging.warning("No post details found.")
            return False

        # Insert scraped data into MongoDB
        for post in post_details:
            media = {
                "media": post.media,  # Access attributes directly
                "description": post.description,
                "thumbnail": post.thumbnail,
                "video_url":post.video_url
            }
            result = await mediaCollection.insert_one(media)
            if result.inserted_id:
                logging.info(f"Successfully inserted post: {post}")
            else:
                logging.error(f"Failed to insert post: {post}")
        return {"posts": post_details}

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return False



async def get_media():
    medias = []
    cursor = mediaCollection.find({})
    async for document in cursor:
        document["id"]=str(document["_id"])
        medias.append(Media(**document))
    return medias


async def get_single_media(id):
    document = await mediaCollection.find_one({"_id": ObjectId(id)})
    if document:
        document['id'] = str(document['_id'])  # Convert ObjectId to string
        return Media(**document)
    return None