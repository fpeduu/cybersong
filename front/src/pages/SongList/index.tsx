import { Button } from "@/components/ui/button";
import { SelectedSong, sendSelectedMusic, Song } from "@/services/musicService";
import { useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { Loader2 } from "lucide-react";

function SongList() {
  const location = useLocation();
  const { songs } = location.state || { songs: [] };
  const navigate = useNavigate();

  const themes = ["futurista", "pré-histórico", "retrô", "clássico", "moderno"]; // Lista de temas

  const [currentSong, setCurrentSong] = useState<number | null>(null);
  const [audio, setAudio] = useState<HTMLAudioElement | null>(null);
  const [selectedSong, setSelectedSong] = useState<SelectedSong | null>(null);
  const [selectedTheme, setSelectedTheme] = useState<string>(themes[0]); // Tema padrão
  const [loading, setLoading] = useState(false);

  const handleSelectSong = (song: Song) => {
    setSelectedSong({ ...song, theme: selectedTheme });
  };

  const handleThemeChange = (theme: string) => {
    setSelectedTheme(theme);
    if (selectedSong) {
      setSelectedSong({ ...selectedSong, theme });
    }
  };

  const playPreview = (songId: number, previewUrl: string) => {
    if (audio) {
      audio.pause();
      setCurrentSong(null);
    }

    const newAudio = new Audio(previewUrl);
    setAudio(newAudio);
    setCurrentSong(songId);

    newAudio.play();

    setTimeout(() => {
      newAudio.pause();
      setCurrentSong(null);
    }, 5000);
  };

  const handleContinue = async () => {
    if (selectedSong) {
      try {
        setLoading(true);
        const url = await sendSelectedMusic(selectedSong);
        navigate("/video-result", { state: { videoUrl: url } });
      } catch (error) {
        console.error("Erro ao enviar música:", error);
      } finally {
        setLoading(false);
      }
    } else {
      alert("Selecione uma música para continuar");
    }
  };

  return (
    <div className="relative home flex flex-col justify-center items-center w-screen min-h-screen bg-[var(--color-primary)] text-white px-8 gap-8 !overflow-hidden">
      <div className="w-64 h-72 md:w-[432px] md:h-[466px] absolute bottom-[-1rem] right-[-1rem] bg-contain bg-center bg-no-repeat bg-[url('/design-rt.svg')] overflow-hidden rotate-90"></div>
      <div className="flex items-center justify-center text-white z-10">
        <div className="w-full max-w-6xl lg:min-w-[780px] p-6 rounded-lg shadow-lg">
          <h2 className="text-lg mb-4">Músicas Encontradas</h2>
          <ul className="space-y-4">
            {songs.map((song: Song) => (
              <li
                key={song.id}
                className={`flex justify-between w-full items-center mb-0 py-3 border-t divide-solid cursor-pointer ${
                  selectedSong?.id === song.id ? "text-[#497289]" : ""
                }`}
                onClick={() => handleSelectSong(song)}
              >
                <div className="flex items-center gap-2">
                  <p className="font-medium">{song.title}</p>
                  <p className="font-medium">|</p>
                  <p className="font-medium">{song.artist}</p>
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

          <div className="mt-4">
            <h3 className="text-lg mb-2">Escolha um tema:</h3>
            <div className="flex gap-4">
              {themes.map((theme) => (
                <label key={theme} className="flex items-center gap-2">
                  <input
                    type="radio"
                    name="theme"
                    value={theme}
                    checked={selectedTheme === theme}
                    onChange={() => handleThemeChange(theme)}
                    className="text-[#497289] accent-blue-600"
                  />
                  {theme.charAt(0).toUpperCase() + theme.slice(1)}
                </label>
              ))}
            </div>
          </div>

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
