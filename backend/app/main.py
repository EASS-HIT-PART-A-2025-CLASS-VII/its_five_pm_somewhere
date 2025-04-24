# --- Imports ---

from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Union, List
from pydantic import BaseModel

# Pydantic AI dependencies
from pydantic_ai import Agent, RunContext, ModelRetry
from pydantic_ai.models.groq import GroqModel
from pydantic_ai.providers.groq import GroqProvider

# System and utilities
import requests
import nest_asyncio
import os
from dotenv import load_dotenv


# --- Load Environment variables ---
load_dotenv()
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")


# --- Setup for async environments ---
nest_asyncio.apply()


# --- FastAPI App Initialization ---
app = FastAPI()

# --- Middleware ---
# Set up CORS to allow all origins (for development; restrict in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Data Models ---

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

class InvalidDrinkRequest(BaseModel):
    error_message: str

# Unified result type for validation
DrinkAIResult = Union[DrinkRecipe, InvalidDrinkRequest]


# --- In-Memory Store ---
drink_db: List[DrinkRecipe] = [
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
        imageUrl="https://images.pexels.com/photos/1187766/pexels-photo-1187766.jpeg?auto=compress&cs=tinysrgb&h=350",
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
        imageUrl="https://images.pexels.com/photos/2531186/pexels-photo-2531186.jpeg?auto=compress&cs=tinysrgb&h=350",
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
        imageUrl="https://images.pexels.com/photos/616836/pexels-photo-616836.jpeg?auto=compress&cs=tinysrgb&h=350",
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
        imageUrl="https://images.pexels.com/photos/31589567/pexels-photo-31589567.jpeg?auto=compress&cs=tinysrgb&h=350",
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
        imageUrl="https://images.pexels.com/photos/8944950/pexels-photo-8944950.jpeg?auto=compress&cs=tinysrgb&h=350",
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
        imageUrl="https://images.pexels.com/photos/1590154/pexels-photo-1590154.jpeg?auto=compress&cs=tinysrgb&h=350",
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
        imageUrl="https://images.pexels.com/photos/31623993/pexels-photo-31623993.jpeg?auto=compress&cs=tinysrgb&h=350",
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
        imageUrl="https://images.pexels.com/photos/7376796/pexels-photo-7376796.jpeg?auto=compress&cs=tinysrgb&h=350",
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
        imageUrl="https://images.pexels.com/photos/11481550/pexels-photo-11481550.jpeg?auto=compress&cs=tinysrgb&h=350",
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
        imageUrl="https://images.pexels.com/photos/28834354/pexels-photo-28834354.jpeg?auto=compress&cs=tinysrgb&h=350",
        isFavorite=False
    )
]

# --- AI Agent Setup ---
PEXELS_BASE_URL = "https://api.pexels.com/v1/search"

pexels_headers = {
    "Authorization": PEXELS_API_KEY
}

llm_model = GroqModel("llama-3.3-70b-versatile", provider=GroqProvider(api_key=GROQ_API_KEY))

mixology_agent: Agent[None, DrinkAIResult] = Agent(
    model=llm_model,
    system_prompt=(
        "You are a professional mixologist assistant. "
        "Given a list of ingredient names, generate a creative and well-balanced drink recipe. "
        "You may ignore ingredients that do not fit well together or are not relevant. "
        "If the ingredients are insufficient to create a proper drink, return an InvalidDrinkRequest object "
        "with a helpful error_message explaining why.\n\n"
        "Return a valid DrinkRecipe object with:\n"
        "- A creative and fitting name.\n"
        "- Logical and realistic ingredients (amount + name).\n"
        "- Clear, step-by-step instructions.\n"
        "- alcoholContent set to true if any ingredient contains alcohol.\n"
        "- A fitting type (e.g., 'Cocktail', 'Mocktail', 'Shot').\n"
        "- imageUrl must be in this format: 'https://www.pexels.com/search/drink-name/'\n"
        "  (replace spaces with hyphens and make it lowercase).\n"
        "- Do not make up or invent ingredients; only use the provided list (or a subset if necessary)."
    ),
    result_type=DrinkAIResult,
    deps_type=None,
)

@mixology_agent.result_validator
async def validate_ai_output(ctx: RunContext[None], result: DrinkAIResult) -> DrinkAIResult:
    """Ensure the AI returns a valid drink recipe or a meaningful error."""

    # If it's an error object, validate the message exists
    if isinstance(result, InvalidDrinkRequest):
        if not result.error_message.strip():
            return InvalidDrinkRequest(error_message="An unknown error occurred. Please try again.")
        return result

    # Let the model decide if not enough ingredients — only check for schema issues here
    if (
        not result.name.strip() or
        not result.ingredients or
        any(not i.name.strip() or not i.amount.strip() for i in result.ingredients) or
        not result.instructions or
        any(not step.strip() for step in result.instructions) or
        not isinstance(result.alcoholContent, bool) or
        not result.type.strip() or
        not result.imageUrl.startswith("https://") 
        # not result.imageUrl.endswith((".jpg", ".jpeg", ".png", ".webp", ".gif"))
    ):
        # Fallback if model tried returning DrinkRecipe but it's broken
        return InvalidDrinkRequest(error_message="The AI generated an incomplete or invalid recipe. Please try again.")

    return result


# --- API Endpoints ---

@app.get("/drinks", response_model=List[DrinkRecipe])
def list_all_drinks():
    """Get all saved drink recipes."""
    return drink_db


@app.get("/drinks/images", response_model=List[str])
def fetch_drink_images(
    name: str = Query(..., description="Search term for the image"),
    count: int = Query(6, description="Number of images per page"),
    page: int = Query(1, description="Page number for pagination")
):
    """Fetch drink-related images from Pexels API."""
    params = {
        "query": name,
        "per_page": count,
        "page": page
    }
    
    response = requests.get(PEXELS_BASE_URL, headers=pexels_headers, params=params)
    
    if response.status_code != 200:
        return {"error": f"Pexels API error: {response.status_code}"}
    
    photos = response.json().get("photos", [])
    return [photo["src"]["medium"] for photo in photos]


@app.post("/drinks", response_model=DrinkRecipe)
def add_new_drink(drink: DrinkRecipe):
    """Add a custom drink recipe to the list."""
    drink_db.append(drink)
    return drink


@app.patch("/drinks/{drink_id}/favorite", response_model=DrinkRecipe)
def toggle_favorite_status(drink_id: str):
    """Toggle favorite status of a specific drink."""
    for drink in drink_db:
        if drink.id == drink_id:
            drink.isFavorite = not drink.isFavorite
            return drink
    raise HTTPException(status_code=404, detail="Drink not found")


@app.post("/drinks/generate", response_model=DrinkRecipe)
def generate_drink_from_ingredients(ingredients: List[str]):
    """
    Generate a creative drink recipe using AI based on given ingredients.
    """
    ingredient_str = ", ".join(ingredients)
    user_prompt = f"Create a drink using the following ingredients: {ingredient_str}."

    ai_result = mixology_agent.run_sync(user_prompt)

    if isinstance(ai_result.data, InvalidDrinkRequest):
            raise HTTPException(
                status_code=422,
                detail=ai_result.data.error_message
            )

    new_drink = ai_result.data
    new_drink.id = str(len(drink_db) + 1)  # Simple ID assignment
    new_drink.isFavorite = False

    drink_db.append(new_drink)

    return new_drink
