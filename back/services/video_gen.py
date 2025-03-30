import httpx
from fastapi import HTTPException
import requests
import librosa
import numpy as np

def pipeline(title, artist, album, preview_url):
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

        # Aqui você pode gerar as imagens com OpenAI ou fazer outro processamento
        images = generate_images_from_features(features)

        return {
            "title": title,
            "artist": artist,
            "album": album,
            "bpm": features['bpm'],
            "energy": features['energy'],
            "danceability": features['danceability'],
            "tone": features['tone'],
            "images": images
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
    

def generate_images_from_features(features):
    # Aqui você colocaria a lógica para gerar as imagens
    return ["image1.png", "image2.png", "image3.png"]