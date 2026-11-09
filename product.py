"""Products composed of recipe items."""
from ingredient import INGREDIENTS
from recipeitem import RecipeItem


class Product:
    """Recipe items, preparation minutes and sale price in pence."""
    def __init__(self, recipe_items, minutes, price):
        self.recipe_items = list(recipe_items)
        self.minutes = minutes
        self.price = price

    def quantity_for(self, ingredient):
        """Return units of this ingredient needed for one product, or zero."""
        quantity = 0
        for item in self.recipe_items:
            if item.ingredient is ingredient:
                quantity += item.quantity
        return quantity


PRODUCTS = {
    "loaf": Product([RecipeItem(INGREDIENTS["flour"], 4)], 6, 350),
    "bun": Product([RecipeItem(INGREDIENTS["flour"], 2),
                    RecipeItem(INGREDIENTS["butter"], 1)], 4, 250),
    "slice": Product([RecipeItem(INGREDIENTS["flour"], 2),
                      RecipeItem(INGREDIENTS["butter"], 1),
                      RecipeItem(INGREDIENTS["fruit"], 2)], 5, 400),
}
