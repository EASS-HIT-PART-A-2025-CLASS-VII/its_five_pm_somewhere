from typing import List
from app.models import ChooseIngredient

# --- In-Memory Store ---
ingredient_db: List[ChooseIngredient] = [
    ChooseIngredient(name="Lemon", imageId=1414110),
    ChooseIngredient(name="Lime", imageId=357577),
    ChooseIngredient(name="Mint", imageId=1264000),
    ChooseIngredient(name="Gin", imageId=1277203),
    ChooseIngredient(name="Tonic", imageId=8131585),
    ChooseIngredient(name="Strawberry", imageId=6944172),
    ChooseIngredient(name="Vodka", imageId=3738485),
    ChooseIngredient(name="Orange", imageId=691166),
]
