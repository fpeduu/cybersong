import httpx
from fastapi import HTTPException
import requests
import librosa
import numpy as np
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
            # Gerar vídeo sincronizado
            audio_path = audio_info['path']
            audio = AudioFileClip(audio_path)
            total_duration = audio.duration

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
            # Primeiro verifica se existe
            info = ydl.extract_info(f"ytsearch5:{query}", download=False)

            if not info.get('entries'):
                print("❌ Nenhum resultado encontrado")
                return None

            # Filtra por duração
            videos_validos = [
                e for e in info['entries']
                if abs(e['duration'] - target_duration) <= tolerance
            ]

            if not videos_validos:
                print("⚠️ Vídeos encontrados, mas fora da tolerância:")
                for vid in info['entries'][:3]:
                    print(f" - {vid['title']} ({vid['duration']}s)")
                return None

            # Seleciona o melhor match
            video = min(videos_validos, key=lambda x: abs(x['duration'] - target_duration))
            print(f"✅ Vídeo adequado encontrado: {video['title']} ({video['duration']}s)")

            # Download real
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
    
def create_collage(image_group, verse_duration):
    image_clips = [ImageSequenceClip([img], durations=[verse_duration]) for img in image_group]
    return ImageSequenceClip(image_clips, durations=[verse_duration] * len(image_group))

# Função para sincronizar o vídeo com o áudio
def sync_with_audio(collages, audio_path):
    audio = AudioFileClip(audio_path)
    video_clips = []

    start_time = 0
    for collage in collages:
        collage = collage.set_start(start_time)
        video_clips.append(collage)
        start_time += collage.duration

    final_video = concatenate_videoclips(video_clips)
    final_audio = AudioFileClip(audio_path)
    final_video = final_video.set_audio(final_audio)
    final_video.write_videofile("output_video.mp4", codec="libx264", audio_codec="aac")
