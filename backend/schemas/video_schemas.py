from pydantic import BaseModel
from typing import Optional

class ChatMessage(BaseModel):
    type: str
    content: str
    timestamp: str
    image: Optional[str] = None

class VideoCreate(BaseModel):
    id: str

class VideoStatus(BaseModel):
    status: str
    video_url: Optional[str] = None