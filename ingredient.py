"""Ingredient definitions used by stock and purchasing calculations."""


class Ingredient:
    """Capacity in units, purchase price in pence and weekly loss percentage."""
    def __init__(self, capacity, price, loss_percentage):
        self.capacity = capacity
        self.price = price
        self.loss_percentage = loss_percentage


INGREDIENTS = {
    "flour": Ingredient(1000, 10, 0),
    "butter": Ingredient(400, 20, 10),
    "fruit": Ingredient(400, 15, 20),
}
