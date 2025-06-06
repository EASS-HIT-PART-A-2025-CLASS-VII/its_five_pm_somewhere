import axios from 'axios';

const API_URL = import.meta.env.VITE_REACT_APP_BACKEND_URL

// Fetch drink-related images from Pexels
export const fetchDrinkImages = async (name: string, count: number = 6, page: number = 1): Promise<string[]> => {
  try {
    const response = await axios.get<string[]>(`${API_URL}/drinks/images`, {
      params: {
        name,
        count,
        page,
      },
    });
    return response.data;
  } catch (error) {
    console.error('Error fetching drink images:', error);
    throw new Error('Could not fetch drink images');
  }
};
