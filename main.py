"""Interactive trading and file replay entry points."""
import argparse
import json
from pathlib import Path
from ingredient import INGREDIENTS
from product import PRODUCTS
from validation import integer
from replay import load_json, replay
from bakery import Bakery


def prompt_integer(label, minimum=0, maximum=None, default=None):
    """Repeat a prompt until a permitted integer is entered."""
    while True:
        raw = input(label).strip()
        try:
            value = default if raw == "" and default is not None else int(raw)
            return integer(value, label, minimum, maximum)
        except ValueError:
            print("Please enter a valid integer in the stated range.")


def display_weekly_summary(record):
    """Print a weekly summary of one record; this does not display stored history."""
    print(json.dumps(record, indent=2, sort_keys=True))


def display_bakery_state(bakery, demand):
    """Show live resources and the published trading rules before a decision."""
    print(f"\nWeek {bakery.week} of {bakery.duration}; cash {bakery.get_cash()} pence")
    print("Current inventory (units):")
    print(f"{'Ingredient':<12}{'In stock':>10}{'Capacity':>10}{'Free space':>12}{'Buy price (p)':>15}{'Weekly loss':>14}")
    for name, item in INGREDIENTS.items():
        quantity = bakery.stock.quantities[name]
        print(f"{name:<12}{quantity:>10}{item.capacity:>10}{item.capacity - quantity:>12}"
              f"{item.price:>15}{str(item.loss_percentage) + '%':>14}")
    print(f"Sales use current stock. Each employee provides 600 minutes and costs {Bakery.COST_PER_WORKER} pence/week.")
    print(f"Weekly rent: {Bakery.WEEKLY_RENT} pence. Product requirements per unit:")
    for name, product in PRODUCTS.items():
        recipe = ', '.join(f"{product.quantity_for(item)} {key}"
                           for key, item in INGREDIENTS.items() if product.quantity_for(item))
        print(f"  {name}: {recipe}; {product.minutes} minutes; sale price {product.price} pence; demand {demand[name]}")
    print("Purchases arrive AFTER sales, wages/rent and spoilage; they cannot supply this week's sales.")
    print("Purchase room = capacity - stock remaining after sales and spoilage. Cash must also cover purchases.")
    print("Flour has no spoilage: when its store is full, sell products using flour before buying more.")
    print("Enter 0 for any sales or purchases you do not want to make.")


def interactive():
    """Run a default-demand simulation with replaceable weekly decisions."""
    duration = prompt_integer("Weeks (1-12, blank = 6): ", 1, 12, 6)
    bakery = Bakery(duration)
    demand = {"loaf": 100, "bun": 80, "slice": 60}
    while not bakery.is_stopped():
        display_bakery_state(bakery, demand)
        decision = {
            "workforce": prompt_integer("Employees (1-3): ", 1, 3),
            "sales": {p: prompt_integer(f"Sell {p}: ") for p in PRODUCTS},
            "purchases": {k: prompt_integer(f"Buy {k} units: ") for k in INGREDIENTS},
        }
        try:
            display_weekly_summary(bakery.step(decision, demand))
        except ValueError as error:
            print(f"Decision rejected: {error}. Replace the decision for this week.")
    return bakery


def main(argv=None):
    """Run the CLI; return a process exit status."""
    parser = argparse.ArgumentParser(description="Community bakery simulator")
    parser.add_argument("--scenario")
    parser.add_argument("--decisions")
    parser.add_argument("--output")
    args = parser.parse_args(argv)
    if any((args.scenario, args.decisions, args.output)) and not all(
            (args.scenario, args.decisions, args.output)):
        parser.error("--scenario, --decisions and --output must be supplied together")
    try:
        if args.scenario:
            records = replay(load_json(args.scenario), load_json(args.decisions))
            output = Path(args.output)
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(json.dumps(records, indent=2, sort_keys=True) + "\n", encoding="utf-8")
            print(f"Wrote {len(records)} weekly records to {output}")
        else:
            interactive()
    except (ValueError, OSError) as error:
        print(f"Error: {error}")
        return 1
    except (EOFError, KeyboardInterrupt):
        print("\nSimulation cancelled.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
