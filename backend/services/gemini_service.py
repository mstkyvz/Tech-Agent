import google.generativeai as genai
from typing import List, Optional, AsyncIterable
import asyncio
from config.config import load_config
from utils.prompt_builder import build_prompt

config = load_config()
genai.configure(api_key=config['api_keys'][0])
model = genai.GenerativeModel('gemini-1.5-pro')

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

def process_gemini_response(response):
    try:
        for chunk in response:
            if hasattr(chunk, 'text'):
                yield chunk.text
            elif isinstance(chunk, str):
                yield chunk
    except Exception as e:
        yield f"Error processing response: {str(e)}"

async def send_message(
    message: str,
    history: List[dict],
    image_data: Optional[bytes] = None,
    types: str = "question",
    extra: Optional[str] = None
) -> AsyncIterable[str]:
    try:
        content = build_prompt(message, history, types, extra)

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