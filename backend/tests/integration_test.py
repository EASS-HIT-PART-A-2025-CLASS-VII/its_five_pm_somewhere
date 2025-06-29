import uuid
from app.models import Ingredient, DrinkRecipe, DrinkType, Unit
from app.main import app
from fastapi.testclient import TestClient
from app.main import drink_db

client = TestClient(app)


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
    for image_id in data:
        assert isinstance(image_id, int)
        assert image_id > 0


# @app.post("/drinks")
def test_add_new_drink_success():
    new_drink = {
        "name": "Sunset Twist",
        "ingredients": [
            {"name": "Orange juice", "amount": 50.0, "unit": Unit.MILLILITER},
            {"name": "Grenadine", "amount": 10.0, "unit": Unit.MILLILITER},
        ],
        "instructions": ["Pour orange juice", "Add grenadine", "Serve with ice"],
        "alcoholContent": False,
        "type": DrinkType.MOCKTAIL,
        "imageId": 11481550,
        "isFavorite": False,
    }

    response = client.post("/drinks", json=new_drink)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Sunset Twist"
    assert uuid.UUID(data["id"])


def test_add_new_drink_missing_fields_error():
    broken_drink = {
        "name": "",
        "ingredients": [],
        "instructions": [],
        "alcoholContent": True,
        "type": "",
        "imageId": 0,
        "isFavorite": False,
    }
    response = client.post("/drinks", json=broken_drink)
    assert response.status_code == 422
    data = response.json()
    assert any(
        "String should have at least 2 characters" in str(msg) for msg in data["detail"]
    )
    assert any("List should have at least 1 item" in str(msg) for msg in data["detail"])


# @app.patch("/drinks/{drink_id}/favorite")
def test_toggle_favorite_status_success():
    original_drinks = drink_db.copy()

    try:
        drink_id = uuid.uuid4()
        drink = DrinkRecipe(
            id=drink_id,
            name="Test Drink",
            ingredients=[
                Ingredient(name="Rum", amount=50.0, unit=Unit.MILLILITER),
                Ingredient(name="Mint", amount=5.0, unit=Unit.PIECE),
            ],
            instructions=["Shake it well!"],
            alcoholContent=True,
            type=DrinkType.COCKTAIL,
            imageId=11481550,
            isFavorite=False,
        )
        drink_db.append(drink)

        response = client.patch(f"/drinks/{drink_id}/favorite")
        assert response.status_code == 200

        data = response.json()
        returned_drink = DrinkRecipe(**data)

        assert returned_drink.id == drink_id
        assert returned_drink.isFavorite is True

    finally:
        drink_db.clear()
        drink_db.extend(original_drinks)


def test_toggle_favorite_error():
    fake_id = uuid.uuid4()
    response = client.patch(f"/drinks/{fake_id}/favorite")
    assert response.status_code == 404
    assert "couldn’t find that drink" in response.text


# @app.get("/drinks/random")
def test_get_random_drink_success():
    original_drinks = drink_db.copy()

    try:
        drink_db.clear()
        test_drink = DrinkRecipe(
            id=uuid.uuid4(),
            name="Test Drink",
            ingredients=[
                Ingredient(name="Rum", amount=50.0, unit=Unit.MILLILITER),
                Ingredient(name="Mint", amount=5.0, unit=Unit.PIECE),
            ],
            instructions=["Shake it well!"],
            alcoholContent=True,
            type=DrinkType.COCKTAIL,
            imageId=11481550,
            isFavorite=False,
        )
        drink_db.append(test_drink)

        response = client.get("/drinks/random")
        assert response.status_code == 200

        data = response.json()
        returned_drink = DrinkRecipe(**data)

        assert returned_drink.id == test_drink.id
        assert returned_drink.name == test_drink.name

    finally:
        drink_db.clear()
        drink_db.extend(original_drinks)


# @app.post("/drinks/generate")
def test_generate_drink_from_ingredients_error():
    response = client.post("/drinks/generate", json=["glue", "paper"])
    assert response.status_code in [200, 422]
