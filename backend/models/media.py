from pydantic import BaseModel
from typing import List, Optional

class Media(BaseModel):
    id: Optional[str] = None
    description: Optional[str] = None
    media: Optional[List[str]] = None
    video_url: Optional[str] = None
    thumbnail: Optional[str] = None
