import asyncio
import os
import threading
import queue
from datetime import datetime
from module import create_videos

video_database = {}
video_queue = queue.Queue()
video_threads = {}
MAX_CONCURRENT_VIDEOS = 3

def video_worker():
    """Worker function that processes videos from the queue"""
    while True:
        try:
            video_id = video_queue.get()
            if video_id is None:  
                break
                
            try:
                
                video_database[video_id]["status"] = "processing"
                
                
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(create_videos.run(video_id))
                loop.close()
                
                video_path = f"/static/videomedia/videos/1080p60/{video_id}.mp4"
                video_database[video_id].update({
                    "status": "completed",
                    "video_url": video_path,
                    "created_at": datetime.now()
                })
            except Exception as e:
                print(f"Error processing video {video_id}: {str(e)}")
                video_database[video_id].update({
                    "status": "error",
                    "error": str(e),
                    "created_at": datetime.now()
                })
            finally:
                video_queue.task_done()
                if video_id in video_threads:
                    del video_threads[video_id]
                
        except Exception as e:
            print(f"Worker thread error: {str(e)}")
            continue
        
        
async def create_video_task(video_id: str):
    try:
        video_path = f"/static/videomedia/videos/1080p60/{video_id}.mp4"
        if os.path.exists("../frontend/build" + video_path):
            if video_id not in video_database:
                video_database[video_id] = {
                    "status": "completed",
                    "video_url": video_path,
                    "created_at": datetime.now()
                }
            return

        if video_id not in video_threads:
            video_threads[video_id] = threading.current_thread()
            video_queue.put(video_id)
            
    except Exception as e:
        print(f"Error queuing video {video_id}: {str(e)}")
        video_database[video_id] = {
            "status": "error",
            "error": str(e),
            "created_at": datetime.now()
        }