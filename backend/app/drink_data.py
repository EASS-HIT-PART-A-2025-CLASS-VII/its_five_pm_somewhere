from typing import List
from app.models import Ingredient, DrinkRecipe, DrinkType, Unit

# --- In-Memory Store ---
drink_db: List[DrinkRecipe] = [
    DrinkRecipe(
        name="Mojito",
        ingredients=[
            Ingredient(name="White Rum", amount=50, unit=Unit.MILLILITER),
            Ingredient(name="Mint Leaves", amount=10, unit=Unit.PIECE),
            Ingredient(name="Lime", amount=0.5, unit=Unit.PIECE),
            Ingredient(name="Sugar", amount=2, unit=Unit.TEASPOON),
            Ingredient(name="Club Soda", amount=1, unit=Unit.TOP_UP),
        ],
        instructions=[
            "Muddle mint leaves and sugar in a glass.",
            "Add lime juice and rum.",
            "Fill the glass with ice and top it up with club soda.",
            "Stir gently and garnish with a mint sprig.",
        ],
        alcoholContent=True,
        type=DrinkType.COCKTAIL,
        imageUrl="https://images.pexels.com/photos/1187766/pexels-photo-1187766.jpeg?auto=compress&cs=tinysrgb&h=350",
        isFavorite=False,
    ),
    DrinkRecipe(
        name="Martini",
        ingredients=[
            Ingredient(name="Gin", amount=60, unit=Unit.MILLILITER),
            Ingredient(name="Dry Vermouth", amount=10, unit=Unit.MILLILITER),
            Ingredient(name="Olive", amount=1, unit=Unit.PIECE),
        ],
        instructions=[
            "Pour gin and dry vermouth into a mixing glass.",
            "Fill with ice and stir for 20-30 seconds.",
            "Strain into a chilled martini glass and garnish with an olive.",
        ],
        alcoholContent=True,
        type=DrinkType.COCKTAIL,
        imageUrl="https://images.pexels.com/photos/2531186/pexels-photo-2531186.jpeg?auto=compress&cs=tinysrgb&h=350",
        isFavorite=False,
    ),
    DrinkRecipe(
        name="Gin and Tonic",
        ingredients=[
            Ingredient(name="Gin", amount=50, unit=Unit.MILLILITER),
            Ingredient(name="Tonic Water", amount=1, unit=Unit.TOP_UP),
            Ingredient(name="Lime", amount=0.25, unit=Unit.PIECE),
        ],
        instructions=[
            "Pour gin into a glass filled with ice.",
            "Top it up with tonic water.",
            "Garnish with a lime wedge.",
        ],
        alcoholContent=True,
        type=DrinkType.COCKTAIL,
        imageUrl="https://images.pexels.com/photos/616836/pexels-photo-616836.jpeg?auto=compress&cs=tinysrgb&h=350",
        isFavorite=False,
    ),
    DrinkRecipe(
        name="Old Fashioned",
        ingredients=[
            Ingredient(name="Bourbon", amount=50, unit=Unit.MILLILITER),
            Ingredient(name="Sugar", amount=1, unit=Unit.TEASPOON),
            Ingredient(name="Angostura Bitters", amount=2, unit=Unit.DASH),
            Ingredient(name="Orange Peel", amount=1, unit=Unit.PIECE),
        ],
        instructions=[
            "Muddle the sugar and bitters in a glass.",
            "Add bourbon and stir with ice.",
            "Garnish with an orange peel.",
        ],
        alcoholContent=True,
        type=DrinkType.COCKTAIL,
        imageUrl="https://images.pexels.com/photos/31589567/pexels-photo-31589567.jpeg?auto=compress&cs=tinysrgb&h=350",
        isFavorite=False,
    ),
    DrinkRecipe(
        name="Piña Colada",
        ingredients=[
            Ingredient(name="White Rum", amount=50, unit=Unit.MILLILITER),
            Ingredient(name="Coconut Cream", amount=30, unit=Unit.MILLILITER),
            Ingredient(name="Pineapple Juice", amount=90, unit=Unit.MILLILITER),
            Ingredient(name="Pineapple Slice", amount=1, unit=Unit.PIECE),
        ],
        instructions=[
            "Blend all ingredients with ice.",
            "Pour into a glass and garnish with a pineapple slice.",
        ],
        alcoholContent=True,
        type=DrinkType.COCKTAIL,
        imageUrl="https://images.pexels.com/photos/8944950/pexels-photo-8944950.jpeg?auto=compress&cs=tinysrgb&h=350",
        isFavorite=False,
    ),
    DrinkRecipe(
        name="Margarita",
        ingredients=[
            Ingredient(name="Tequila", amount=50, unit=Unit.MILLILITER),
            Ingredient(name="Lime Juice", amount=30, unit=Unit.MILLILITER),
            Ingredient(name="Triple Sec", amount=20, unit=Unit.MILLILITER),
            Ingredient(name="Salt", amount=1, unit=Unit.TOP_UP),
        ],
        instructions=[
            "Rub a lime wedge around the rim of a glass and dip it in salt.",
            "Shake tequila, lime juice, and triple sec with ice.",
            "Strain into the prepared glass.",
        ],
        alcoholContent=True,
        type=DrinkType.COCKTAIL,
        imageUrl="https://images.pexels.com/photos/1590154/pexels-photo-1590154.jpeg?auto=compress&cs=tinysrgb&h=350",
        isFavorite=False,
    ),
    DrinkRecipe(
        name="Cosmopolitan",
        ingredients=[
            Ingredient(name="Vodka", amount=45, unit=Unit.MILLILITER),
            Ingredient(name="Triple Sec", amount=15, unit=Unit.MILLILITER),
            Ingredient(name="Lime Juice", amount=15, unit=Unit.MILLILITER),
            Ingredient(name="Cranberry Juice", amount=30, unit=Unit.MILLILITER),
        ],
        instructions=[
            "Shake all ingredients with ice.",
            "Strain into a chilled martini glass.",
        ],
        alcoholContent=True,
        type=DrinkType.COCKTAIL,
        imageUrl="https://images.pexels.com/photos/31623993/pexels-photo-31623993.jpeg?auto=compress&cs=tinysrgb&h=350",
        isFavorite=False,
    ),
    DrinkRecipe(
        name="Bloody Mary",
        ingredients=[
            Ingredient(name="Vodka", amount=50, unit=Unit.MILLILITER),
            Ingredient(name="Tomato Juice", amount=100, unit=Unit.MILLILITER),
            Ingredient(name="Lemon Juice", amount=15, unit=Unit.MILLILITER),
            Ingredient(name="Tabasco Sauce", amount=2, unit=Unit.DASH),
            Ingredient(name="Worcestershire Sauce", amount=2, unit=Unit.DASH),
        ],
        instructions=[
            "Shake all ingredients with ice.",
            "Strain into a tall glass and garnish with a celery stick.",
        ],
        alcoholContent=True,
        type=DrinkType.COCKTAIL,
        imageUrl="https://images.pexels.com/photos/7376796/pexels-photo-7376796.jpeg?auto=compress&cs=tinysrgb&h=350",
        isFavorite=False,
    ),
    DrinkRecipe(
        name="Mai Tai",
        ingredients=[
            Ingredient(name="Rum", amount=30, unit=Unit.MILLILITER),
            Ingredient(name="Orange Curaçao", amount=15, unit=Unit.MILLILITER),
            Ingredient(name="Orgeat Syrup", amount=15, unit=Unit.MILLILITER),
            Ingredient(name="Lime Juice", amount=30, unit=Unit.MILLILITER),
            Ingredient(name="Mint Leaves", amount=2, unit=Unit.PIECE),
        ],
        instructions=[
            "Shake all ingredients with ice.",
            "Strain into a glass filled with crushed ice and garnish with mint leaves.",
        ],
        alcoholContent=True,
        type=DrinkType.COCKTAIL,
        imageUrl="https://images.pexels.com/photos/11481550/pexels-photo-11481550.jpeg?auto=compress&cs=tinysrgb&h=350",
        isFavorite=False,
    ),
    DrinkRecipe(
        name="Whiskey Sour",
        ingredients=[
            Ingredient(name="Whiskey", amount=50, unit=Unit.MILLILITER),
            Ingredient(name="Lemon Juice", amount=25, unit=Unit.MILLILITER),
            Ingredient(name="Simple Syrup", amount=15, unit=Unit.MILLILITER),
            Ingredient(name="Egg White", amount=1, unit=Unit.PIECE),
        ],
        instructions=[
            "Shake all ingredients without ice to emulsify.",
            "Add ice and shake again.",
            "Strain into a glass and garnish with a cherry.",
        ],
        alcoholContent=True,
        type=DrinkType.COCKTAIL,
        imageUrl="https://images.pexels.com/photos/28834354/pexels-photo-28834354.jpeg?auto=compress&cs=tinysrgb&h=350",
        isFavorite=False,
    ),
]
