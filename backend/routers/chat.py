from fastapi import APIRouter, Form, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from typing import Optional
import json
import asyncio
from services.gemini_service import send_message
from utils.pdf_utils import process_pdf_file

router = APIRouter()

@router.post("/chat_question/")
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
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/chat_create_question/")
async def chat_create_endpoint(
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
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/chat_konu/")
async def chat_konu_endpoint(
    message: str = Form(...),
    file: Optional[UploadFile] = File(None),
    history: str = Form(default="[]")
) -> StreamingResponse:
    try:
        chat_history = json.loads(history)
        text = ""
        if file:
            text = await process_pdf_file(file)
            
        async def stream_response():
            async for chunk in send_message(message, chat_history, None, "konu", text):
                yield chunk.encode('utf-8')
        
        return StreamingResponse(
            stream_response(),
            media_type="text/plain"
        )
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid history format")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))