# Stage 1 public interface

These are required behaviours, including where the supplied implementation is defective. Tests should use these interfaces rather than private attributes. All quantities, minutes and money are integers; booleans are invalid. Mutating exported constants, recipes or bakery state directly is outside the supported interface.

## Construct and inspect

```python
from bakery import Bakery
b = Bakery(duration=6, initial_cash=100000, initial_stock=None)
```

`duration` is 1–12; `initial_cash` is non-negative. `initial_stock=None` means full capacity. Alternatively supply a complete dictionary with `flour`, `butter`, `fruit`, each non-negative and no greater than its published capacity. Input mappings must be copied. Invalid constructor values raise `ValueError`.

Call `b.get_cash()` to read the current cash balance in pence. Cash is maintained internally and changed by `step()`; there is no public cash setter. Inspect the attributes `b.week`, `b.bankrupt` and `b.stock.quantities`. Call `b.is_stopped()` to check whether the simulation has ended, and `b.get_history()` to obtain a list of independent completed-record snapshots. `week` is the next week to attempt, starting at 1 and incremented after every completed record, including a bankrupt final week. `is_stopped()` returns `True` when the bakery is bankrupt or `week > duration`. These methods must not change state. Do not assign to the inspected attributes in assessment tests.

Call `b.get_stock()` to access the bakery’s current stock dictionary containing `flour`, `butter` and `fruit` quantities, for example `b.get_stock().get("flour")`. It returns the live dictionary, not a copy: changing it would change bakery state, so callers and assessment tests must treat it as read-only. To retain a before/after snapshot, explicitly copy it with `before = b.get_stock().copy()`; assigning `before = b.get_stock()` only retains a reference to live stock. A shallow copy is sufficient because the values are integers. The method itself does not change state and is available before trading, after a rejected decision and after the simulation stops. Prefer this method to `b.stock.quantities` when inspecting stock; the existing attribute remains supported for compatibility. Returned weekly records and `get_history()` retain their separate independent-snapshot requirements.

The fixed operating rates are `Bakery.WEEKLY_RENT` (5000 pence per week) and `Bakery.COST_PER_WORKER` (10000 pence per employee per week). These are public class constants; do not modify them. The record fields `rent` and `wages` describe the charges applied for that completed week. Tests can calculate independent expected charges from the published rules.

`from stock import Stock`, `from product import Product, PRODUCTS` and `from ingredient import Ingredient, INGREDIENTS` are also supported. `Stock(initial=None)` accepts the same initial-stock mapping and exposes `quantities`. `Product(recipe_items, minutes, price)` has `recipe_items`, `minutes` and `price`. Import `RecipeItem` from `recipeitem.py`. Each `RecipeItem(ingredient, quantity)` holds an `Ingredient` reference and a positive integer quantity required per product (booleans are rejected). Recipes omit unused ingredients. `product.quantity_for(ingredient)` returns the total units required for the supplied ingredient object, or zero when absent. Pass the shared definition from `INGREDIENTS`, for example `PRODUCTS["loaf"].quantity_for(INGREDIENTS["flour"])` returns 4. The recipe quantity belongs to RecipeItem, not to the shared Ingredient. `Ingredient(capacity, price, loss_percentage)` groups each ingredient’s maximum stock, unit purchase price in pence and weekly percentage loss. `INGREDIENTS` maps ingredient names to these objects; `PRODUCTS` maps product names to Product objects. These catalogues implement the published tables; treat their definitions as fixed. These exports may help development; tests of behaviour can use Bakery alone.

## Step

```python
decision = {
    "workforce": 1,
    "sales": {"loaf": 1, "bun": 0, "slice": 0},
    "purchases": {"flour": 0, "butter": 0, "fruit": 0},
}
demand = {"loaf": 100, "bun": 80, "slice": 60}
record = b.step(decision, demand)
```

