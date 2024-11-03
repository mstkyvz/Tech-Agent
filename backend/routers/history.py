from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database.database import get_db
from models import models
from schemas import schemas
from services.video_service import video_database
from utils.utils import *
import json

router = APIRouter()

@router.post("/save_chat_history/", response_model=schemas.ChatHistoryResponse)
async def save_chat_history(
    chat_history: schemas.ChatHistoryCreate,
    db: Session = Depends(get_db)
):
    messages_hash = calculate_chat_hash(chat_history.messages)
    
    existing_chat = db.query(models.ChatHistory).filter(
        models.ChatHistory.title == chat_history.title
    ).first()
    
    if existing_chat:
        try:
            existing_chat.messages = json.dumps(chat_history.messages)
            existing_chat.messages_hash = messages_hash
            db.commit()
            db.refresh(existing_chat)
            return existing_chat
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=str(e))
    
    db_chat_history = models.ChatHistory(
        id=chat_history.title,
        title=chat_history.title,
        messages=json.dumps(chat_history.messages),
        messages_hash=messages_hash
    )
    
    try:
        db.add(db_chat_history)
        db.commit()
        db.refresh(db_chat_history)
        return db_chat_history
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/get_chat_history/{history_id}", response_model=schemas.ChatHistoryFull)
async def get_chat_history(history_id: str, db: Session = Depends(get_db)):
    try:
        chat_history = db.query(models.ChatHistory).filter(
            models.ChatHistory.id == history_id
        ).first()
        
        if chat_history is None:
            raise HTTPException(status_code=404, detail="Chat history not found")
        
        return {
            "id": chat_history.id,
            "title": chat_history.title,
            "timestamp": chat_history.timestamp,
            "messages": json.loads(chat_history.messages)
        }
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Error decoding messages from database")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/get_all_histories/", response_model=List[schemas.ChatHistoryResponse])
async def get_all_histories(db: Session = Depends(get_db)):
    try:
        histories = db.query(models.ChatHistory).order_by(
            models.ChatHistory.timestamp.desc()
        ).all()
        return histories
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/delete_chat_history/{history_id}")
async def delete_chat_history(history_id: str, db: Session = Depends(get_db)):
    try:
        chat_history = db.query(models.ChatHistory).filter(
            models.ChatHistory.id == history_id
        ).first()
        
        if chat_history is None:
            raise HTTPException(status_code=404, detail="Chat history not found")
        
        db.delete(chat_history)
        db.commit()
        if history_id in video_database:
            del video_database[history_id]
        return {"message": "Chat history deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))