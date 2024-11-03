from fastapi import APIRouter, UploadFile, File
from fastapi.responses import FileResponse
from services.audio_service import generate_audio

router = APIRouter()

@router.post("/upload-pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    with open("temp.pdf", "wb") as buffer:
        buffer.write(await file.read())
    
    audio_file_path = generate_audio("temp.pdf")
    return {"audio_file": audio_file_path}

@router.get("/audio/{filename}")
async def get_audio(filename: str):
    return FileResponse(f"/home/gozerutime/static/tmp/{filename}", media_type="audio/mpeg")