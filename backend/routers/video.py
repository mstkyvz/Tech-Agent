from fastapi import APIRouter, HTTPException
from schemas.video_schemas import VideoCreate, VideoStatus
from services.video_service import create_video_task, video_database
import os
from datetime import datetime
import asyncio

router = APIRouter()

@router.post("/create_video")
async def create_video(video_data: VideoCreate):
    video_id = video_data.id
    video_path = f"/static/videomedia/videos/1080p60/{video_id}.mp4"
    
    if os.path.exists("../frontend/build" + video_path):
        if video_id not in video_database:
            video_database[video_id] = {
                "status": "completed",
                "video_url": video_path,
                "created_at": datetime.now()
            }
        return VideoStatus(status=video_database[video_id]["status"])
    
    if video_id in video_database:
        return VideoStatus(status=video_database[video_id]["status"])
    
    video_database[video_id] = {"status": "queued"}
    asyncio.create_task(create_video_task(video_id))
    
    return VideoStatus(status="queued")

@router.get("/check_video/{video_id}")
async def check_video(video_id: str):
    if video_id not in video_database:
        return VideoStatus(status="not_found")
    
    video_info = video_database[video_id]
    return VideoStatus(
        status=video_info["status"],
        video_url=video_info.get("video_url")
    )

@router.delete("/delete_video/{video_id}")
async def delete_video(video_id: str):
    if video_id not in video_database:
        raise HTTPException(status_code=404, detail="Video not found")
    
    del video_database[video_id]
    return {"message": "Video deleted successfully"}