import os
import google.generativeai as genai
from PIL import Image
import io


def generate_response(user_message):
    api_key = "AIzaSyAy3E3BYjXjS6fyrRUbS2m8ip3Sdb3hmqA"
    model_name = "gemini-1.5-pro"
    genai.configure(api_key=api_key)
    generation_config = {
            "temperature": 0.3,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 8192,
            "response_mime_type": "text/plain",
        }

    model = genai.GenerativeModel(
        model_name=model_name,
        generation_config=generation_config,
    )

    chat_session = model.start_chat(
        history=[]
    )

    response = chat_session.send_message(user_message)

    return response.text



def generate_response_with_image(user_message, image):
    try:

        pil_image = image
        api_key = "AIzaSyAy3E3BYjXjS6fyrRUbS2m8ip3Sdb3hmqA"
        if not api_key:
            return "API anahtarı bulunamadı!"
            
        model_name = "gemini-1.5-pro"
        genai.configure(api_key=api_key)
        
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
        
        response = chat.send_message([user_message, pil_image])
        return response.text
        
    except Exception as e:
        return f"Hata oluştu: {str(e)}\nHata türü: {type(e)}"
    
    


