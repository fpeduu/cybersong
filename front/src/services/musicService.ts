import axios from "axios";

const API_URL = "https://489b-150-161-2-200.ngrok-free.app"; // Endpoint de produção

export interface Song {
  id: number;
  title: string;
  artist: string;
  album: string;
  preview_url: string;
  duration: number;
}
export interface SelectedSong extends Song {
  theme: string;
}

export const searchMusic = async (
  artist: string,
  title: string
): Promise<Song[]> => {
  try {
    const response = await axios.get(`${API_URL}/api/search`, {
      headers: {
        "ngrok-skip-browser-warning": "true"
      },
      params: { artist, title },
    });
    return response.data.results;
  } catch (error) {
    console.error("Erro ao buscar músicas:", error);
    return [];
  }
};

// Envia música selecionada para o backend
export const sendSelectedMusic = async (song: SelectedSong) => {
  try {
    const response = await axios.post(`${API_URL}/api/select`, song, {
      headers: {
        "ngrok-skip-browser-warning": "true"
      },
      responseType: "blob",
    });
    if (response.status === 200) {
      // Criar uma URL para o arquivo de vídeos
      const videoBlob = new Blob([response.data], { type: "video/mp4" });
      const videoUrl = URL.createObjectURL(videoBlob);
      return videoUrl;
    }
  } catch (error) {
    console.error("Erro ao enviar música:", error);
    throw error;
  }
};
