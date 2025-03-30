from fastapi import APIRouter
from typing import List
from IPython.display import Audio, display, HTML
from pydantic import BaseModel

from services.deezer import search_deezer, format_duration
from services.video_gen import pipeline

router = APIRouter()

class Song(BaseModel):
    id: int
    title: str
    artist: str
    album: str
    preview_url: str

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
            preview_url=song['preview']
        ) for song in found_songs
    ]
    
    return SearchResponse(results=songs)

@router.post("/select")
async def select_music(selected_song: Song):
    response = pipeline(
        title=selected_song.title,
        artist=selected_song.artist,
        album=selected_song.album,
        preview_url=selected_song.preview_url
    )

    if "error" not in response:
        return {"message": "Análise realizada com sucesso!", "data": response}
    return {"error": "Falha ao analisar a música."}




