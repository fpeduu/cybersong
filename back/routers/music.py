from fastapi import APIRouter
from typing import List

router = APIRouter()

@router.get("/search")
async def search_music(artist: str, title: str) -> List[str]:
    found_songs = [
        f"{title} - {artist} (Preview 1)",
        f"{title} - {artist} (Preview 2)",
        f"{title} - {artist} (Preview 3)"
    ]
    return found_songs
