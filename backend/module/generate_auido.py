import concurrent.futures as cf
import glob
import io
import os
import time
import json
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import List, Literal, Tuple
import google.generativeai as genai
from gtts import gTTS
from pydantic import BaseModel, ValidationError, Field
from pypdf import PdfReader
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential
from config.config import load_config

config=load_config()

genai.configure(api_key=config['api_keys'][1])

class DialogueItem(BaseModel):
    """Podcast diyalogu için bir konuşma öğesini temsil eder."""
    text: str
    speaker: Literal["female-1", "male-1", "female-2"] = Field(default="female-1")

    @property
    def voice(self) -> str:
        """Konuşmacının ses dilini döner."""
        return {
            "female-1": "tr",
            "male-1": "tr", 
            "female-2": "tr",
        }[self.speaker]

class Dialogue(BaseModel):
    """Podcast diyaloğunu temsil eden bir veri modeli."""
    scratchpad: str = ""
    dialogue: List[DialogueItem]

def clean_text(text: str) -> str:
    """Metni temizler, gereksiz boşlukları kaldırır."""
    if not text:
        return ""
    cleaned_text = ' '.join(text.split())
    return cleaned_text

def get_mp3(text: str, voice: str, max_chunk_length: int = 300) -> bytes:
    """Verilen metni ses dosyasına dönüştürür."""
    text = clean_text(text)
    
    text_chunks = [text[i:i+max_chunk_length] for i in range(0, len(text), max_chunk_length)]
    
    audio_chunks = []
    for chunk in text_chunks:
        with io.BytesIO() as file:
            tts = gTTS(text=chunk, lang=voice)
            tts.write_to_fp(file)
            file.seek(0)
            audio_chunks.append(file.getvalue())
    
    return b''.join(audio_chunks)

def extract_json_from_response(response_text: str) -> dict:
    """Yanıt metninden JSON verisini çıkarır."""
    start = response_text.find('{')
    end = response_text.rfind('}') + 1
    
    if start == -1 or end == 0:
        raise ValueError("JSON bulunamadı")
    
    json_str = response_text[start:end].replace("'", '"')
    
    # JSON parse et
    return json.loads(json_str)

def generate_dialogue(text: str) -> Dialogue:
    """
    Verilen metinden podcast diyaloğu oluşturur.
    
    Args:
        text (str): Podcast konusu metni
    
    Returns:
        Dialogue: Oluşturulan podcast diyaloğu
    """
    model = genai.GenerativeModel('gemini-pro')
    prompt = f"""
    Göreviniz, sağlanan metni podcast formatında diyaloga dönüştürmek.
    İçerik bilgilendirici, akıcı ve dinleyici için ilginç olmalı.

    Giriş metni:
    <input_text>{text}</input_text>

    Çok önemli: SADECE JSON formatında yanıt ver!
    Örnek JSON formatı:
    {{
        "scratchpad": "Podcast için konsept ve ana temalar",
        "dialogue": [
            {{"text": "İlk konuşmacının metni", "speaker": "female-1"}},
            {{"text": "İkinci konuşmacının yanıtı", "speaker": "male-1"}},
            {{"text": "Üçüncü konuşmacının yorumu", "speaker": "female-2"}}
        ]
    }}
    """
    
    try:
        while True:
            try:
                response = model.generate_content(prompt)
                dialogue_dict = extract_json_from_response(response.text)
                break
            except Exception as e:
                print(f"Yanıt oluşturma hatası: {e}")
        
        return Dialogue(**dialogue_dict)
    
    except Exception as e:
        print(f"Diyalog oluşturma hatası: {e}")
        return Dialogue(
            scratchpad="Otomatik içerik oluşturulamadı",
            dialogue=[DialogueItem(text="PDF içeriği analiz edilemedi.", speaker="female-1")]
        )

def generate_audio(file: str, max_audio_length: int = 3600) -> str:
    """
    PDF dosyasından ses dosyası oluşturur.
    
    Args:
        file (str): PDF dosya yolu
        max_audio_length (int): Maksimum ses dosyası uzunluğu (saniye)
    
    Returns:
        str: Oluşturulan ses dosyası yolu
    """
    try:
        with Path(file).open("rb") as f:
            reader = PdfReader(f)
            text = "\n\n".join([page.extract_text() for page in reader.pages])
            text = clean_text(text)

        llm_output = generate_dialogue(text)

        audio = b""
        transcript = ""

        with cf.ThreadPoolExecutor(max_workers=3) as executor:
            futures = []
            for line in llm_output.dialogue:
                transcript_line = f"{line.speaker}: {line.text}"
                future = executor.submit(get_mp3, line.text, line.voice)
                futures.append((future, transcript_line))

            for future, transcript_line in futures:
                audio_chunk = future.result()
                audio += audio_chunk
                transcript += transcript_line + "\n\n"

        temporary_directory = "/home/gozerutime/static/tmp/"
        os.makedirs(temporary_directory, exist_ok=True)

        audio_file_path = NamedTemporaryFile(
            dir=temporary_directory,
            delete=False,
            suffix=".mp3",
        )
        audio_file_path.write(audio)
        audio_file_path.close()

        for file in glob.glob(f"{temporary_directory}*.mp3"):
            if os.path.isfile(file) and time.time() - os.path.getmtime(file) > 24 * 60 * 60:
                os.remove(file)

        return temporary_directory + audio_file_path.name.split("\\")[-1]

    except Exception as e:
        print(f"Ses oluşturma hatası: {e}")
        return None

if __name__ == "__main__":
    test_pdf_path = "temp.pdf"  
    audio_file = generate_audio(test_pdf_path)
    print(f"Oluşturulan ses dosyası: {audio_file}")