The decision must contain exactly those three fields. Sales and purchases must contain exactly their illustrated keys. Quantities are non-negative, workforce is 1–3, and each demand is 0–200. Extra or missing keys, invalid types and infeasible decisions raise `ValueError`. A stopped simulation also raises `ValueError`. Rejection leaves all state and history unchanged. Inputs must not be modified or retained as mutable live state.

A completed step returns a **weekly record** dictionary. `get_history()` retrieves the **stored weekly history** in memory. `display_weekly_summary(record)` in `main.py` prints a terminal summary of one record; it does not retrieve history or save a file. The following keys are required; later stages may add keys. Tests must not reject additional record keys.

| Keys | Meaning |
|---|---|
| `week`, `workforce` | Completed week number and employee count |
| `opening_cash`, `closing_cash` | Integer pence before and after the week |
| `revenue`, `wages`, `rent`, `purchases_cost` | Integer pence for each accounting term |
| `sales` | Walk-in units sold, by product |
| `opening_stock`, `consumed`, `discarded`, `purchased`, `closing_stock` | Complete ingredient mappings |
| `minutes_used` | Total production minutes used |
| `bankrupt` | Boolean, true exactly when charges caused negative cash |

`purchased` records actual purchases, so it contains zeros on bankruptcy. Returned records, earlier history and live stock must remain independent when another week runs or callers modify a returned record/history copy. See the brief for operation order, rounding, purchase timing and bankruptcy semantics.

## Files and replay

File replay uses two input JSON files and writes a separate output JSON file:

| File | Contents | Example |
|---|---|---|
| Scenario JSON file | One object defining duration, weekly walk-in demand and optional starting conditions; Stage 2 also allows advance orders | `data/example.json` |
| Decision JSON file | A list of the manager's weekly choices: workforce, walk-in sales and ingredient purchases | `data/example_decisions.json` |
| Output JSON file | The list of resulting weekly records | `output/run.json` |

The scenario JSON file defines the conditions; the decision JSON file defines the choices made under those conditions. These are separate inputs, not saved simulation results. When loaded into Python, JSON objects become dictionaries and JSON arrays become lists.

```python
from replay import replay, from_scenario
bakery, demands = from_scenario(scenario)
records = replay(scenario, decisions)
```

The scenario JSON file stores an object, loaded as the `scenario` dictionary, containing `duration` and `demands`. `demands` is a list with exactly one complete demand dictionary per week. Optional `initial_cash` and `initial_stock` use the constructor rules; omit them for normal initial conditions. Other fields are invalid in Stage 1. These optional initial conditions support small tests; the published prices, capacities and recipes do not change.

The decision JSON file stores the `decisions` list, with exactly `duration` entries. Each attempted entry must satisfy the step contract. Entries after bankruptcy are ignored. `replay` creates a fresh bakery, stops at bankruptcy or duration, returns its records, and does not modify either input. `from_scenario` validates all demands before returning. See `data/` for examples of both input files.

Run replay using all three options:

```sh
python3 main.py --scenario data/example.json --decisions data/example_decisions.json --output output/run.json
```

`replay.load_json(path)` reads UTF-8 JSON. The CLI creates the output directory when needed and writes the list of weekly records to the output JSON file. File or validation errors produce a nonzero exit status. Interactive mode is `python3 main.py`.

`main.main(argv=None)` returns an exit code. `prompt_integer(label, minimum=0, maximum=None, default=None)` repeats until a permitted integer is entered; an empty input uses `default` only if supplied. `interactive()` returns the completed Bakery and `display_weekly_summary(record)` prints a weekly summary of the supplied record. It does not display stored weekly history. Preserve these entry points; exact terminal prose is not assessed.

## Test layout

Keep supplied public tests unchanged. Follow [Adding and running your tests](tests/README.md) for a neutral worked example and discovery instructions.

Place regression tests in `tests/student/test_*.py` and retain `tests/student/__init__.py`. Use imports from the documented modules and `unittest.TestCase`. Fixtures may be created directly in tests or loaded relative to the test file. Do not depend on the current working directory or access private staff files. Tests must work when staff select a different implementation of these modules with this same API.

```sh
python3 -m unittest discover -s tests -v
```
