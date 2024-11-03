from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from database.database import Base

class ChatHistory(Base):
    """ChatHistory, kullanıcıların sohbet geçmişlerini temsil eden bir veritabanı modelidir."""
    
    __tablename__ = "chat_histories"
    
    id: str = Column(String, primary_key=True) 
    title: str = Column(String, unique=True, nullable=False)
    messages: str = Column(Text, nullable=False)
    messages_hash: str = Column(String, unique=True, nullable=False)
    timestamp: DateTime = Column(DateTime(timezone=True), server_default=func.now())
