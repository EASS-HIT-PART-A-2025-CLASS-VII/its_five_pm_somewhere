from typing import List
from pydantic import BaseModel, Field, HttpUrl

from .ingredient import Ingredient
from .drink_type import DrinkType


class DrinkRecipe(BaseModel):
    id: str
    name: str = Field(..., min_length=2)
    ingredients: List[Ingredient] = Field(..., min_length=1)
    instructions: List[str] = Field(..., min_length=1)
    alcoholContent: bool
    type: DrinkType
    imageUrl: HttpUrl
    isFavorite: bool
