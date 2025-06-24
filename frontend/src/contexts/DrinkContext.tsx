import { createContext, useState, ReactNode, useContext, useEffect } from 'react';
import { DrinkRecipe } from '../client';
import { getAllDrinks, addNewDrink, toggleFavorite, generateDrinkFromIngredients, getRandomDrink } from '../services/drinkService';
import { fetchDrinkImages } from '../services/imageService';
import { IMAGES_PER_PAGE } from '../constants'

interface DrinkContextType {
  drinks: DrinkRecipe[];
  randomDrink: DrinkRecipe | null;
  loading: boolean;
  error: string | null;
  fetchDrinks: () => void;
  addDrink: (drink: DrinkRecipe) => void;
  toggleFavoriteStatus: (drinkId: string) => void;
  generateDrink: (ingredients: string[]) => void;
  fetchRandomDrink: () => void;
  fetchImages: (query: string, page: number) => Promise<string[] | undefined>;
  clearError: () => void;
}

const DrinkContext = createContext<DrinkContextType | undefined>(undefined);

interface DrinkProviderProps {
  children: ReactNode;  // Explicitly defining the children prop type
}

export const DrinkProvider: React.FC<DrinkProviderProps> = ({ children }) => {
  const [drinks, setDrinks] = useState<DrinkRecipe[]>([]);
  const [randomDrink, setRandomDrink] = useState<DrinkRecipe | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchDrinks();
  }, []);

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

  // Note: This function is intended for use with components that handle their own loading and error states.
  // The consuming component should manage loading and error display locally, not via the global context.
  const fetchImages = async (query: string, page: number) => {
    const request = { name: query, count: IMAGES_PER_PAGE, page }
    return await fetchDrinkImages(request);
  };

  const clearError = () => setError(null);

  return (
    <DrinkContext.Provider
      value={{
        drinks,
        randomDrink,
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

export const useDrinkContext = (): DrinkContextType => {
  const context = useContext(DrinkContext);
  if (!context) {
    throw new Error('useDrinkContext must be used within a DrinkProvider');
  }
  return context;
};
