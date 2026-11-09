"""Ingredient stock and weekly losses."""
from ingredient import INGREDIENTS
from validation import quantities


class Stock:
    """Store one bakery's ingredient quantities."""
    _shared = {k: item.capacity for k, item in INGREDIENTS.items()}

    def __init__(self, initial=None):
        values = {k: item.capacity for k, item in INGREDIENTS.items()} if initial is None else initial
        if initial is None:
            self.quantities = self._shared
        else:
            self.quantities = quantities(values, INGREDIENTS, "stock")
        if any(self.quantities[k] > INGREDIENTS[k].capacity for k in INGREDIENTS):
            raise ValueError("initial stock exceeds capacity")

    def update(self, remaining):
        """Update the existing stock quantities from a dictionary."""
        for ingredient in remaining:
            self.quantities[ingredient] = remaining[ingredient]

    def discarded(self, remaining):
        """Return the whole units lost, rounded upwards."""
        discarded = {}
        for ingredient in INGREDIENTS:
            discarded[ingredient] = (remaining[ingredient] * INGREDIENTS[ingredient].loss_percentage) // 100
        return discarded
