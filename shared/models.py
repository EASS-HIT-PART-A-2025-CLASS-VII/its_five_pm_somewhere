from typing import Union, List
from pydantic import BaseModel

class Ingredient(BaseModel):
    name: str
    amount: str  # e.g., "50ml", "1 tsp"

class DrinkRecipe(BaseModel):
    id: str
    name: str
    ingredients: List[Ingredient]
    instructions: List[str]
    alcoholContent: bool
    type: str  # e.g., "Cocktail", "Mocktail", "Shot"
    imageUrl: str
    isFavorite: bool

class InvalidDrinkRequest(BaseModel):
    error_message: str

# Unified result type for validation
DrinkAIResult = Union[DrinkRecipe, InvalidDrinkRequest]