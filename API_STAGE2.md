# Stage 2 public interface additions

The advance-order rules, preservation of Stage 1 behaviour and required tests are defined in the coursework document. This reference specifies the interfaces used to implement and test them; Stage 1 interfaces remain documented in API.md.

## Construction and order input

```python
from bakery import Bakery
from order import Order
from orderbook import OrderBook
records = [{"id": "A", "product_id": "loaf", "quantity": 2, "collection_week": 1}]
bakery = Bakery(duration=6, orders=records)
```

- `Bakery` gains an optional final argument `orders=None`. Omitting it or passing `None` constructs a bakery with no orders.
- The scenario JSON file gains an optional `orders` field in its top-level object; the same field is available in the loaded scenario dictionary. If supplied, its value must be a list; an empty list is valid. An explicit `None` is invalid.
- Each order record has exactly the four fields illustrated above, with values satisfying the brief's advance-order validation rules.
- Supply the complete batch at construction. No later order additions or `add_orders()` method are required.

## Order objects and inspection

`Order(id, product_id, quantity, collection_week)` exposes these four attributes and `status`, initially `"pending"`. Invalid fields raise `ValueError`; a standalone Order accepts collection weeks 1–12.

`OrderBook(records, duration)` accepts the record list and simulation duration, checks collection weeks against that duration and rejects duplicate IDs with `ValueError`. Its `orders` attribute is a list of Order objects. `bakery.order_book` exposes the bakery's OrderBook.

Tests may inspect these objects but must not mutate them directly. Other internal methods and data structures are your choice.

## Weekly records

Retain the Stage 1 keys documented in API.md and add:

| Field | Type and meaning |
|---|---|
| `fulfilled_order_ids` | List of IDs fulfilled that week, in ascending ID order |
| `missed_order_ids` | List of IDs missed that week, in ascending ID order |
| `order_revenue` | Advance-order revenue in integer pence |
| `walk_in_revenue` | Walk-in revenue in integer pence |

`revenue` is the sum of `order_revenue` and `walk_in_revenue`. Existing `sales` records walk-in quantities; `consumed` and `minutes_used` record total production. Apply the brief's no-orders rules to these fields.

## Running advance orders

Use the existing file replay command from API.md with a scenario containing orders. Inspect results through weekly records and `bakery.order_book.orders`. Keep ordinary no-order interactive trading and the Stage 1 callable entry points. No `--interactive-scenario` option, scenario argument to `interactive()`, or `display_orders()` function is required.
