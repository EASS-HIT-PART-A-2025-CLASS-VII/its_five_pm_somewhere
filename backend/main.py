from fastapi import FastAPI, Query
from typing import Union, List
from pydantic import BaseModel
from pydantic_ai import Agent, RunContext, ModelRetry
from pydantic_ai.models.groq import GroqModel
from pydantic_ai.providers.groq import GroqProvider
from fastapi.middleware.cors import CORSMiddleware
import nest_asyncio
import os
import requests

# Needed for notebook environments; in real API deployments you can skip this.
nest_asyncio.apply()

app = FastAPI()

# Set up CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Models ---
class Ingredient(BaseModel):
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

# Invalid result model
class InvalidDrinkRequest(BaseModel):
    error_message: str

# Union for AI result
DrinkResult = Union[DrinkRecipe, InvalidDrinkRequest]

# Local in-memory array to store drink recipes
drink_recipes = [
    DrinkRecipe(
        id="1",
        name="Mojito",
        ingredients=[
            Ingredient(name="White Rum", amount="50ml"),
            Ingredient(name="Mint Leaves", amount="10 leaves"),
            Ingredient(name="Lime", amount="1/2"),
            Ingredient(name="Sugar", amount="2 tsp"),
            Ingredient(name="Club Soda", amount="Top it up")
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
            Ingredient(name="Gin", amount="60ml"),
            Ingredient(name="Dry Vermouth", amount="10ml"),
            Ingredient(name="Olive", amount="1")
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
            Ingredient(name="Gin", amount="50ml"),
            Ingredient(name="Tonic Water", amount="Top it up"),
            Ingredient(name="Lime", amount="1/4")
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
            Ingredient(name="Bourbon", amount="50ml"),
            Ingredient(name="Sugar", amount="1 tsp"),
            Ingredient(name="Angostura Bitters", amount="2 dashes"),
            Ingredient(name="Orange Peel", amount="1 piece")
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
            Ingredient(name="White Rum", amount="50ml"),
            Ingredient(name="Coconut Cream", amount="30ml"),
            Ingredient(name="Pineapple Juice", amount="90ml"),
            Ingredient(name="Pineapple Slice", amount="1 piece")
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
            Ingredient(name="Tequila", amount="50ml"),
            Ingredient(name="Lime Juice", amount="30ml"),
            Ingredient(name="Triple Sec", amount="20ml"),
            Ingredient(name="Salt", amount="For the rim")
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
            Ingredient(name="Vodka", amount="45ml"),
            Ingredient(name="Triple Sec", amount="15ml"),
            Ingredient(name="Lime Juice", amount="15ml"),
            Ingredient(name="Cranberry Juice", amount="30ml")
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
            Ingredient(name="Vodka", amount="50ml"),
            Ingredient(name="Tomato Juice", amount="100ml"),
            Ingredient(name="Lemon Juice", amount="15ml"),
            Ingredient(name="Tabasco Sauce", amount="Few dashes"),
            Ingredient(name="Worcestershire Sauce", amount="Few dashes")
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
            Ingredient(name="Rum", amount="30ml"),
            Ingredient(name="Orange Curaçao", amount="15ml"),
            Ingredient(name="Orgeat Syrup", amount="15ml"),
            Ingredient(name="Lime Juice", amount="30ml"),
            Ingredient(name="Mint Leaves", amount="For garnish")
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
            Ingredient(name="Whiskey", amount="50ml"),
            Ingredient(name="Lemon Juice", amount="25ml"),
            Ingredient(name="Simple Syrup", amount="15ml"),
            Ingredient(name="Egg White", amount="1")
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

# --- AI agent setup ---
API_KEY = ""
PEXELS_API_KEY = ""
PEXELS_BASE_URL = "https://api.pexels.com/v1/search"

headers = {
    "Authorization": PEXELS_API_KEY
}

model = GroqModel("llama-3.3-70b-versatile", provider=GroqProvider(api_key=API_KEY))
agent: Agent[None, DrinkResult] = Agent(
    model=model,
    system_prompt=(
        "You are a professional mixologist assistant. "
        "Given a list of ingredient names, generate a creative and well-balanced drink recipe. "
        "You must return a valid DrinkRecipe object (as described in the schema) with detailed instructions, "
        "a creative name, and a fitting drink type. "
        "The imageUrl should be in the format: https://unsplash.com/s/photos/drink-name "
        "(replace spaces with hyphens and make it lowercase). "
        "Make sure the ingredients and instructions align logically and are realistic."
    ),
    result_type=DrinkResult,
    deps_type=None,
)

@agent.result_validator
async def validate_drink_result(ctx: RunContext[None], result: DrinkResult) -> DrinkResult:
    if isinstance(result, InvalidDrinkRequest):
        return result
    if not result.name or not result.ingredients or not result.instructions:
        raise ModelRetry("Incomplete recipe. Try again.")
    return result


# --- Endpoint ---
# 1. Get all drink recipes
@app.get("/drinks", response_model=List[DrinkRecipe])
def get_drinks():
    return drink_recipes


@app.get("/drinks/images")
def get_drink_images(
    name: str = Query(..., description="Search term for the image"),
    count: int = Query(6, description="Number of images per page"),
    page: int = Query(1, description="Page number for pagination")
) -> List[str]:
    params = {
        "query": name,
        "per_page": count,
        "page": page
    }
    
    response = requests.get(PEXELS_BASE_URL, headers=headers, params=params)
    
    if response.status_code != 200:
        return {"error": f"Pexels API error: {response.status_code}"}
    
    data = response.json()
    urls = [photo["src"]["medium"] for photo in data.get("photos", [])]
    return urls
    
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
    # Format the ingredient names into a prompt
    ingredient_str = ", ".join(ingredients)
    prompt = f"Create a drink using the following ingredients: {ingredient_str}."

    # Ask the AI for a drink recipe
    result = agent.run_sync(prompt)

    if isinstance(result.data, InvalidDrinkRequest):
        raise Exception(f"AI generation failed: {result.data.error_message}")

    new_recipe = result.data

    # Assign a unique ID (basic incremental ID for simplicity)
    new_recipe.id = str(len(drink_recipes) + 1)
    new_recipe.isFavorite = False

    # Add to in-memory list
    drink_recipes.append(new_recipe)

    return new_recipe