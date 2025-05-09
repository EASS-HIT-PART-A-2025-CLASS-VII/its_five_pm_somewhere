from pydantic import BaseModel


class Ingredient(BaseModel):
    name: str
    amount: str  # e.g., "50ml", "1 tsp"
