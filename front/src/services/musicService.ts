import axios from "axios";

const API_URL = "http://localhost:8000"; // Atualize para o seu endpoint

export interface Song {
  id: number;
  title: string;
  artist: string;
  album: string;
  preview_url: string;
  duration: number;
}

export const searchMusic = async (
  artist: string,
  title: string
): Promise<Song[]> => {
  try {
    const response = await axios.get(`${API_URL}/api/search`, {
      params: { artist, title },
    });
    return response.data.results;
  } catch (error) {
    console.error("Erro ao buscar músicas:", error);
    return [];
  }
};

// Envia música selecionada para o backend
export const sendSelectedMusic = async (song: Song) => {
  try {
    const response = await axios.post(`${API_URL}/api/select`, song);
    return response.data;
  } catch (error) {
    console.error("Erro ao enviar música:", error);
    throw error;
  }
};
