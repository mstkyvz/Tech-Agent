from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class MessageBase(BaseModel):
    type: str
    content: str
    timestamp: str
    image: Optional[str] = None

class ChatHistoryCreate(BaseModel):
    title: str
    messages: List[dict]

class ChatHistoryResponse(BaseModel):
    id: int
    title: str
    timestamp: datetime

    class Config:
        from_attributes = True

class ChatHistoryFull(ChatHistoryResponse):
    messages: List[dict]