import { useLocation } from "react-router-dom";

function Video() {
  const location = useLocation();
  const videoUrl = location.state?.videoUrl;

  if (!videoUrl) {
    return <p>Erro: Vídeo não encontrado.</p>;
  }
  return (
    <div className="relative home flex flex-col justify-center items-center w-screen min-h-screen bg-[var(--color-primary)] text-white px-8 gap-8 !overflow-hidden">
      <div className="w-64 h-72 md:w-[432px] md:h-[466px] absolute bottom-[-1rem]  right-[-1rem] bg-contain bg-center bg-no-repeat bg-[url('/design-rt.svg')] overflow-hidden rotate-90"></div>
      <h1>Resultado em vídeo</h1>
      <video controls width="600">
        <source src={videoUrl} type="video/mp4" />
        Seu navegador não suporta o vídeo.
      </video>
    </div>
  );
}

export default Video;
