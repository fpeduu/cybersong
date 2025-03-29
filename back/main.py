from fastapi import FastAPI
from routers import music, video

app = FastAPI()

# Incluindo os routers
app.include_router(music.router, prefix="/api")
app.include_router(video.router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Welcome to the CyberSong API"}
