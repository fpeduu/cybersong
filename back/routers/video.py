from fastapi import APIRouter

router = APIRouter()

@router.post("/generate-video")
async def generate_video(selected_song: str):
    # Aqui você colocaria a lógica para gerar o vídeo
    return {"message": f"Video generated for: {selected_song}"}
