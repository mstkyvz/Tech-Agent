from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from database import Base

class ChatHistory(Base):
    __tablename__ = "chat_histories"
    
    id = Column(String, primary_key=True) 
    title = Column(String, unique=True, nullable=False)
    messages = Column(Text, nullable=False)
    messages_hash = Column(String, unique=True, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())