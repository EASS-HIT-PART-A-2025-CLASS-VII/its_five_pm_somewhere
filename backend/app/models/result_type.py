from typing import Union
from .drink_recipe import DrinkRecipe
from .error_response import ErrorResponse

# Unified result type for validation
DrinkAIResult = Union[DrinkRecipe, ErrorResponse]
