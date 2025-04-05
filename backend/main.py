from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware
import random
# import json

app = FastAPI()

# Set up CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Ingredient(BaseModel):
    id: str
    name: str
    amount: str  # e.g., "50ml", "1 tsp", etc.

class DrinkRecipe(BaseModel):
    id: str
    name: str
    ingredients: List[Ingredient]
    instructions: List[str]
    alcoholContent: bool
    type: str  # "Cocktail" | "Mocktail" | "Shot"
    imageUrl: str
    isFavorite: bool

# Local in-memory array to store drink recipes
drink_recipes = [
    DrinkRecipe(
        id="1",
        name="Mojito",
        ingredients=[
            Ingredient(id="1", name="White Rum", amount="50ml"),
            Ingredient(id="2", name="Mint Leaves", amount="10 leaves"),
            Ingredient(id="3", name="Lime", amount="1/2"),
            Ingredient(id="4", name="Sugar", amount="2 tsp"),
            Ingredient(id="5", name="Club Soda", amount="Top it up")
        ],
        instructions=[
            "Muddle mint leaves and sugar in a glass.",
            "Add lime juice and rum.",
            "Fill the glass with ice and top it up with club soda.",
            "Stir gently and garnish with a mint sprig."
        ],
        alcoholContent=True,
        type="Cocktail",
        imageUrl="https://unsplash.com/s/photos/mojito",
        isFavorite=False
    ),
    DrinkRecipe(
        id="2",
        name="Martini",
        ingredients=[
            Ingredient(id="1", name="Gin", amount="60ml"),
            Ingredient(id="2", name="Dry Vermouth", amount="10ml"),
            Ingredient(id="3", name="Olive", amount="1")
        ],
        instructions=[
            "Pour gin and dry vermouth into a mixing glass.",
            "Fill with ice and stir for 20-30 seconds.",
            "Strain into a chilled martini glass and garnish with an olive."
        ],
        alcoholContent=True,
        type="Cocktail",
        imageUrl="https://unsplash.com/s/photos/martini",
        isFavorite=False
    ),
    DrinkRecipe(
        id="3",
        name="Gin and Tonic",
        ingredients=[
            Ingredient(id="1", name="Gin", amount="50ml"),
            Ingredient(id="2", name="Tonic Water", amount="Top it up"),
            Ingredient(id="3", name="Lime", amount="1/4")
        ],
        instructions=[
            "Pour gin into a glass filled with ice.",
            "Top it up with tonic water.",
            "Garnish with a lime wedge."
        ],
        alcoholContent=True,
        type="Cocktail",
        imageUrl="https://unsplash.com/s/photos/gin-and-tonic",
        isFavorite=False
    ),
    DrinkRecipe(
        id="4",
        name="Old Fashioned",
        ingredients=[
            Ingredient(id="1", name="Bourbon", amount="50ml"),
            Ingredient(id="2", name="Sugar", amount="1 tsp"),
            Ingredient(id="3", name="Angostura Bitters", amount="2 dashes"),
            Ingredient(id="4", name="Orange Peel", amount="1 piece")
        ],
        instructions=[
            "Muddle the sugar and bitters in a glass.",
            "Add bourbon and stir with ice.",
            "Garnish with an orange peel."
        ],
        alcoholContent=True,
        type="Cocktail",
        imageUrl="https://unsplash.com/s/photos/old-fashioned",
        isFavorite=False
    ),
    DrinkRecipe(
        id="5",
        name="Piña Colada",
        ingredients=[
            Ingredient(id="1", name="White Rum", amount="50ml"),
            Ingredient(id="2", name="Coconut Cream", amount="30ml"),
            Ingredient(id="3", name="Pineapple Juice", amount="90ml"),
            Ingredient(id="4", name="Pineapple Slice", amount="1 piece")
        ],
        instructions=[
            "Blend all ingredients with ice.",
            "Pour into a glass and garnish with a pineapple slice."
        ],
        alcoholContent=True,
        type="Cocktail",
        imageUrl="https://unsplash.com/s/photos/pina-colada",
        isFavorite=False
    ),
    DrinkRecipe(
        id="6",
        name="Margarita",
        ingredients=[
            Ingredient(id="1", name="Tequila", amount="50ml"),
            Ingredient(id="2", name="Lime Juice", amount="30ml"),
            Ingredient(id="3", name="Triple Sec", amount="20ml"),
            Ingredient(id="4", name="Salt", amount="For the rim")
        ],
        instructions=[
            "Rub a lime wedge around the rim of a glass and dip it in salt.",
            "Shake tequila, lime juice, and triple sec with ice.",
            "Strain into the prepared glass."
        ],
        alcoholContent=True,
        type="Cocktail",
        imageUrl="https://unsplash.com/s/photos/margarita",
        isFavorite=False
    ),
    DrinkRecipe(
        id="7",
        name="Cosmopolitan",
        ingredients=[
            Ingredient(id="1", name="Vodka", amount="45ml"),
            Ingredient(id="2", name="Triple Sec", amount="15ml"),
            Ingredient(id="3", name="Lime Juice", amount="15ml"),
            Ingredient(id="4", name="Cranberry Juice", amount="30ml")
        ],
        instructions=[
            "Shake all ingredients with ice.",
            "Strain into a chilled martini glass."
        ],
        alcoholContent=True,
        type="Cocktail",
        imageUrl="https://unsplash.com/s/photos/cosmopolitan",
        isFavorite=False
    ),
    DrinkRecipe(
        id="8",
        name="Bloody Mary",
        ingredients=[
            Ingredient(id="1", name="Vodka", amount="50ml"),
            Ingredient(id="2", name="Tomato Juice", amount="100ml"),
            Ingredient(id="3", name="Lemon Juice", amount="15ml"),
            Ingredient(id="4", name="Tabasco Sauce", amount="Few dashes"),
            Ingredient(id="5", name="Worcestershire Sauce", amount="Few dashes")
        ],
        instructions=[
            "Shake all ingredients with ice.",
            "Strain into a tall glass and garnish with a celery stick."
        ],
        alcoholContent=True,
        type="Cocktail",
        imageUrl="https://unsplash.com/s/photos/bloody-mary",
        isFavorite=False
    ),
    DrinkRecipe(
        id="9",
        name="Mai Tai",
        ingredients=[
            Ingredient(id="1", name="Rum", amount="30ml"),
            Ingredient(id="2", name="Orange Curaçao", amount="15ml"),
            Ingredient(id="3", name="Orgeat Syrup", amount="15ml"),
            Ingredient(id="4", name="Lime Juice", amount="30ml"),
            Ingredient(id="5", name="Mint Leaves", amount="For garnish")
        ],
        instructions=[
            "Shake all ingredients with ice.",
            "Strain into a glass filled with crushed ice and garnish with mint leaves."
        ],
        alcoholContent=True,
        type="Cocktail",
        imageUrl="https://unsplash.com/s/photos/mai-tai",
        isFavorite=False
    ),
    DrinkRecipe(
        id="10",
        name="Whiskey Sour",
        ingredients=[
            Ingredient(id="1", name="Whiskey", amount="50ml"),
            Ingredient(id="2", name="Lemon Juice", amount="25ml"),
            Ingredient(id="3", name="Simple Syrup", amount="15ml"),
            Ingredient(id="4", name="Egg White", amount="1")
        ],
        instructions=[
            "Shake all ingredients without ice to emulsify.",
            "Add ice and shake again.",
            "Strain into a glass and garnish with a cherry."
        ],
        alcoholContent=True,
        type="Cocktail",
        imageUrl="https://unsplash.com/s/photos/whiskey-sour",
        isFavorite=False
    )
]


