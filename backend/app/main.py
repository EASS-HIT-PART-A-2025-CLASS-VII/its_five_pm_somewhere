# --- System and utilities ---
import os
import sys
import requests
import nest_asyncio
from dotenv import load_dotenv
import uuid
import random

# Add shared folder to path before importing anything from it
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'shared')))

# --- Imports ---
from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from shared.models import Ingredient, DrinkRecipe, InvalidDrinkRequest, DrinkAIResult
from .drink_data import drink_db
from typing import List

# Pydantic AI dependencies
from pydantic_ai import Agent, RunContext, ModelRetry
from pydantic_ai.models.groq import GroqModel
from pydantic_ai.providers.groq import GroqProvider



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
    drink.id = str(uuid.uuid4())
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


@app.get("/drinks/random", response_model=DrinkRecipe)
def get_random_drink():
    """Return a random drink from the database."""
    return random.choice(drink_db)


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
    new_drink.id = str(uuid.uuid4())
    new_drink.isFavorite = False

    drink_db.append(new_drink)

    return new_drink
