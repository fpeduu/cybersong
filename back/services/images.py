from dotenv import load_dotenv
import os
import requests
from openai import OpenAI, ChatCompletion
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

def images_generator(lyrics, features_descriptions, theme):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    images = []
    
    bpm_description, energy_description, danceability_description = features_descriptions

    for verse in lyrics.split("\n\n"):  # Supondo que cada verso está separado por uma quebra de linha
        verse_images = []  # Lista para armazenar as 4 imagens do verso
        print(f"Gerando imagens para o verso: {verse}")
        for _ in range(2):  # Loop para gerar 4 imagens para cada verso
            response = client.images.generate(
                model="dall-e-3",
                prompt = gerar_prompt(verse, bpm_description, energy_description, danceability_description, theme),
                n=1,  # Apenas 1 imagem por chamada
                size="1024x1024"
            )
            # Extrai a URL da imagem gerada
            image_url = response.data[0].url  # Corrigido para acessar corretamente
            verse_images.append(image_url)  # Adiciona a URL da imagem gerada
        
        images.append(verse_images)  # Adiciona as 4 imagens do verso na lista principal

    return images


def gerar_prompt(verse, bpm_level, energy_level, danceability_level, theme):
    client = OpenAI()  # Cria o cliente corretamente na versão nova da API
    
    system_message = "Você é um assistente que cria prompts para gerar imagens no DALL-E sem incluir texto na imagem."

    user_message = f"""
    Gere um prompt detalhado para uma imagem no DALL-E baseada em uma música. A imagem deve refletir a energia ({energy_level}), a dançabilidade ({danceability_level}) e a velocidade ({bpm_level}) da música. 
    O estilo deve ser {theme}, com elementos visuais que combinem com essa estética e transmitam uma sensação de movimento.
    
    **Importante: A imagem NÃO pode conter texto, letras, números ou qualquer tipo de símbolo escrito.**
    
    O significado do verso da música é: {verse}. Use isso para inspirar o cenário da imagem, mas sem incluir palavras na ilustração.
    """
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ],
        temperature=0.7
    )
    prompt_text = response.choices[0].message.content.strip()
    # print(f"Prompt gerado: {prompt_text}")
    return prompt_text