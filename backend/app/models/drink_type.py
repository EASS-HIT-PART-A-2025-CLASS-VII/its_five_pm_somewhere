from enum import Enum


class DrinkType(str, Enum):
    COCKTAIL = "Cocktail"
    MOCKTAIL = "Mocktail"
    SHOT = "Shot"
    SMOOTHIE = "Smoothie"
    MILKSHAKE = "Milkshake"
    PUNCH = "Punch"
    COFFEE_DRINK = "Coffee Drink"
    TEA_DRINK = "Tea Drink"
    HOT_CHOCOLATE = "Hot Chocolate"
