"""Load JSON scenarios and replay decisions deterministically."""
import json
from pathlib import Path
from product import PRODUCTS
from validation import integer, quantities
from bakery import Bakery


def load_json(path):
    """Read a JSON value using UTF-8."""
    return json.loads(Path(path).read_text(encoding="utf-8"))


def from_scenario(scenario):
    """Validate a scenario and return a fresh bakery and copied demands."""
    if not isinstance(scenario, dict):
        raise ValueError("scenario must be an object")
    allowed = {"duration", "demands", "initial_cash", "initial_stock"}
    if set(scenario) - allowed or not {"duration", "demands"} <= set(scenario):
        raise ValueError("invalid scenario fields")
    duration = integer(scenario["duration"], "duration", 1, 12)
    demands = scenario["demands"]
    if not isinstance(demands, list) or len(demands) != duration:
        raise ValueError("one demand object is required for each week")
    demands = [quantities(d, PRODUCTS, "demand", 200) for d in demands]
    bakery = Bakery(duration, scenario.get("initial_cash", 100000),
                    scenario.get("initial_stock"))
    return bakery, demands


def replay(scenario, decisions):
    """Return records; ignore remaining decisions after bankruptcy."""
    bakery, demands = from_scenario(scenario)
    if not isinstance(decisions, list) or len(decisions) != bakery.duration:
        raise ValueError("one decision object is required for each week")
    for decision, demand in zip(decisions, demands):
        bakery.step(decision, demand)
        if bakery.is_stopped():
            break
    return bakery.get_history()
