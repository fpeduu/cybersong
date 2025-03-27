import { Button } from "@/components/ui/button";
import { useState } from "react";

type Song = {
  id: number;
  title: string;
  artist: string;
  duration: string;
  preview: string; // Link para um trecho da música
};

function SongList() {
  //   const { data, loading, error } = useQuery(GET_SONGS);

  //   if (loading) return <p>Loading...</p>;
  //   if (error) return <p>Error :(</p>;

  const songs: Song[] = [
    {
      id: 1,
      title: "Blinding Lights",
      artist: "The Weeknd",
      duration: "3:20",
      preview: "https://p.scdn.co/mp3-preview/4a07c30c", // URL fictícia
    },
    {
      id: 2,
      title: "Shape of You",
      artist: "Ed Sheeran",
      duration: "3:53",
      preview: "https://p.scdn.co/mp3-preview/8f8e3cda", // URL fictícia
    },
    {
      id: 3,
      title: "Levitating",
      artist: "Dua Lipa",
      duration: "3:40",
      preview: "https://p.scdn.co/mp3-preview/d0cfe54b", // URL fictícia
    },
  ];

  const [currentSong, setCurrentSong] = useState<number | null>(null);
  const [audio, setAudio] = useState<HTMLAudioElement | null>(null);

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
    }, 5000); // Toca por 5 segundos
  };

  return (
    <div className="relative home flex flex-col justify-center items-center w-screen min-h-screen bg-[var(--color-primary)] text-white px-8 gap-8 !overflow-hidden">
      <div className="w-64 h-72 md:w-[432px] md:h-[466px] absolute bottom-[-1rem]  right-[-1rem] bg-contain bg-center bg-no-repeat bg-[url('/design-rt.svg')] overflow-hidden rotate-90"></div>{" "}
      <div className="flex items-center justify-center  text-white z-10">
        <div className="w-full max-w-6xl lg:min-w-[780px] p-6  rounded-lg shadow-lg">
          <h2 className="text-lg  mb-4">Músicas Encontradas</h2>
          <ul className="space-y-4">
            {songs.map((song) => (
              <li
                key={song.id}
                className="flex justify-between w-full items-center mb-0  py-3  border-t divide-solid  "
              >
                <div className="flex items-center gap-2">
                  <p className="font-medium">{song.title} </p>
                  <p className="font-medium">|</p>
                  <p className="font-medium">{song.artist}</p>
                  <p className="font-medium">|</p>
                  <p className="font-medium">{song.duration}</p>
                </div>
                <div className="flex items-center gap-4">
                  <button
                    onClick={() => playPreview(song.id, song.preview)}
                    className="bg-blue-500 hover:bg-blue-600 text-white p-2 rounded-full transition"
                  >
                    {currentSong === song.id ? "⏸️" : "▶️"}
                  </button>
                </div>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
}

export default SongList;
