import { createContext, useState, ReactNode, useContext, useEffect } from 'react';
import { DrinkRecipe } from '../client';
import { getAllDrinks, addNewDrink, toggleFavorite, generateDrinkFromIngredients, getRandomDrink } from '../services/drinkService';
import { fetchDrinkImages } from '../services/imageService';
import { IMAGES_PER_PAGE } from '../constants'

interface DrinkContextType {
  drinks: DrinkRecipe[];
  loading: boolean;
  error: string | null;
  fetchDrinks: () => void;
  addDrink: (drink: DrinkRecipe) => Promise<DrinkRecipe>;
  toggleFavoriteStatus: (drinkId: string) => void;
  generateDrink: (ingredients: string[]) => Promise<DrinkRecipe>;
  fetchRandomDrink: () => Promise<DrinkRecipe>;
  fetchImages: (query: string, page: number) => Promise<number[] | undefined>;
  clearError: () => void;
  getDrinkById: (id: string) => DrinkRecipe | undefined;
}

const DrinkContext = createContext<DrinkContextType | undefined>(undefined);

interface DrinkProviderProps {
  children: ReactNode;  // Explicitly defining the children prop type
}

export const DrinkProvider: React.FC<DrinkProviderProps> = ({ children }) => {
  const [drinks, setDrinks] = useState<DrinkRecipe[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [imageIdCache, setImageIdCache] = useState<Record<string, number[]>>({});


  useEffect(() => {
    fetchDrinks();
  }, []);

  const sortDrinksByName = (drinks: DrinkRecipe[]): DrinkRecipe[] => {
    return [...drinks].sort((a, b) => a.name.localeCompare(b.name));
  };


  const fetchDrinks = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await getAllDrinks();
      setDrinks(sortDrinksByName(data));
    } catch (err) {
      setError('Error fetching drinks');
    } finally {
      setLoading(false);
    }
  };

  const addDrink = async (drink: DrinkRecipe): Promise<DrinkRecipe> => {
    setLoading(true);
    setError(null);
    try {
      const newDrink = await addNewDrink(drink);
      setDrinks((prevDrinks) => sortDrinksByName([...prevDrinks, newDrink]));
      return newDrink;
    } catch (err) {
      setError('Error adding drink');
      throw err;
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
        sortDrinksByName(
          prevDrinks.map((drink) =>
            drink.id === updatedDrink.id ? updatedDrink : drink
          )
        )
      );
    } catch (err) {
      setError('Error toggling favorite');
    } finally {
      setLoading(false);
    }
  };

  //The component manages loading and error states internally, not through the global context.
  const generateDrink = async (ingredients: string[]): Promise<DrinkRecipe> => {
    try {
      const generatedDrink = await generateDrinkFromIngredients(ingredients);
      setDrinks((prevDrinks) => sortDrinksByName([...prevDrinks, generatedDrink]));
      return generatedDrink;
    } catch (err) {
      throw err;
    }
  };

  const fetchRandomDrink = async (): Promise<DrinkRecipe> => {
    setLoading(true);
    setError(null);
    try {
      const randomDrink = await getRandomDrink();
      return randomDrink
    } catch (err) {
      setError('Error fetching random drink');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  //The component manages loading and error states internally, not through the global context.
  const fetchImages = async (query: string, page: number) => {
    const cacheKey = `${query}:${page}`;
    if (imageIdCache[cacheKey]) return imageIdCache[cacheKey];
    try {
      const request = { name: query, count: IMAGES_PER_PAGE, page };
      const result = await fetchDrinkImages(request) || [];
      setImageIdCache(prev => ({ ...prev, [cacheKey]: result }));
      return result;
    } catch (err) {
      throw err;
    }
  };

  const clearError = () => setError(null);

  const getDrinkById = (id: string): DrinkRecipe | undefined => {
    return drinks.find(drink => drink.id === id);
  };


  return (
    <DrinkContext.Provider
      value={{
        drinks,
        loading,
        error,
        fetchDrinks,
        addDrink,
        toggleFavoriteStatus,
        generateDrink,
        fetchRandomDrink,
        fetchImages,
        clearError,
        getDrinkById
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
