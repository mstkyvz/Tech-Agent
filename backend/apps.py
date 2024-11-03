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
import threading
import queue
import time
from langchain_community.tools import DuckDuckGoSearchRun
from pypdf import PdfReader
# Initialize database
models.Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

# Database session dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Initialize global variables
video_database = {}
video_queue = queue.Queue()
video_threads = {}
MAX_CONCURRENT_VIDEOS = 3

search = DuckDuckGoSearchRun()
# Configure Gemini AI
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

class VideoCreate(BaseModel):
    id: str

class VideoStatus(BaseModel):
    status: str
    video_url: Optional[str] = None

def video_worker():
    """Worker function that processes videos from the queue"""
    while True:
        try:
            video_id = video_queue.get()
            if video_id is None:  
                break
                
            try:
                
                video_database[video_id]["status"] = "processing"
                
                
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(create_videos.run(video_id))
                loop.close()
                
                video_path = f"/static/videomedia/videos/1080p60/{video_id}.mp4"
                video_database[video_id].update({
                    "status": "completed",
                    "video_url": video_path,
                    "created_at": datetime.now()
                })
            except Exception as e:
                print(f"Error processing video {video_id}: {str(e)}")
                video_database[video_id].update({
                    "status": "error",
                    "error": str(e),
                    "created_at": datetime.now()
                })
            finally:
                video_queue.task_done()
                if video_id in video_threads:
                    del video_threads[video_id]
                
        except Exception as e:
            print(f"Worker thread error: {str(e)}")
            continue

# Start worker threads
worker_threads = []
for _ in range(MAX_CONCURRENT_VIDEOS):
    t = threading.Thread(target=video_worker, daemon=True)
    t.start()
    worker_threads.append(t)

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

def build_prompt(message: str, history: List[dict], types,extra=None) -> List[Dict[str, Any]]:
    if types == "question":
        messages = [{'role': 'user', 'parts': prompt.system_prompt_question}]
    elif types == "create_question":
            messages = [{'role': 'user', 'parts': prompt.system_prompt_create_question}]
    else:
        try:
            internet_search=search.invoke(message)
        except:
            internet_search=""
        try:
            messages = [{'role': 'user', 'parts': prompt.system_prompt_konu.format(internet_search,extra)}]
        except:
            messages = [{'role': 'user', 'parts': prompt.system_prompt_konu}]
    
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
    print(messages)
    return messages

async def send_message(message: str, history: List[dict], image_data: Optional[bytes] = None, types="question",extra=None):
    try:
        content = build_prompt(message, history, types,extra)

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

async def create_video_task(video_id: str):
    try:
        # Check if video already exists
        video_path = f"/static/videomedia/videos/1080p60/{video_id}.mp4"
        if os.path.exists("../frontend/build" + video_path):
            if video_id not in video_database:
                video_database[video_id] = {
                    "status": "completed",
                    "video_url": video_path,
                    "created_at": datetime.now()
                }
            return

        # Add to queue if not already being processed
        if video_id not in video_threads:
            video_threads[video_id] = threading.current_thread()
            video_queue.put(video_id)
            
    except Exception as e:
        print(f"Error queuing video {video_id}: {str(e)}")
        video_database[video_id] = {
            "status": "error",
            "error": str(e),
            "created_at": datetime.now()
        }

def calculate_chat_hash(messages: List[Dict]) -> str:
    hash_content = []
    for msg in messages:
        hash_content.append({
            'type': msg['type'],
            'content': msg['content']
        })
    
    message_str = json.dumps(hash_content, sort_keys=True)
    return hashlib.sha256(message_str.encode()).hexdigest()

# API Endpoints

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
            async for chunk in send_message(message, chat_history, contents, "create_question"):
                yield chunk.encode('utf-8')
        
        return StreamingResponse(
            stream_response(),
            media_type="text/plain"
        )
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid history format")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

def clean_text(text: str) -> str:
    if not text:
        return ""

    cleaned_text = ' '.join(text.split())
    return cleaned_text

@app.post("/api/chat_konu/")
async def chat_endpoint(
    message: str = Form(...),
    file: Optional[UploadFile] = File(None),
    history: str = Form(default="[]")
) -> StreamingResponse:
    try:
        chat_history = json.loads(history)
        print(file)
        if file:
            contents = await file.read()
            try:
                pdf_file = io.BytesIO(contents)
                reader = PdfReader(pdf_file)
                text = "\n\n".join(page.extract_text() for page in reader.pages if page.extract_text())
                text = clean_text(text)
            except Exception as e:
                print(f"An error occurred while reading the PDF: {e}")
                text = ""
        else:
            text=""        
        async def stream_response():
            async for chunk in send_message(message, chat_history, None, "konu",text):
                yield chunk.encode('utf-8')
        
        return StreamingResponse(
            stream_response(),
            media_type="text/plain"
        )
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid history format")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

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
async def get_chat_history(history_id: str, db: Session = Depends(get_db)):
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

@app.post("/api/create_video")
async def create_video(video_data: VideoCreate):
    video_id = video_data.id
    
    # Check if video already exists
    video_path = f"/static/videomedia/videos/1080p60/{video_id}.mp4"
    if os.path.exists("../frontend/build" + video_path):
        if video_id not in video_database:
            video_database[video_id] = {
                "status": "completed",
                "video_url": video_path,
                "created_at": datetime.now()
            }
        return VideoStatus(status=video_database[video_id]["status"])
    

    if video_id in video_database:
        return VideoStatus(status=video_database[video_id]["status"])
    
    video_database[video_id] = {"status": "queued"}
    asyncio.create_task(create_video_task(video_id))
    
    return VideoStatus(status="queued")

@app.get("/api/check_video/{video_id}")
async def check_video(video_id: str):
    print(video_id, video_database)
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

# Shutdown event handler
@app.on_event("shutdown")
async def shutdown_event():
    # Send poison pills to stop worker threads
    for _ in worker_threads:
        video_queue.put(None)
    
    # Wait for all threads to complete
    for t in worker_threads:
        t.join()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    #uvicorn.run(app, host="0.0.0.0", port=8000,ssl_keyfile="/home/gozerutime/key.pem",ssl_certfile="/home/gozerutime/cert.pem")