from typing import List, Dict, Any, Optional
from langchain_community.tools import DuckDuckGoSearchRun
from utils import prompt

search = DuckDuckGoSearchRun()

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