from typing import AsyncIterable, List, Optional, Dict, Any
from pydantic import BaseModel
from fastapi import FastAPI, Form, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
from PIL import Image
import io
import json
import asyncio
from datetime import datetime
import pathlib
import prompt
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import json
import hashlib
import os
import models
import schemas
from database import SessionLocal, engine
import create_videos
from generate_auido import generate_audio
from fastapi.staticfiles import StaticFiles

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

video_database = {}        
genai.configure(api_key='AIzaSyCeusRpeamEuHVVRrNCwmu0XtDj_QL8mXc')
model = genai.GenerativeModel('gemini-1.5-pro')  

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatMessage(BaseModel):
    type: str
    content: str
    timestamp: str
    image: Optional[str] = None

def process_gemini_response(response):
    try:
        for chunk in response:
            if hasattr(chunk, 'text'):
                yield chunk.text
            elif isinstance(chunk, str):
                yield chunk
    except Exception as e:
        yield f"Error processing response: {str(e)}"

def create_content_parts(message: str, image_data: Optional[bytes] = None) -> List[genai.protos.Content]:
    parts = []
    
    parts.append(genai.protos.Part(text=message))
    
    if image_data:
        parts.append(
            genai.protos.Part(
                inline_data=genai.protos.Blob(
                    mime_type='image/jpeg',
                    data=image_data
                )
            )
        )
    
    return genai.protos.Content(parts=parts)

def build_prompt(message: str, history: List[dict],types) -> List[Dict[str, Any]]:
    if types=="question":
        messages = [{'role':'user','parts':prompt.system_prompt_question}]
    elif types=="create_question":
        messages = [{'role':'user','parts':prompt.system_prompt_question}]
    else:
        messages = [{'role':'user','parts':prompt.system_prompt_konu}]
    
    for msg in history:
        role = "user" if msg['type'] == 'user' else "model"
        messages.append({
            'role': role,
            'parts': [msg['content']]
        })
    
    messages.append({
        'role': 'user',
        'parts': [message]
    })
    
    return messages

async def send_message(message: str, history: List[dict], image_data: Optional[bytes] = None,types="question"):
    try:
        content = build_prompt(message, history,types)

        if image_data:
            content_parts = create_content_parts(message, image_data)
            response = model.generate_content(content_parts, stream=True)
        else:
            response = model.generate_content(content, stream=True)
        
        for chunk in process_gemini_response(response):
            yield chunk
            await asyncio.sleep(0.01)
            
    except Exception as e:
        yield f"Error in message processing: {str(e)}"

@app.post("/api/chat_question/")
async def chat_endpoint(
    message: str = Form(...),
    file: Optional[UploadFile] = File(None),
    history: str = Form(default="[]")
) -> StreamingResponse:
    try:
        chat_history = json.loads(history)
        
        contents = None
        if file:
            if not file.content_type.startswith('image/'):
                raise HTTPException(status_code=400, detail="Only image files are supported")
            contents = await file.read()
            
        async def stream_response():
            async for chunk in send_message(message, chat_history, contents):
                yield chunk.encode('utf-8')
        
        return StreamingResponse(
            stream_response(),
            media_type="text/plain"
        )
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid history format")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")
    
    
@app.post("/api/chat_create_question/")
async def chat_endpoint(
    message: str = Form(...),
    file: Optional[UploadFile] = File(None),
    history: str = Form(default="[]")
) -> StreamingResponse:
    try:
        chat_history = json.loads(history)
        
        contents = None
        if file:
            if not file.content_type.startswith('image/'):
                raise HTTPException(status_code=400, detail="Only image files are supported")
            contents = await file.read()
            
        async def stream_response():
            async for chunk in send_message(message, chat_history, contents,"create_question"):
                yield chunk.encode('utf-8')
        
        return StreamingResponse(
            stream_response(),
            media_type="text/plain"
        )
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid history format")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")
    
    
@app.post("/api/chat_konu/")
async def chat_endpoint(
    message: str = Form(...),
    file: Optional[UploadFile] = File(None),
    history: str = Form(default="[]")
) -> StreamingResponse:
    try:
        chat_history = json.loads(history)
        
        contents = None
        if file:
            if not file.content_type.startswith('image/'):
                raise HTTPException(status_code=400, detail="Only image files are supported")
            contents = await file.read()
            
        async def stream_response():
            async for chunk in send_message(message, chat_history, contents,"konu"):
                yield chunk.encode('utf-8')
        
        return StreamingResponse(
            stream_response(),
            media_type="text/plain"
        )
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid history format")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")


def calculate_chat_hash(messages: List[Dict]) -> str:
    """
    Calculate a hash of chat messages to check for duplicates.
    Only considers the content and type of messages, ignoring timestamps.
    """
    hash_content = []
    for msg in messages:
        
        hash_content.append({
            'type': msg['type'],
            'content': msg['content']
        })
    
    
    message_str = json.dumps(hash_content, sort_keys=True)
    return hashlib.sha256(message_str.encode()).hexdigest()


