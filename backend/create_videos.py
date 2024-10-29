import sqlite3
import json
import base64
from PIL import Image
from io import BytesIO
from typing import Tuple, List, Dict
from pathlib import Path
from contextlib import contextmanager
import generate_response
import prompt
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService
from manim import *
import importlib.util
import sys

class ChatDatabase:
    def __init__(self, db_path: str = 'chat_history.db'):
        self.db_path = Path(db_path)
    
    @contextmanager
    def connect(self):
        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            yield conn
        finally:
            if conn:
                conn.close()
    
    def get_tables(self) -> List[str]:
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            return [table[0] for table in cursor.fetchall()]

    def get_chat_history(self, chat_id: int) -> Dict:
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT messages FROM chat_histories WHERE id = ?", 
                (chat_id,)
            )
            result = cursor.fetchone()
            
            if not result:
                raise ValueError(f"Chat ID {chat_id} bulunamadı")
                
            return json.loads(result[0])

class MessageProcessor:
    @staticmethod
    def decode_image(base64_str: str) -> Image.Image:
        try:
            if ',' in base64_str:
                base64_str = base64_str.split(',')[1]
            
            image_data = base64.b64decode(base64_str)
            return Image.open(BytesIO(image_data))
        except Exception as e:
            print(f"Görüntü decode hatası: {e}")
            raise

    def process_messages(self, messages: List[Dict]) -> Tuple[str, List[Image.Image]]:
        text_messages = []
        images = []
        
        for message in messages:
            text_messages.append(f"{message['type']}: {message['content']}")
            
            if 'image' in message and message['image']:
                try:
                    image = self.decode_image(message['image'])
                    images.append(image)
                except Exception as e:
                    print(f"Görüntü işleme hatası: {e}")
        
        return '\n'.join(text_messages), images

def save_and_run_manim_code(manim_code: str):
    with open("manicode.py", "w", encoding="utf-8") as f:
        f.write(manim_code)
    
    if "manicode" in sys.modules:
        del sys.modules["manicode"]
    
    try:
        spec = importlib.util.spec_from_file_location("manicode", "manicode.py")
        if spec is None:
            raise ImportError("Module spec not found")
        
        module = importlib.util.module_from_spec(spec)
        if spec.loader is None:
            raise ImportError("Module loader not found")
            
        sys.modules["manicode"] = module
        spec.loader.exec_module(module)
        
        if hasattr(module, 'Solution'):
            s = module.Solution()
            s.render()
    except Exception as e:
        print(f"Modül yükleme hatası: {e}")
        raise

async def run(chat_id):
    print("id: ", chat_id, flush=False)
    chat_id = str(chat_id)
    try:
        db = ChatDatabase()
        processor = MessageProcessor()
        tables = db.get_tables()
        chat_messages = db.get_chat_history(chat_id)
        messages, images = processor.process_messages(chat_messages)
        prompt_manim = prompt.manim_prompt.format(messages)
        
        response = generate_response.generate_response_with_image(prompt_manim, images[0] if images else None)
        print(messages)
        config.media_dir="../frontend/public/media"
        config.output_file = f"{chat_id}"
        config.background_color = "#e0e6e2" 
        Tex.set_default(color=BLACK)
        Text.set_default(color=BLACK)
        Mobject.set_default(color=RED)
        Dot.set_default(color=BLACK)
        VMobject.set_default(color=BLACK, stroke_width=4)
        Square.set_default(color=GREEN)
        for _ in range(10):
            try:
                manim_code = response.split("```python\n")[1].split("```")[0]
                save_and_run_manim_code(manim_code)
                break
            except Exception as e:
                response = generate_response.generate_response_with_image(prompt_manim, images[0] if images else None)
                print("-----" * 30)
                print(e)

    except Exception as e:
        print(f"Program hatası: {e}")
        raise
