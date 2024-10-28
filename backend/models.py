from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from database import Base

class ChatHistory(Base):
    __tablename__ = "chat_histories"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    messages = Column(Text)
    messages_hash = Column(String(64), unique=True, index=True) 
    timestamp = Column(DateTime(timezone=True), server_default=func.now())