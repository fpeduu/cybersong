from fastapi import FastAPI
from routers import music, video
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

# Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # URL do frontend React
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos HTTP
    allow_headers=["*"],  # Permite todos os cabeçalhos
)

# Incluindo os routers
app.include_router(music.router, prefix="/api")
app.include_router(video.router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Welcome to the CyberSong API"}

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000)
