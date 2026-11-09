"""Stage 2 tests; keep Stage 1 tests and add your own regressions."""
import unittest
from bakery import Bakery


class Stage2PublicTests(unittest.TestCase):
    def test_order_interface(self):
        b = Bakery(orders=[{'id': 'A', 'product_id': 'loaf', 'quantity': 1, 'collection_week': 1}])
        demand = {'loaf': 1, 'bun': 0, 'slice': 0}
        decision = {'workforce': 1, 'sales': {'loaf': 1, 'bun': 0, 'slice': 0},
                    'purchases': {'flour': 0, 'butter': 0, 'fruit': 0}}
        r = b.step(decision, demand)
        self.assertEqual(r['fulfilled_order_ids'], ['A'])
        self.assertEqual(b.order_book.orders[0].status, 'fulfilled')

    def test_legacy_scenario_has_empty_orders(self):
        self.assertEqual(Bakery().order_book.orders, [])
