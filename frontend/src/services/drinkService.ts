import axios from 'axios';
import { DrinkRecipe } from '../client';

const API_URL = import.meta.env.VITE_REACT_APP_BACKEND_URL

// List all drinks
export const getAllDrinks = async (): Promise<DrinkRecipe[]> => {
  try {
    const response = await axios.get<DrinkRecipe[]>(`${API_URL}/drinks`);
    return response.data;
  } catch (error) {
    console.error('Error fetching drinks:', error);
    throw new Error('Could not fetch drinks');
  }
};

// Add a new drink recipe
export const addNewDrink = async (drink: DrinkRecipe): Promise<DrinkRecipe> => {
  try {
    const response = await axios.post<DrinkRecipe>(`${API_URL}/drinks`, drink);
    return response.data;
  } catch (error) {
    console.error('Error adding new drink:', error);
    throw new Error('Could not add the new drink');
  }
};

// Toggle the favorite status of a drink
export const toggleFavorite = async (drinkId: string): Promise<DrinkRecipe> => {
  try {
    const response = await axios.patch<DrinkRecipe>(`${API_URL}/drinks/${drinkId}/favorite`);
    return response.data;
  } catch (error) {
    console.error('Error toggling favorite status:', error);
    throw new Error('Could not toggle favorite status');
  }
};

// Generate a drink based on provided ingredients
export const generateDrinkFromIngredients = async (ingredients: string[]): Promise<DrinkRecipe> => {
  try {
    const response = await axios.post<DrinkRecipe>(`${API_URL}/drinks/generate`, { ingredients });
    return response.data;
  } catch (error) {
    console.error('Error generating drink from ingredients:', error);
    throw new Error('Could not generate drink');
  }
};

// Get a random drink
export const getRandomDrink = async (): Promise<DrinkRecipe> => {
  try {
    const response = await axios.get<DrinkRecipe>(`${API_URL}/drinks/random`);
    return response.data;
  } catch (error) {
    console.error('Error fetching random drink:', error);
    throw new Error('Could not fetch random drink');
  }
};
