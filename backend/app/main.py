# --- System and utilities ---
import os
import sys
import requests
from dotenv import load_dotenv
import uuid
import random

# Add shared folder to path before importing anything from it
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'shared')))

# --- Imports ---
from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from shared.models import Ingredient, DrinkRecipe, DrinkAIResult, ErrorResponse, ImageSearchRequest
from .drink_data import drink_db
from typing import List

# Pydantic AI dependencies
from pydantic_ai import Agent, RunContext, ModelRetry
from pydantic_ai.models.groq import GroqModel
from pydantic_ai.providers.groq import GroqProvider

# --- Load Environment variables ---
load_dotenv()
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY", "")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

# --- FastAPI App Initialization ---
app = FastAPI()

# --- Middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Set up CORS to allow all origins (for development; restrict in production)
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
        "If the ingredients are insufficient to create a proper drink, return an ErrorResponse object "
        "with a helpful error_message explaining why.\n\n"
        "Return a valid DrinkRecipe object with:\n"
        "- A creative and fitting name.\n"
        "- Logical and realistic ingredients (amount + name).\n"
        "- Clear, step-by-step instructions.\n"
        "- alcoholContent set to true if any ingredient contains alcohol.\n"
        "- A fitting type (e.g., 'Cocktail', 'Mocktail', 'Shot').\n"
        "- isFavorite should always be false.\n"
        "- id is not relevant, so set it to '0'.\n"
        "- imageUrl is not relevant, so set it to '0'.\n"
        "- Do not make up or invent ingredients; only use the provided list (or a subset if necessary)."
    ),
    result_type=DrinkAIResult,
    deps_type=None,
)

# --- Utility Function ---
def get_pexels_images(name: str, count: int, page: int):
    params = {
        "query": name,
        "per_page": count,
        "page": page
    }

    response = requests.get(PEXELS_BASE_URL, headers=pexels_headers, params=params)

    if response.status_code != 200:
        return ErrorResponse(error_code=response.status_code, message="Pexels API error: " + response.text)
    
    photos = response.json().get("photos", [])
    return [photo["src"]["medium"] for photo in photos]

@mixology_agent.result_validator
async def validate_ai_output(ctx: RunContext[None], result: DrinkAIResult) -> DrinkAIResult:
    """Ensure the AI returns a valid drink recipe or a meaningful error."""

    # If it's an error object, validate the message exists
    if isinstance(result, ErrorResponse):
        if not result.error_code or not result.message.strip():
            return ErrorResponse(error_code=500, message="Hmm, the AI had a hiccup and didn’t explain why. Let’s give it another shot!")
        return result

    # Let the model decide if not enough ingredients — only check for schema issues here
    if (
        not result.name.strip() or
        not result.ingredients or
        any(not i.name.strip() or not i.amount.strip() for i in result.ingredients) or
        not result.instructions or
        any(not step.strip() for step in result.instructions) or
        not isinstance(result.alcoholContent, bool) or
        not result.type.strip()
    ):
        # Fallback if model tried returning DrinkRecipe but it's broken
        return ErrorResponse(error_code=500, message="Looks like the recipe’s missing a few important details—maybe the AI got distracted. Try again with a new list of ingredients!")

    return result


# --- Routes ---
@app.get("/drinks", response_model=List[DrinkRecipe])
def list_all_drinks():
    """Get all saved drink recipes."""
    return drink_db


@app.post("/drinks/images", response_model=List[str])
def fetch_drink_images(request: ImageSearchRequest):
    """Fetch drink-related images from Pexels API."""
    result = get_pexels_images(request.name, request.count, request.page)

    if isinstance(result, ErrorResponse):
        raise HTTPException(status_code=result.error_code, detail="Looks like our image search is a bit thirsty! No photo this time, but the recipe is still delicious.")

    return result


@app.post("/drinks", response_model=DrinkRecipe)
def add_new_drink(drink: DrinkRecipe):
    """Add a custom drink recipe to the list."""

    if (
        not drink.name.strip() or
        not drink.ingredients or
        any(not i.name.strip() or not i.amount.strip() for i in drink.ingredients) or
        not drink.instructions or
        any(not step.strip() for step in drink.instructions) or
        not isinstance(drink.alcoholContent, bool) or
        not drink.type.strip() or
        not drink.imageUrl.startswith("https://") 
    ):
        raise HTTPException( status_code=400, detail="Looks like some details are missing or incomplete in the drink recipe. Please make sure to provide all necessary information like the name, ingredients, instructions, and image URL. Don't worry, we’ve got you covered!")

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
    raise HTTPException(status_code=404, detail="Hmm, we couldn’t find that drink. Maybe it got shaken, not stirred?")


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

    if isinstance(ai_result.data, ErrorResponse):
            raise HTTPException(status_code=422, detail=ai_result.data.message)

    new_drink = ai_result.data
    
    result = get_pexels_images(new_drink.name, 1, 1)

    if isinstance(result, ErrorResponse):
        raise HTTPException(status_code=result.error_code, detail="Oops! Something went wrong while fetching images for your drink. Please try again later!")

    new_drink.imageUrl = result[0]
    new_drink.id = str(uuid.uuid4())
    drink_db.append(new_drink)

    return new_drink
