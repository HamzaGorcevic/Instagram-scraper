from pydantic import BaseModel
class ScrapeRequest(BaseModel):
    profile_id: str
    num_posts: int = 5