@app.post("/api/save_chat_history/", response_model=schemas.ChatHistoryResponse)
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
            raise HTTPException(
                status_code=500,
                detail=f"Error updating chat history: {str(e)}"
            )
    
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
        raise HTTPException(
            status_code=500,
            detail=f"Error saving chat history: {str(e)}"
        )

@app.get("/api/get_chat_history/{history_id}", response_model=schemas.ChatHistoryFull)
async def get_chat_history(history_id: str, db: Session = Depends(get_db)):  # Changed to str
    try:
        chat_history = db.query(models.ChatHistory).filter(
            models.ChatHistory.id == history_id
        ).first()
        
        if chat_history is None:
            raise HTTPException(
                status_code=404,
                detail="Chat history not found"
            )
        
        return {
            "id": chat_history.id,
            "title": chat_history.title,
            "timestamp": chat_history.timestamp,
            "messages": json.loads(chat_history.messages)
        }
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=500,
            detail="Error decoding messages from database"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving chat history: {str(e)}"
        )

@app.get("/api/get_all_histories/", response_model=List[schemas.ChatHistoryResponse])
async def get_all_histories(db: Session = Depends(get_db)):
    try:
        histories = db.query(models.ChatHistory).order_by(
            models.ChatHistory.timestamp.desc()
        ).all()
        return histories
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving chat histories: {str(e)}"
        )


@app.delete("/api/delete_chat_history/{history_id}")
async def delete_chat_history(history_id: str, db: Session = Depends(get_db)):
    try:
        chat_history = db.query(models.ChatHistory).filter(
            models.ChatHistory.id == history_id
        ).first()
        
        if chat_history is None:
            raise HTTPException(
                status_code=404,
                detail="Chat history not found"
            )
        
        db.delete(chat_history)
        db.commit()
        if history_id in video_database:
            del video_database[history_id]
        return {"message": "Chat history deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error deleting chat history: {str(e)}"
        )




class VideoCreate(BaseModel):
    id: str

class VideoStatus(BaseModel):
    status: str
    video_url: Optional[str] = None

async def create_video_task(video_id: str):
    try:

        video_path = f"/static/videomedia/videos/1080p60/{video_id}.mp4"  
        if os.path.exists("../frontend/build"+video_path):
            if not video_id in video_database:
                video_database[video_id] = {
                    "status": "completed",
                    "video_url": video_path,
                    "created_at": datetime.now()
                }
            return
        await create_videos.run(video_id)
        
    
        video_database[video_id] = {
            "status": "completed",
            "video_url": video_path,
            "created_at": datetime.now()
        }
    except Exception as e:
        print(f"Error {e}")
        # video_database[video_id] = {
        #     "status": "error",
        #     "error": str(e),
        #     "created_at": datetime.now()
        # }

@app.post("/api/create_video")
async def create_video(video_data: VideoCreate):
    video_id = video_data.id
    
    video_path = f"/static/videomedia/videos/1080p60/{video_id}.mp4"  
    if os.path.exists("../frontend/build"+video_path):
            if not video_id in video_database:
                video_database[video_id] = {
                    "status": "completed",
                    "video_url": video_path,
                    "created_at": datetime.now()
                }
            return VideoStatus(status=video_database[video_id]["status"])
    if video_id in video_database:
        return VideoStatus(status=video_database[video_id]["status"])
    
    video_database[video_id] = {"status": "processing"}
    
    asyncio.create_task(create_video_task(video_id))
    
    return VideoStatus(status="processing")


@app.get("/api/check_video/{video_id}")
async def check_video(video_id: str):
    print(video_id,video_database)
    if video_id not in video_database:
        return VideoStatus(status="not_found")
    
    video_info = video_database[video_id]
    return VideoStatus(
        status=video_info["status"],
        video_url=video_info.get("video_url")
    )


@app.delete("/api/delete_video/{video_id}")
async def delete_video(video_id: str):
    if video_id not in video_database:
        raise HTTPException(status_code=404, detail="Video not found")
    
    del video_database[video_id]
    return {"message": "Video deleted successfully"}




@app.post("/api/upload-pdf/")
async def upload_pdf(file: UploadFile = File(...)):

    with open("temp.pdf", "wb") as buffer:
        buffer.write(await file.read())
    
    audio_file_path = generate_audio("temp.pdf")
    
    return {"audio_file": audio_file_path}

@app.get("/api/audio/{filename}")
async def get_audio(filename: str):
    return FileResponse(f"/home/gozerutime/static/tmp/{filename}", media_type="audio/mpeg")



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    #uvicorn.run(app, host="0.0.0.0", port=8000,ssl_keyfile="/home/gozerutime/key.pem",ssl_certfile="/home/gozerutime/cert.pem")
