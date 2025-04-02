import { Button } from "@/components/ui/button";
import { sendSelectedMusic, Song } from "@/services/musicService";
import { useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { Loader2 } from "lucide-react";

function SongList() {
  const location = useLocation();
  const { songs } = location.state || { songs: [] };
  //   const { data, loading, error } = useQuery(GET_SONGS);

  //   if (loading) return <p>Loading...</p>;
  //   if (error) return <p>Error :(</p>;
  const navigate = useNavigate();

  const [currentSong, setCurrentSong] = useState<number | null>(null);
  const [audio, setAudio] = useState<HTMLAudioElement | null>(null);
  const [selectedSong, setSelectedSong] = useState<Song | null>(null); // Estado para a música selecionada
  const [loading, setLoading] = useState(false);

  const handleSelectSong = (song: Song) => {
    setSelectedSong(song); // Atualiza a música selecionada
  };

  const playPreview = (songId: number, previewUrl: string) => {
    // Se já houver um áudio tocando, pausa e reinicia a música
    if (audio) {
      audio.pause();
      setCurrentSong(null);
    }

    // Cria um novo elemento de áudio com o preview
    const newAudio = new Audio(previewUrl);
    setAudio(newAudio);
    setCurrentSong(songId);

    newAudio.play();

    // Pausa o áudio após 5 segundos
    setTimeout(() => {
      newAudio.pause();
      setCurrentSong(null);
    }, 5000); // Toca por 5 segundos
  };

  const handleContinue = async () => {
    if (selectedSong) {
      try {
        setLoading(true); // Inicia o carregamento
        const url = await sendSelectedMusic(selectedSong);
        navigate("/video-result", { state: { videoUrl: url } });
      } catch (error) {
        console.error("Erro ao enviar música:", error);
      } finally {
        setLoading(false); // Finaliza o carregamento
      }
    } else {
      alert("Selecione uma música para continuar");
    }
  };

  return (
    <div className="relative home flex flex-col justify-center items-center w-screen min-h-screen bg-[var(--color-primary)] text-white px-8 gap-8 !overflow-hidden">
      <div className="w-64 h-72 md:w-[432px] md:h-[466px] absolute bottom-[-1rem]  right-[-1rem] bg-contain bg-center bg-no-repeat bg-[url('/design-rt.svg')] overflow-hidden rotate-90"></div>{" "}
      <div className="flex items-center justify-center  text-white z-10">
        <div className="w-full max-w-6xl lg:min-w-[780px] p-6  rounded-lg shadow-lg">
          <h2 className="text-lg  mb-4">Músicas Encontradas</h2>
          <ul className="space-y-4">
            {songs.map((song: Song) => (
              <li
                key={song.id}
                className={`flex justify-between w-full items-center mb-0 py-3 border-t divide-solid cursor-pointer ${
                  selectedSong?.id === song.id ? "text-[#497289]" : ""
                }`} // Adiciona destaque na música selecionada
                onClick={() => handleSelectSong(song)}
              >
                <div className="flex items-center gap-2">
                  <p className="font-medium">{song.title} </p>
                  <p className="font-medium">|</p>
                  <p className="font-medium">{song.artist}</p>
                  {/* <p className="font-medium">|</p>
                  <p className="font-medium">{song.duration}</p> */}
                </div>
                <div className="flex items-center gap-4">
                  <button
                    onClick={() => playPreview(song.id, song.preview_url)}
                    className="bg-blue-500 hover:bg-blue-600 text-white p-2 rounded-full transition"
                  >
                    {currentSong === song.id ? "⏸️" : "▶️"}
                  </button>
                </div>
              </li>
            ))}
          </ul>
          <div className="flex gap-2 justify-between items-center flex-wrap">
            <Button
              className="w-full mt-4 max-w-3xs md:max-w-xs items-self-center !bg-[#484848] hover:!border-white"
              onClick={() => navigate(-1)}
            >
              Voltar
            </Button>
            <Button
              className="w-full mt-4 max-w-3xs md:max-w-xs items-self-center !bg-[#497289] hover:!bg-[#3e5c7d] hover:!border-white"
              onClick={handleContinue}
              disabled={loading}
            >
              {loading ? (
                <Loader2 className="animate-spin mr-2 h-4 w-4" />
              ) : (
                "Continuar"
              )}
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default SongList;
