from typing import List, Optional
from pydantic import BaseModel, Field, HttpUrl
from enum import Enum
from uuid import UUID, uuid4

from .ingredient import Ingredient


class DrinkType(str, Enum):
    COCKTAIL = "Cocktail"
    MOCKTAIL = "Mocktail"
    SHOT = "Shot"
    SMOOTHIE = "Smoothie"
    MILKSHAKE = "Milkshake"
    PUNCH = "Punch"
    COFFEE_DRINK = "Coffee Drink"
    TEA_DRINK = "Tea Drink"
    HOT_CHOCOLATE = "Hot Chocolate"


class DrinkRecipe(BaseModel):
    id: Optional[UUID] = Field(default_factory=uuid4)
    name: str = Field(..., min_length=2)
    ingredients: List[Ingredient] = Field(..., min_length=1)
    instructions: List[str] = Field(..., min_length=1)
    alcoholContent: bool
    type: DrinkType
    imageUrl: Optional[HttpUrl] = None
    isFavorite: bool
