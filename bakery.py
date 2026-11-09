"""Weekly trading calculations, independent of terminal input and output."""
from copy import deepcopy
from ingredient import INGREDIENTS
from product import PRODUCTS
from validation import integer, validate_decision
from stock import Stock


class Bakery:
    """A bounded simulation with stock, cash and completed weekly records."""
    # Fixed operating rates, in pence.
    WEEKLY_RENT = 5000
    COST_PER_WORKER = 10000

    def __init__(self, duration=6, initial_cash=100000, initial_stock=None):
        self.duration = integer(duration, "duration", 1, 12)
        self._cash = integer(initial_cash, "initial_cash")
        self.stock = Stock(initial_stock)
        self.week = 1
        self.bankrupt = False
        self._history = []

    def get_stock(self):
        """Return the live stock dictionary; copy it to retain a snapshot."""
        return self.stock.quantities

    def get_cash(self):
        """Return the current cash balance in pence."""
        return self._cash

    def get_history(self):
        """Return independent record snapshots."""
        return deepcopy(self._history)

    def is_stopped(self):
        """Whether another trading week is forbidden."""
        return self.bankrupt or self.week > self.duration

    def step(self, decision, demand):
        """Validate and apply one complete week, returning a record dictionary."""
        if self.is_stopped():
            raise ValueError("simulation has stopped")
        workforce, sales, purchases = validate_decision(decision, demand)
        opening_stock = dict(self.stock.quantities)
        consumed = {k: sum(PRODUCTS[p].quantity_for(INGREDIENTS[k]) * sales[p] for p in PRODUCTS)
                    for k in INGREDIENTS}
        minutes = sum(PRODUCTS[p].minutes * sales[p] for p in PRODUCTS)
        if any(PRODUCTS[p].quantity_for(INGREDIENTS[k]) * sales[p] > opening_stock[k]
               for p in PRODUCTS for k in INGREDIENTS):
            raise ValueError("insufficient ingredients")
        if minutes > workforce * 600:
            raise ValueError("insufficient labour")
        remaining = {k: opening_stock[k] - consumed[k] for k in INGREDIENTS}
        self.stock.update(remaining)
        revenue = sum(PRODUCTS[p].price * sales[p] for p in PRODUCTS)
        wages = workforce * self.COST_PER_WORKER if revenue else 0
        rent = self.WEEKLY_RENT
        cash_after_charges = self._cash + revenue - wages - rent
        bankrupt = cash_after_charges <= 0
        discarded = dict.fromkeys(INGREDIENTS, 0)
        purchased = dict.fromkeys(INGREDIENTS, 0)
        purchases_cost = 0
        if not bankrupt:
            discarded = self.stock.discarded(remaining)
            remaining = {k: remaining[k] - discarded[k] for k in INGREDIENTS}
            if any(remaining[k] + purchases[k] > INGREDIENTS[k].capacity for k in INGREDIENTS):
                raise ValueError("purchase exceeds capacity")
            purchases_cost = sum(INGREDIENTS[k].price * purchases[k] for k in INGREDIENTS)
            if purchases_cost > cash_after_charges:
                raise ValueError("purchase is unaffordable")
            purchased = purchases
            remaining = {k: remaining[k] + purchased[k] for k in INGREDIENTS}
        opening_cash = self._cash
        self._cash = cash_after_charges - purchases_cost
        self.stock.update(remaining)
        self.bankrupt = bankrupt
        record = {
            "week": self.week, "opening_cash": opening_cash, "closing_cash": self._cash,
            "workforce": workforce, "revenue": revenue, "wages": wages, "rent": rent,
            "purchases_cost": purchases_cost, "sales": sales,
            "opening_stock": opening_stock, "consumed": consumed,
            "discarded": discarded, "purchased": purchased,
            "closing_stock": self.stock.quantities, "minutes_used": minutes,
            "bankrupt": bankrupt,
        }
        self._history.append(record)
        self.week += 1
        return deepcopy(record)
