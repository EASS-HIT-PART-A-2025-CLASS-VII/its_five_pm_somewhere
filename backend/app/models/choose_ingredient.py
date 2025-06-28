from pydantic import BaseModel


class ChooseIngredient(BaseModel):
    name: str
    imageId: int
