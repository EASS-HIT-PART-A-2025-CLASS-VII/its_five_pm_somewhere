# from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

# from app.main import app
import uuid

from app.models import Ingredient, DrinkRecipe

from app.main import app, mixology_agent, get_pexels_images
from fastapi.testclient import TestClient
from app.main import drink_db

client = TestClient(app)

mock_drink = DrinkRecipe(
    id="0",
    name="Mocktail Delight",
    ingredients=[
        Ingredient(name="apple juice", amount="50ml"),
        Ingredient(name="lime", amount="1 slice"),
        Ingredient(name="mint", amount="5 leaves"),
    ],
    instructions=["Mix all ingredients", "Shake well", "Serve over ice"],
    alcoholContent=False,
    type="Mocktail",
    imageUrl="0",
    isFavorite=False,
)


class MockResult:
    output = mock_drink


# @app.get("/drinks")
def test_list_all_drinks_success():
    response = client.get("/drinks")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


# @app.post("/drinks/images")
def test_fetch_images_success():
    payload = {"name": "mojito", "count": 2, "page": 1}

    response = client.post("/drinks/images", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) == payload["count"]
    for url in data:
        assert isinstance(url, str)
        assert url.startswith("https://images.pexels.com/photos")


# @app.post("/drinks")
def test_add_new_drink_success():
    new_drink = {
        "id": "0",  # Will be overwritten anyway
        "name": "Sunset Twist",
        "ingredients": [
            {"name": "Orange juice", "amount": "50ml"},
            {"name": "Grenadine", "amount": "10ml"},
        ],
        "instructions": ["Pour orange juice", "Add grenadine", "Serve with ice"],
        "alcoholContent": False,
        "type": "Mocktail",
        "imageUrl": "https://example.com/image.jpg",
        "isFavorite": False,
    }

    response = client.post("/drinks", json=new_drink)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Sunset Twist"
    assert data["id"] != "0"


def test_add_new_drink_missing_fields_error():
    broken_drink = {
        "id": "0",
        "name": "",
        "ingredients": [],
        "instructions": [],
        "alcoholContent": True,
        "type": "",
        "imageUrl": "invalid-url",
        "isFavorite": False,
    }
    response = client.post("/drinks", json=broken_drink)
    assert response.status_code == 400
    assert "Looks like some details are missing" in response.text


# @app.patch("/drinks/{drink_id}/favorite")
def test_toggle_favorite_status_success():
    # Save current state of drink_db
    original_drinks = drink_db.copy()

    try:
        # Setup: create and insert a mock drink
        drink_id = str(uuid.uuid4())
        drink = DrinkRecipe(
            id=drink_id,
            name="Test Drink",
            ingredients=[
                Ingredient(name="Rum", amount="50ml"),
                Ingredient(name="Mint", amount="5 leaves"),
            ],
            instructions=["Shake it well!"],
            alcoholContent=True,
            type="Cocktail",
            imageUrl="https://example.com/image.jpg",
            isFavorite=False,
        )
        drink_db.append(drink)

        # Act: toggle favorite status
        response = client.patch(f"/drinks/{drink_id}/favorite")
        assert response.status_code == 200

        # Assert
        data = response.json()
        try:
            returned_drink = DrinkRecipe(**data)
        except ValidationError as e:
            pytest.fail(f"Response doesn't match DrinkRecipe model: {e}")

        assert returned_drink.id == drink_id
        assert returned_drink.isFavorite is True  # it was False before

    finally:
        # Restore original state
        drink_db.clear()
        drink_db.extend(original_drinks)


def test_toggle_favorite_error():
    fake_id = str(uuid.uuid4())
    response = client.patch(f"/drinks/{fake_id}/favorite")
    assert response.status_code == 404
    assert "couldn’t find that drink" in response.text


# @app.get("/drinks/random")
def test_get_random_drink_success():
    # Save current state of drink_db
    original_drinks = drink_db.copy()

    try:
        # Clear and add only our test drink
        drink_db.clear()
        test_drink = DrinkRecipe(
            id=str(uuid.uuid4()),
            name="Test Drink",
            ingredients=[
                Ingredient(name="Rum", amount="50ml"),
                Ingredient(name="Mint", amount="5 leaves"),
            ],
            instructions=["Shake it well!"],
            alcoholContent=True,
            type="Cocktail",
            imageUrl="https://example.com/image.jpg",
            isFavorite=False,
        )
        drink_db.append(test_drink)

        # Test the endpoint
        response = client.get("/drinks/random")
        assert response.status_code == 200

        # Validate response structure
        data = response.json()
        try:
            returned_drink = DrinkRecipe(**data)
        except ValidationError as e:
            pytest.fail(f"Response doesn't match DrinkRecipe model: {e}")

        # Since we cleared the DB, we should get our test drink
        assert returned_drink.id == test_drink.id
        assert returned_drink.name == test_drink.name

        # Alternatively, if you can't guarantee a clean DB:
        # assert any(d.id == returned_drink.id for d in drink_db)

    finally:
        # Restore original state
        drink_db.clear()
        drink_db.extend(original_drinks)


# @app.post("/drinks/generate")
def test_generate_drink_success():
    # Save current state of drink_db
    original_drinks = drink_db.copy()

    try:
        # Create a mock AI result object that matches what mixology_agent returns
        mock_ai_result = MockResult()

        mock_image_url = "https://images.pexels.com/photos/mock-image.jpg"

        # Mock dependencies
        with patch.object(
            mixology_agent, "run_sync", return_value=mock_ai_result
        ), patch("app.main.get_pexels_images", return_value=[mock_image_url]):

            # Call endpoint
            response = client.post(
                "/drinks/generate", json=["apple juice", "lime", "mint"]
            )

            # Verify response
            assert response.status_code == 200
            data = response.json()

            # Validate response structure (using model_dump for Pydantic v2)
            try:
                returned_drink = DrinkRecipe(**data)
            except ValidationError as e:
                pytest.fail(f"Invalid drink structure: {e}")

            # Verify content
            assert returned_drink.name == "Mocktail Delight"
            assert returned_drink.imageUrl == mock_image_url
            assert returned_drink.id != "0"  # Should have been assigned a real UUID
            assert len(returned_drink.ingredients) == 3
            assert any(
                ing.name.lower() == "apple juice" for ing in returned_drink.ingredients
            )

            # Verify the drink was added to the database
            assert any(d.id == returned_drink.id for d in drink_db)

    finally:
        # Restore original state
        drink_db.clear()
        drink_db.extend(original_drinks)


def test_generate_drink_from_ingredients_error():
    # This is likely to error if the LLM returns ErrorResponse
    response = client.post("/drinks/generate", json=["glue", "paper"])
    assert response.status_code in [200, 422]  # Depending on AI
