import os
import google.generativeai as genai
from typing import Optional
from PIL import Image
import io
from config.config import load_config

config=load_config()

def generate_response_with_image(user_message: str, image: Optional[Image.Image] = None) -> str:
    """
    Kullanıcı mesajı ve isteğe bağlı bir görüntü ile yanıt oluşturur.
    
    Args:
        user_message (str): Kullanıcının mesajı.
        image (Optional[Image.Image]): İsteğe bağlı görüntü.

    Returns:
        str: Yanıt metni veya hata mesajı.
    """
    try:
        model_name = "gemini-1.5-pro"
        genai.configure(api_key=config['api_keys'][2])
        
        generation_config = {
            "temperature": 0.8,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 8192,
        }
        
        model = genai.GenerativeModel(
            model_name=model_name,
            generation_config=generation_config,
        )
        
        chat = model.start_chat(history=[])
        if image:
            response = chat.send_message([user_message, image])
        else:
            response = chat.send_message([user_message])
        
        return response.text
        
    except Exception as e:
        return f"Hata oluştu: {str(e)}\nHata türü: {type(e)}"
