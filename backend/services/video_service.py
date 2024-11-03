import threading
from datetime import datetime
from typing import Dict, List
import asyncio
from module.videos_manager import *

worker_threads: List[threading.Thread] = []

def initialize_workers():
    for _ in range(MAX_CONCURRENT_VIDEOS):
        t = threading.Thread(target=video_worker, daemon=True)
        t.start()
        worker_threads.append(t)

async def shutdown_workers():
    for _ in worker_threads:
        video_queue.put(None)
    
    for t in worker_threads:
        t.join()
