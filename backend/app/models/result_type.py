from typing import Union
from .drink_recipe import DrinkRecipe
from .error_response import ErrorResponse

DrinkAIResult = Union[DrinkRecipe, ErrorResponse]
