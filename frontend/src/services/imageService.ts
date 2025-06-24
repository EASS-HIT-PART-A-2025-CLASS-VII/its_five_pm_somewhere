import axios from 'axios';
import { ImageSearchRequest } from '../client';

const API_URL = import.meta.env.VITE_REACT_APP_BACKEND_URL;

export const fetchDrinkImages = async (request: ImageSearchRequest): Promise<string[]> => {
  try {
    const response = await axios.post<string[]>(`${API_URL}/drinks/images`, request);
    return response.data;
  } catch (error) {
    console.error('Error fetching drink images:', error);
    throw new Error('Could not fetch drink images');
  }
};
