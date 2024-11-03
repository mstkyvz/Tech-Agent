from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class MessageBase(BaseModel):
    """Temel mesaj modelini temsil eder."""
    type: str
    content: str
    timestamp: str
    image: Optional[str] = None

class ChatHistoryCreate(BaseModel):
    """Yeni bir sohbet geçmişi oluşturmak için kullanılan model."""
    title: str
    messages: List[dict]

class ChatHistoryResponse(BaseModel):
    """Sohbet geçmişi yanıt modelini temsil eder."""
    id: str  
    title: str
    timestamp: datetime

    class Config:
        """Pydantic yapılandırması."""
        from_attributes = True

class ChatHistoryFull(ChatHistoryResponse):
    """Tam sohbet geçmişi modelini temsil eder; mesajları içerir."""
    messages: List[dict]
