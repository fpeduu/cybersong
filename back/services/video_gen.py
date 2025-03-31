import httpx
from fastapi import HTTPException
import requests
import librosa
import numpy as np
import os
import yt_dlp
import re
from .lyrics import obter_e_salvar_letras
from .images import images_generator
from moviepy import ImageClip, concatenate_videoclips, AudioFileClip, CompositeVideoClip, ImageSequenceClip


def pipeline(title, artist, album, preview_url, duration):
    print(f"\n🎵 Música Escolhida:")
    print(f"   Música: {title}")
    print(f"   Artista: {artist}")
    print(f"   Álbum: {album}")
    print(f"   Preview URL: {preview_url}")

    # Análise Librosa
    print("\n   🔬 Analisando preview técnico...")
    features, y, sr = audio_analysis(preview_url)

    if features:
        # Exibe features
        print("\n   📊 Análise Técnica:")
        print(f"      • 🎵 BPM: {features['bpm']}")
        print(f"      • ⚡ Energia: {features['energy']:.3f} (0-1)")
        print(f"      • 🕺 Dançabilidade: {features['danceability']:.3f} Hz")
        print(f"      • 🎶 Tom: {features['tone']:.2f} semitons")

        # Obter Letra
        print("\n   📝 Buscando a letra...")
        lyrics = obter_e_salvar_letras(artist, title)
        # print(f"\n   📝 Letra: {lyrics}")

        print("\n   🎨 Gerando imagens...")
        images = images_generator(lyrics, features)
        
        print("\n   🚀 Baixando o arquivo MP3...")
        audio_info = yt_download(title, artist, album, target_duration=duration)
        if audio_info:
            print("Audio info:", audio_info)
            # Gerar vídeo sincronizado
            try:
                audio_path = audio_info['path']
 
                audio = AudioFileClip(audio_path)
                print("Duração do áudio:", audio.duration)
                total_duration = audio.duration

            except KeyError:
                print(f"Erro ao carregar o áudio: {audio_path} pode estar corrompido ou inválido.")

            # Calcular a duração de cada verso (assumindo 4 imagens por parágrafo)
            verse_duration = total_duration / len(images)

            # Criar colagem para cada conjunto de imagens e sincronizar com a música
            collages = [create_collage(image_group, verse_duration) for image_group in images]
            sync_with_audio(collages, audio_path)

            return {
                "title": title,
                "artist": artist,
                "album": album,
                "bpm": features['bpm'],
                "energy": features['energy'],
                "danceability": features['danceability'],
                "tone": features['tone'],
                "images": images,
                "audio_path": audio_path
            }

    return {"error": "Falha ao analisar a música."}


def audio_analysis(preview_url):
    try:
        # Baixa o preview
        audio_data = requests.get(preview_url).content
        with open("temp_preview.mp3", 'wb') as f:
            f.write(audio_data)

        # Processamento com Librosa
        y, sr = librosa.load("temp_preview.mp3", duration=30)

        # Extração de features (corrigido o warning do BPM)
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
        features = {
            "bpm": int(np.mean(tempo)) if isinstance(tempo, np.ndarray) else int(tempo),
            "energy": float(np.mean(librosa.feature.rms(y=y))),
            "danceability": float(np.mean(librosa.feature.spectral_centroid(y=y))),
            "tone": float(librosa.estimate_tuning(y=y, sr=sr)),
        }
        return features, y, sr

    except Exception as e:
        print(f"⚠️ Erro na análise: {str(e)}")
        return None, None, None
    

import re
import yt_dlp

def yt_download(title, artist, album, target_duration, tolerance=15):

    # Pré-processamento da query
    query = f"{title} {artist} {album}".strip()
    safe_filename = re.sub(r'[\\/*?:"<>|]', "", title)[:50].strip()

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': f"{safe_filename}.%(ext)s",
        'quiet': False,  # Mostra logs para debug
        'match_filter': lambda info: (
            None if abs(info['duration'] - target_duration) <= tolerance
            else f"Duração {info['duration']}s fora do limite"
        ),
        'socket_timeout': 30,
        'retries': 3
    }

    try:
        print(f"\n🔍 Buscando: '{query}' (Duração alvo: {target_duration}s ±{tolerance}s)")

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Buscar vídeos
            info = ydl.extract_info(f"ytsearch5:{query}", download=False)

            if not info.get('entries'):
                print("❌ Nenhum resultado encontrado")
                return None

            # Filtrar vídeos por duração
            videos_validos = [
                e for e in info['entries']
                if abs(e['duration'] - target_duration) <= tolerance
            ]

            if not videos_validos:
                print("⚠️ Vídeos encontrados, mas fora da tolerância:")
                for vid in info['entries'][:3]:
                    print(f" - {vid['title']} ({vid['duration']}s)")
                return None

            # Melhor match
            video = min(videos_validos, key=lambda x: abs(x['duration'] - target_duration))
            print(f"✅ Vídeo adequado encontrado: {video['title']} ({video['duration']}s)")

            # Download do áudio diretamente
            ydl.download([video['webpage_url']])

            return {
                'path': f"{safe_filename}.mp3",
                'duration': video['duration'],
                'title': video['title'],
                'url': video['webpage_url']
            }

    except Exception as e:
        print(f"⚠️ Erro crítico: {str(e)}")
        return None

    
# def create_collage(image_group, verse_duration):
#     print(f"🖼️ Criando colagem para {len(image_group)} imagens")
#     print(image_group)
#     image_clips = [ImageSequenceClip([img], durations=[verse_duration]) for img in image_group]
#     # No lugar de tentar criar um ImageSequenceClip com outros clips, apenas concatenar
#     return concatenate_videoclips(image_clips, method="compose")
def create_collage(image_group, verse_duration):
    print(f"🖼️ Criando colagem para {len(image_group)} imagens")
    print(image_group)

    # Calcular a duração de cada imagem como metade do tempo do verso
    image_clip_duration = verse_duration / len(image_group)
    
    # Criar os clipes das imagens, cada uma com a duração calculada
    image_clips = [ImageClip(img).with_duration(image_clip_duration) for img in image_group]
    
    # Concatenar as imagens em um único vídeo
    return concatenate_videoclips(image_clips, method="compose")

# Função para sincronizar o vídeo com o áudio
def sync_with_audio(collages, audio_path):
    try:
        # Tentar abrir o arquivo m4a diretamente
        audio = AudioFileClip(audio_path)
    except Exception as e:
        print(f"Erro ao carregar webm: {e}, tentando converter para mp3.")
        # Converter o áudio se der problema
        audio_path = convert_audio(audio_path)
        audio = AudioFileClip(audio_path)

    video_clips = []
    start_time = 0
    for collage in collages:
        collage = collage.with_start(start_time)
        video_clips.append(collage)
        start_time += collage.duration

    final_video = concatenate_videoclips(video_clips)
    final_video = final_video.with_audio(audio)
    final_video.write_videofile("output_video.mp4", codec="libx264", audio_codec="aac", fps=24)


def convert_audio(input_path):
    output_path = input_path.replace(".webm", ".mp3")
    if not os.path.exists(output_path):
        audio = AudioFileClip(input_path)
        audio.write_audiofile(output_path)
    return output_path