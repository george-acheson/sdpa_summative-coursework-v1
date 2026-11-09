"""One ingredient and the quantity needed for a product recipe."""
from ingredient import Ingredient


class RecipeItem:
    """Associate an ingredient definition with units required per product."""
    def __init__(self, ingredient, quantity):
        if not isinstance(ingredient, Ingredient):
            raise ValueError("ingredient must be an Ingredient")
        if type(quantity) is not int or quantity <= 0:
            raise ValueError("recipe quantity must be a positive integer")
        self.ingredient = ingredient
        self.quantity = quantity
