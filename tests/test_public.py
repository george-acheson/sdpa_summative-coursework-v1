"""Tests only: consult the brief for the complete required behaviour."""
import unittest
from bakery import Bakery
from replay import replay


class PublicTests(unittest.TestCase):
    def test_construct(self):
        b = Bakery(duration=2)
        self.assertEqual(b.week, 1)
        self.assertEqual(b.get_cash(), 100000)
        self.assertFalse(b.is_stopped())

    def test_feasible_week_interface(self):
        b = Bakery(initial_stock={'flour': 100, 'butter': 20, 'fruit': 20})
        d = {'workforce': 1, 'sales': {'loaf': 1, 'bun': 0, 'slice': 0},
             'purchases': {'flour': 0, 'butter': 0, 'fruit': 0}}
        r = b.step(d, {'loaf': 10, 'bun': 10, 'slice': 10})
        self.assertEqual(r['week'], 1)
        self.assertEqual(r['revenue'], 350)
        self.assertEqual(b.week, 2)
        self.assertEqual(len(b.get_history()), 1)

    def test_replay_interface(self):
        scenario = {'duration': 1, 'demands': [{'loaf': 10, 'bun': 10, 'slice': 10}]}
        d = {'workforce': 1, 'sales': {'loaf': 1, 'bun': 0, 'slice': 0},
             'purchases': {'flour': 0, 'butter': 0, 'fruit': 0}}
        self.assertEqual(len(replay(scenario, [d])), 1)
