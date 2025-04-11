export interface Ingredient {
    name: string;
    amount: string;
}

export interface DrinkRecipe {
    id: string;
    name: string;
    ingredients: Ingredient[];
    instructions: string[];
    alcoholContent: boolean;
    type: string; // e.g., "Cocktail", "Mocktail", "Shot"
    imageUrl: string;
    isFavorite: boolean;
}
