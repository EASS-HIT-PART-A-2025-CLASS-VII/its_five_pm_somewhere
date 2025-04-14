import { createContext, useState, ReactNode , useContext, useEffect } from 'react';
import { getAllDrinks, addNewDrink, toggleFavorite, generateDrinkFromIngredients, getRandomDrink } from '../services/drinkService';
import { fetchDrinkImages } from '../services/imageService';
import { DrinkRecipe } from '../types/drink';

// Define the context type
interface DrinkContextType {
  drinks: DrinkRecipe[];
  randomDrink: DrinkRecipe | null;
  images: string[];
  loading: boolean;
  error: string | null;
  fetchDrinks: () => void;
  addDrink: (drink: DrinkRecipe) => void;
  toggleFavoriteStatus: (drinkId: string) => void;
  generateDrink: (ingredients: string[]) => void;
  fetchRandomDrink: () => void;
  fetchImages: (name: string) => void;
  clearError: () => void;
}

// Create the context
const DrinkContext = createContext<DrinkContextType | undefined>(undefined);

// Define the props for the provider component
interface DrinkProviderProps {
    children: ReactNode;  // Explicitly defining the children prop type
}

// The provider component that supplies the context value
export const DrinkProvider: React.FC<DrinkProviderProps> = ({ children }) => {
  const [drinks, setDrinks] = useState<DrinkRecipe[]>([]);
  const [randomDrink, setRandomDrink] = useState<DrinkRecipe | null>(null);
  const [images, setImages] = useState<string[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchDrinks();
  }, []);

  // Fetch all drinks
  const fetchDrinks = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await getAllDrinks();
      setDrinks(data);
    } catch (err) {
      setError('Error fetching drinks');
    } finally {
      setLoading(false);
    }
  };

  // Add a new drink
  const addDrink = async (drink: DrinkRecipe) => {
    setLoading(true);
    setError(null);
    try {
      const newDrink = await addNewDrink(drink);
      setDrinks((prevDrinks) => [...prevDrinks, newDrink]);
    } catch (err) {
      setError('Error adding drink');
    } finally {
      setLoading(false);
    }
  };

  // Toggle favorite status of a drink
  const toggleFavoriteStatus = async (drinkId: string) => {
    setLoading(true);
    setError(null);
    try {
      const updatedDrink = await toggleFavorite(drinkId);
      setDrinks((prevDrinks) =>
        prevDrinks.map((drink) => (drink.id === updatedDrink.id ? updatedDrink : drink))
      );
    } catch (err) {
      setError('Error toggling favorite');
    } finally {
      setLoading(false);
    }
  };

  // Generate a drink from ingredients
  const generateDrink = async (ingredients: string[]) => {
    setLoading(true);
    setError(null);
    try {
      const generatedDrink = await generateDrinkFromIngredients(ingredients);
      setRandomDrink(generatedDrink);
    } catch (err) {
      setError('Error generating drink');
    } finally {
      setLoading(false);
    }
  };

  // Fetch a random drink
  const fetchRandomDrink = async () => {
    setLoading(true);
    setError(null);
    try {
      const random = await getRandomDrink();
      setRandomDrink(random);
    } catch (err) {
      setError('Error fetching random drink');
    } finally {
      setLoading(false);
    }
  };

  // Fetch images for a drink
  const fetchImages = async (name: string) => {
    setLoading(true);
    setError(null);
    try {
      const drinkImages = await fetchDrinkImages(name);
      setImages(drinkImages);
    } catch (err) {
      setError('Error fetching drink images');
    } finally {
      setLoading(false);
    }
  };

  const clearError = () => setError(null);

  return (
    <DrinkContext.Provider
      value={{
        drinks,
        randomDrink,
        images,
        loading,
        error,
        fetchDrinks,
        addDrink,
        toggleFavoriteStatus,
        generateDrink,
        fetchRandomDrink,
        fetchImages,
        clearError
      }}
    >
      {children}
    </DrinkContext.Provider>
  );
};

// Custom hook to use the DrinkContext
export const useDrinkContext = (): DrinkContextType => {
  const context = useContext(DrinkContext);
  if (!context) {
    throw new Error('useDrinkContext must be used within a DrinkProvider');
  }
  return context;
};