# 1. Get all drink recipes
@app.get("/drinks", response_model=List[DrinkRecipe])
def get_drinks():
    return drink_recipes

# 2. Add a new drink recipe
@app.post("/drinks", response_model=DrinkRecipe)
def add_drink(drink: DrinkRecipe):
    drink_recipes.append(drink)
    return drink

# 3. Change favorite status of a drink
@app.patch("/drinks/{drink_id}/favorite", response_model=DrinkRecipe)
def change_favorite(drink_id: str):
    # Find the drink recipe by ID
    for drink in drink_recipes:
        if drink.id == drink_id:
            drink.isFavorite = not drink.isFavorite  # Toggle the favorite status
            return drink
    raise HTTPException(status_code=404, detail="Drink not found")

# 4. Generate a drink recipe based on ingredients
@app.post("/drinks/generate", response_model=DrinkRecipe)
def generate_drink(ingredients: List[str]):
    # A simple mock generation logic (you can replace this with a more complex one)
    if not ingredients:
        raise HTTPException(status_code=400, detail="Ingredients list is required")
    
    # Randomly generate a drink name
    drink_name = f"Generated Drink {random.randint(1, 100)}"
    
    # Generate the recipe details based on ingredients (just a mock-up)
    generated_recipe = DrinkRecipe(
        id=str(random.randint(1, 1000)),
        name=drink_name,
        ingredients=[Ingredient(id=str(i), name=ingredient, amount="50ml") for i, ingredient in enumerate(ingredients)],
        instructions=["Mix the ingredients in a shaker and serve."],
        alcoholContent=random.choice([True, False]),
        type=random.choice(["Cocktail", "Mocktail", "Shot"]),
        imageUrl="https://example.com/drink.jpg",
        isFavorite=False
    )
    
    # Return the generated drink recipe
    return generated_recipe