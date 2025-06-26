import os
import httpx
from dotenv import load_dotenv
import uuid
import random

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.models import (
    DrinkRecipe,
    ErrorResponse,
    ImageSearchRequest,
    DrinkAIResult,
    DrinkType,
    Unit,
)

from .drink_data import drink_db
from typing import List

from pydantic_ai import Agent, RunContext
from pydantic_ai.models.groq import GroqModel
from pydantic_ai.providers.groq import GroqProvider

# --- Load Environment variables ---
load_dotenv()
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY", "")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
PEXELS_BASE_URL = "https://api.pexels.com/v1/search"

# --- FastAPI App Initialization ---
app = FastAPI()

# --- Middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*"
    ],  # Set up CORS to allow all origins (for development; restrict in production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- AI Agent Setup ---
pexels_headers = {"Authorization": PEXELS_API_KEY}

llm_model = GroqModel(
    "meta-llama/llama-4-scout-17b-16e-instruct",
    provider=GroqProvider(api_key=GROQ_API_KEY),
)
drink_type_values = [d.value for d in DrinkType]
units_values = [u.value for u in Unit]

mixology_agent: Agent[None, DrinkAIResult] = Agent(
    model=llm_model,
    system_prompt=(
        "You are a professional mixologist assistant. "
        "Given a list of ingredient names, generate a creative and well-balanced drink recipe. "
        "Only use ingredients that are included in the provided list. "
        "Do not add any ingredients in the instructions or recipe that are not present in the ingredients list. "
        "If the ingredients are insufficient to create a proper drink, return an ErrorResponse object "
        "with a helpful error_message explaining why.\n\n"
        "Return a valid DrinkRecipe object with:\n"
        "- A creative, descriptive drink name that matches the drink and would return a relevant drink image when searched.\n"
        "- Logical and realistic ingredients with:\n"
        "   - amount: float (e.g., 50.0)\n"
        "   - unit: EXACTLY one of these values: " + ", ".join(units_values) + ".\n"
        "- Clear, step-by-step instructions.\n"
        "- alcoholContent set to true if any ingredient contains alcohol.\n"
        "- A fitting type using EXACTLY one of these values: "
        + ", ".join(drink_type_values)
        + ".\n"
        "- isFavorite should always be false.\n"
        "- id and imageId is not relevant, so set it to None.\n"
        "- Do not make up or invent ingredients; only use the provided list (or a subset if necessary).\n"
        "- Make sure the drink is balanced and pleasant—avoid combinations that are likely to be unpleasant or gross."
    ),
    output_type=DrinkAIResult,
    deps_type=None,
)


# --- Utility Function ---
def get_pexels_images(name: str, count: int, page: int):
    params = {"query": name, "per_page": count, "page": page}
    response = httpx.get(PEXELS_BASE_URL, headers=pexels_headers, params=params)
    if response.status_code != 200:
        return ErrorResponse(
            error_code=response.status_code,
            message="Pexels API error: " + response.text,
        )
    photos = response.json().get("photos", [])
    return [photo["id"] for photo in photos]


@mixology_agent.output_validator
async def validate_ai_output(
    ctx: RunContext[None], result: DrinkAIResult
) -> DrinkAIResult:

    if isinstance(result, ErrorResponse):
        if not result.error_code or not result.message.strip():
            return ErrorResponse(
                error_code=500,
                message="Hmm, the AI had a hiccup and didn’t explain why. Let’s give it another shot!",
            )
        return result

    return result


# --- Routes ---
@app.get("/drinks", response_model=List[DrinkRecipe])
def list_all_drinks():
    return drink_db


@app.post("/drinks/images", response_model=List[int])
def fetch_drink_images(request: ImageSearchRequest):
    result = get_pexels_images(request.name, request.count, request.page)

    if isinstance(result, ErrorResponse):
        raise HTTPException(
            status_code=result.error_code,
            detail="Looks like our image search is a bit thirsty! No photo this time, but the recipe is still delicious.",
        )

    return result


@app.post("/drinks", response_model=DrinkRecipe)
def add_new_drink(drink: DrinkRecipe):
    drink.id = uuid.uuid4()
    drink_db.append(drink)
    return drink


@app.patch("/drinks/{drink_id}/favorite", response_model=DrinkRecipe)
def toggle_favorite_status(drink_id: uuid.UUID):
    for drink in drink_db:
        if drink.id == drink_id:
            drink.isFavorite = not drink.isFavorite
            return drink
    raise HTTPException(
        status_code=404,
        detail="Hmm, we couldn’t find that drink. Maybe it got shaken, not stirred?",
    )


@app.get("/drinks/random", response_model=DrinkRecipe)
def get_random_drink():
    return random.choice(drink_db)


@app.post("/drinks/generate", response_model=DrinkRecipe)
def generate_drink_from_ingredients(ingredients: List[str]):
    ingredient_str = ", ".join(ingredients)
    user_prompt = f"Create a drink using the following ingredients: {ingredient_str}."

    ai_result = mixology_agent.run_sync(user_prompt)

    if isinstance(ai_result.output, ErrorResponse):
        raise HTTPException(status_code=422, detail=ai_result.output.message)

    new_drink = ai_result.output

    result = get_pexels_images(new_drink.name, 1, 1)

    if isinstance(result, ErrorResponse):
        new_drink.imageId = None
    elif not result:
        new_drink.imageId = None
    else:
        new_drink.imageId = result[0]

    new_drink.id = uuid.uuid4()
    drink_db.append(new_drink)

    return new_drink
