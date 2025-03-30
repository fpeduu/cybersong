from dotenv import load_dotenv
import os
import requests
from openai import OpenAI
from moviepy import ImageClip, concatenate_videoclips, AudioFileClip, CompositeVideoClip

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def download_image(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, 'wb') as file:
            file.write(response.content)
        print(f"Imagem baixada: {filename}")
        return filename
    else:
        print(f"Erro ao baixar imagem: {url}")
        return None

def images_generator(lyrics, features):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    images = []
    
    for verse in lyrics.split("\n\n"):  # Supondo que cada verso está separado por uma quebra de linha
        verse_images = []  # Lista para armazenar as 4 imagens do verso
        print(f"Gerando imagens para o verso: {verse}")
        for _ in range(2):  # Loop para gerar 4 imagens para cada verso
            response = client.images.generate(
                model="dall-e-3",
                prompt=f"Uma imagem baseada no verso da música: '{verse}'. Características: BPM: {features['bpm']}, Energia: {features['energy']}, Dançabilidade: {features['danceability']}, Tom: {features['tone']}",
                n=1,  # Apenas 1 imagem por chamada
                size="1024x1024"
            )
            # Extrai a URL da imagem gerada
            image_url = response.data[0].url  # Corrigido para acessar corretamente
            verse_images.append(image_url)  # Adiciona a URL da imagem gerada
        
        images.append(verse_images)  # Adiciona as 4 imagens do verso na lista principal

    return images


