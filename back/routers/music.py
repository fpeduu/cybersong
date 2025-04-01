from fastapi import APIRouter
from typing import List
from IPython.display import Audio, display, HTML
from pydantic import BaseModel
from fastapi.responses import JSONResponse, FileResponse

from services.deezer import search_deezer, format_duration
from services.video_gen import pipeline

router = APIRouter()

class Song(BaseModel):
    id: int
    title: str
    artist: str
    album: str
    preview_url: str
    duration: int

class SearchResponse(BaseModel):
    results: List[Song]

@router.get("/search")
async def search_music(artist: str, title: str):
    found_songs = await search_deezer(title, artist)
    
    if found_songs is None or len(found_songs) == 0:
        return {"error": "Nenhum resultado encontrado no Deezer."}
    
    songs = [
        Song(
            id=song['id'],
            title=song['title'],
            artist=song['artist']['name'],
            album=song['album']['title'],
            preview_url=song['preview'],
            duration=song['duration']
        ) for song in found_songs
    ]
    
    return SearchResponse(results=songs)

@router.post("/select")
async def select_music(selected_song: Song):
    video_path = pipeline(
        title=selected_song.title,
        artist=selected_song.artist,
        album=selected_song.album,
        preview_url=selected_song.preview_url,
        duration=selected_song.duration
    )

    if isinstance(video_path, dict) and "error" in video_path:
        return JSONResponse(content=video_path, status_code=400)

    # Retorna o vídeo diretamente
    return FileResponse(video_path, media_type="video/mp4", filename="output_video.mp4")




