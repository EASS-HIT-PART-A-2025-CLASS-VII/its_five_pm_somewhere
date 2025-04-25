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

class ErrorResponse(BaseModel):
    error_code: int
    message: str

class ImageSearchRequest(BaseModel):
    name: str
    count: int # Number of images per page
    page: int # Page number for pagination

# Unified result type for validation
DrinkAIResult = Union[DrinkRecipe, ErrorResponse]