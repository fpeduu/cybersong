import httpx
from fastapi import HTTPException
import requests

def format_duration(seconds):
    """Converte segundos para MM:SS"""
    minutes, seconds = divmod(seconds, 60)
    return f"{minutes:02d}:{seconds:02d}"

async def search_deezer(track_name, artist_name):
    # Buscar as 10 primeiras músicas no Deezer
    search_url = "https://api.deezer.com/search"
    params = {
        'q': f'track:"{track_name}" artist:"{artist_name}"',
        'limit': 5  # Agora buscando 5 resultados
    }
    
    # Usando httpx.AsyncClient() para fazer a requisição de forma assíncrona
    async with httpx.AsyncClient() as client:
        response = await client.get(search_url, params=params)
        data = response.json()

    if data.get('data'):
        return data['data']
    else:
        return None
