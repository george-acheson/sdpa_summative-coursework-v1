"""Validation helpers for simulation inputs."""
from ingredient import INGREDIENTS
from product import PRODUCTS


def integer(value, name, minimum=0, maximum=None):
    """Reject booleans, non-integers and out-of-range values."""
    if type(value) is not int or value < minimum:
        raise ValueError(f"{name} must be an integer >= {minimum}")
    if maximum is not None and value > maximum:
        raise ValueError(f"{name} must be <= {maximum}")
    return value


def quantities(value, keys, name, maximum=None):
    """Validate a complete mapping and return an independent copy."""
    if not isinstance(value, dict) or set(value) != set(keys):
        raise ValueError(f"{name} must contain exactly {', '.join(keys)}")
    return {key: integer(value[key], f"{name}.{key}", maximum=maximum)
            for key in keys}


def validate_decision(decision, demand):
    """Validate decision shape and walk-in demand without changing state."""
    if not isinstance(decision, dict) or set(decision) != {"workforce", "sales", "purchases"}:
        raise ValueError("decision needs workforce, sales and purchases")
    workforce = integer(decision["workforce"], "workforce", 1, 3)
    sales = quantities(decision["sales"], PRODUCTS, "sales")
    purchases = quantities(decision["purchases"], INGREDIENTS, "purchases")
    demand = quantities(demand, PRODUCTS, "demand", 200)
    if any(sales[p] > demand[p] for p in PRODUCTS):
        raise ValueError("sales exceed demand")
    return workforce, sales, purchases
