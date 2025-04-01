from dotenv import load_dotenv
import os
import json
import random
from time import sleep
from unidecode import unidecode
from googleapiclient.discovery import build
from bs4 import BeautifulSoup
import requests

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_CSE_ID = os.getenv("GOOGLE_CSE_ID")
CACHE_FILE = "cache.json"
USER_AGENTS = os.getenv("USER_AGENTS").split(',')


def buscar_links_letras_mus_br(artista, musica):
    """Busca links e filtra por presença do nome do artista na URL"""
    try:
        service = build("customsearch", "v1", developerKey=GOOGLE_API_KEY)
        res = service.cse().list(
            q=f"{artista} {musica} letras site:letras.mus.br",
            cx=GOOGLE_CSE_ID,
            num=3  # Busca mais resultados para melhor filtragem
        ).execute()

        if 'items' not in res:
            return None

        # Pré-processa o nome do artista para comparação
        artista_slug = unidecode(artista).lower().replace(" ", "-")

        # Filtra links que contenham o nome do artista
        links_filtrados = []
        for item in res['items']:
            link = item['link']
            if (artista.lower() in link.lower()) or (artista_slug in link.lower()):
                links_filtrados.append(link)


        return links_filtrados

    except Exception as e:
        print(f"Erro na Google Search API: {str(e)}")
        return None
    

def extrair_letras_letrasmusbr(url):
    headers = {
        'User-Agent': random.choice(USER_AGENTS),
        'Accept-Language': 'pt-BR,pt;q=0.9'
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)

        # Verifique se a resposta é bem-sucedida
        if response.status_code != 200:
            print(f"Erro ao acessar {url}. Status Code: {response.status_code}")
            return None
        
        soup = BeautifulSoup(response.text, 'html.parser')

        # Contêiner principal com fallback
        container = soup.find('div', class_='lyric-original') or \
                   soup.find('div', class_='cnt-letra')

        if not container:
            print(f"Não foi possível encontrar o container de letra em {url}")
            return None

        # Processamento que preserva a estrutura original
        letras = []
        for elemento in container.children:
            if elemento.name == 'p':
                # Extrai texto mantendo quebras internas
                texto = ''
                for content in elemento.contents:
                    if content.name == 'br':
                        texto += '\n'
                    elif isinstance(content, str):
                        texto += content.strip()
                letras.append(texto.strip())
                letras.append('')
            elif isinstance(elemento, str):
                texto = elemento.strip()
                if texto:
                    letras.append(texto)
            elif elemento.name == 'br':
                letras.append('')  # Mantém quebras explícitas

        # Junta tudo preservando linhas individuais
        letra_completa = '\n'.join(
            linha.replace('"', '').rstrip()
            for linha in letras
        )

        # Se a letra estiver vazia ou não for bem extraída, retorna None
        if not letra_completa.strip():
            print(f"Letra extraída vazia de {url}")
            return None

        return letra_completa

    except Exception as e:
        print(f"Erro na extração: {str(e)}")
        return None


def buscar_lyrics_ovh(artista, musica):
    """Fallback usando API pública"""
    try:
        headers = {'User-Agent': random.choice(USER_AGENTS)}
        url = f"https://api.lyrics.ovh/v1/{artista}/{musica}"
        response = requests.get(url, headers=headers, timeout=5)

        if response.status_code == 200:
            data = response.json()
            if data.get('lyrics'):
                letras = []
                contador = 0
                intervalo = random.choice([4, 5])  # Define o primeiro intervalo aleatoriamente
                # Gerando quebras de linhas para a letra
                for linha in [l for l in data['lyrics'].split('\n') if l.strip()]:
                    letras.append(linha)
                    contador += 1
                    if contador == intervalo:
                        letras.append("\n")
                        contador = 0  #
                        intervalo = random.choice([4, 5])
                        print(letras)
                letra_completa = ''.join(letras) if "\n\n" in letras else '\n'.join(letras)
                return letra_completa

        print(f"Lyrics.ovh: {response.status_code}")
        return None
    except Exception as e:
        print(f"Erro no lyrics.ovh: {str(e)}")
        return None
    
def salvar_letra_txt(artista, musica, conteudo):
    """Salva a letra formatada em arquivo TXT"""
    nome_arquivo = f"{artista} - {musica}.txt".replace('/', '_')

    # Garante que o conteúdo seja string
    if isinstance(conteudo, list):
        conteudo = '\n'.join(conteudo)
    elif not isinstance(conteudo, str):
        conteudo = str(conteudo)

    with open(nome_arquivo, 'w', encoding='utf-8') as f:
        f.write(conteudo)

    print(f"✓ Letra salva em: {nome_arquivo}")
    return nome_arquivo

def obter_e_salvar_letras(artista, musica):
    """Fluxo completo com salvamento automático"""
    print(f"\n🔍 Buscando: {artista} - {musica}")

    # Busca via Google CSE
    print("⏳ Buscando no letras.mus.br...")
    links = buscar_links_letras_mus_br(artista, musica)
    letra = None

    if links:
        for url in links:
            print(f"🔗 Tentando: {url}")
            letra = extrair_letras_letrasmusbr(url)
            if letra:
                print("✅ Letra encontrada no letras.mus.br")
                break
            sleep(random.uniform(1, 3))

    # Fallback para lyrics.ovh
    if not letra:
        print("⏳ Tentando lyrics.ovh...")
        letra = buscar_lyrics_ovh(artista, musica)
        if letra:
            print("✅ Letra encontrada via lyrics.ovh")

    if letra:
        salvar_letra_txt(artista, musica, letra)
        return letra
    else:
        print("❌ Nenhuma fonte retornou resultados")
        return None