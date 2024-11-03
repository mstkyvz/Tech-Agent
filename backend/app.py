from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from database.database import engine
from models import models
from routers import chat, history, video, audio
from config.config import load_config
from services.video_service import initialize_workers

# Initialize database
models.Base.metadata.create_all(bind=engine)

# Initialize app
app = FastAPI()
config = load_config()

# Static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router, prefix="/api", tags=["chat"])
app.include_router(history.router, prefix="/api", tags=["history"])
app.include_router(video.router, prefix="/api", tags=["video"])
app.include_router(audio.router, prefix="/api", tags=["audio"])

initialize_workers()

@app.on_event("shutdown")
async def shutdown_event():
    from services.video_service import shutdown_workers
    await shutdown_workers()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)