
from typing import List, Optional, Dict, Any
import json
import hashlib
from datetime import datetime

def calculate_chat_hash(messages: List[Dict]) -> str:
    hash_content = []
    for msg in messages:
        hash_content.append({
            'type': msg['type'],
            'content': msg['content']
        })
    
    message_str = json.dumps(hash_content, sort_keys=True)
    return hashlib.sha256(message_str.encode()).hexdigest()


def clean_text(text: str) -> str:
    if not text:
        return ""

    cleaned_text = ' '.join(text.split())
    return cleaned_text