from fastapi import APIRouter
from typing import List
from IPython.display import Audio, display, HTML
from pydantic import BaseModel

from services.deezer import search_deezer, format_duration

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

# @router.get("/search")
# async def search_music(title: str, artist: str) -> List[str]:
#     found_songs = await search_deezer(title, artist)
#     print(found_songs)
#     if found_songs is None or len(found_songs) == 0:
#         return {"error": "Nenhum resultado encontrado no Deezer."}
#     # if found_songs:
#     #     print(f"🔍 Top 10 resultados para '{title}' de {artist}:\n")
#     # for i, track in enumerate(found_songs, 1):
#     #     print(f"🎵 {i}. Música: {track['title']}")
#     #     print(f"   🎤 Artista: {track['artist']['name']}")
#     #     print(f"   💿 Álbum: {track['album']['title']}")
#     #     print(f"   ⏱️ Duração: {format_duration(track['duration'])}")

#     #     if track.get('preview'):
#     #         print("   🔊 Preview:")
#     #         display(Audio(url=track['preview'], autoplay=False))
#     #     else:
#     #         print("   ❌ Preview não disponível")
#     # else:
#     #     print("Nenhum resultado encontrado no Deezer.")
#     return found_songs
