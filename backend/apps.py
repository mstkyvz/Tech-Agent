from typing import AsyncIterable, List, Optional
from pydantic import BaseModel
from fastapi import FastAPI, Form, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
from PIL import Image
import io
import json
import asyncio
from datetime import datetime

app = FastAPI()

genai.configure(api_key='AIzaSyAy3E3BYjXjS6fyrRUbS2m8ip3Sdb3hmqA')
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

async def process_gemini_response(response) -> AsyncIterable[str]:
    """Process the Gemini response and yield chunks of text."""
    try:
        for chunk in response:
            if hasattr(chunk, 'text'):
                yield chunk.text
            elif isinstance(chunk, str):
                yield chunk
            await asyncio.sleep(0.01)
    except Exception as e:
        yield f"Error processing response: {str(e)}"

def build_prompt(message: str, history: List[dict]) -> str:
    """Build a context-aware prompt including chat history."""
    prompt = "Previous conversation:\n"
    
    for msg in history:
        role = "User" if msg['type'] == 'user' else "Assistant"
        prompt += f"{role}: {msg['content']}\n"
    
    prompt += f"\nCurrent message: {message}\n"
    prompt += "\nPlease provide a helpful response based on the conversation context."
    
    return prompt

async def send_message(message: str, history: List[dict], image_data: Optional[bytes] = None) -> AsyncIterable[str]:
    """Send message and optional image to Gemini and stream the response."""
    try:
        prompt = build_prompt(message, history)
        
        if image_data:
            image = Image.open(io.BytesIO(image_data))
            response = model.generate_content([prompt, image], stream=True)
        else:
            response = model.generate_content(prompt, stream=True)
        
        async for chunk in process_gemini_response(response):
            yield chunk
            
    except Exception as e:
        yield f"Error: {str(e)}"

@app.post("/upload/")
async def upload_file(
    message: str = Form(...),
    file: Optional[UploadFile] = File(None),
    history: str = Form(default="[]")
):
    """Handle file upload, message, and chat history, then stream the response."""
    try:
        chat_history = json.loads(history)
        
        contents = await file.read() if file else None
        
        if file and not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")

        async def stream_response():
            async for chunk in send_message(message, chat_history, contents):
                yield chunk.encode('utf-8')
        
        return StreamingResponse(
            stream_response(),
            media_type="text/plain"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)