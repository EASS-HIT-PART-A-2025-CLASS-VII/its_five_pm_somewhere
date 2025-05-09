from typing import List
from .ingredient import Ingredient
from pydantic import BaseModel


class DrinkRecipe(BaseModel):
    id: str
    name: str
    ingredients: List[Ingredient]
    instructions: List[str]
    alcoholContent: bool
    type: str  # e.g., "Cocktail", "Mocktail", "Shot"
    imageUrl: str
    isFavorite: bool
