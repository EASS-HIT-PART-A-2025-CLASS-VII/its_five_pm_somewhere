from pydantic import BaseModel
from enum import Enum


class Unit(str, Enum):
    GRAM = "g"
    MILLILITER = "ml"
    TEASPOON = "tsp"
    TABLESPOON = "tbsp"
    PIECE = "piece"
    DASH = "dash"
    TOP_UP = "top_up"


class Ingredient(BaseModel):
    name: str
    amount: float
    unit: Unit
