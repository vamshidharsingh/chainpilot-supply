# Purchase Orders

Approved purchase orders awaiting a single atomic receipt.

| Field | Type | Constraint |
| --- | --- | --- |
| `supplier_id` | string | Reference to `suppliers` |
| `product_id` | string | Reference to `products` |
| `warehouse_id` | string | Reference to `warehouses` |
| `quantity` | integer | Required |
| `unit_cost_cents` | integer | Required |
| `status` | string | approved, received |

Read endpoint: `GET /api/resources/purchase_orders`. A local operator bearer token is required.
This resource is read-only through the generic HTTP API. Use the documented business workflows so derived state remains consistent.

Foreign keys are checked before writes; referenced records cannot be deleted. Unique constraints: `[]`.
Fixture file: `fixtures/purchase_orders.json`. Repository exact-match helper: `find_by_supplier_id`.
Test module: `tests/test_purchase_orders.py` checks persistence, validation, duplicate rollback and fixture compatibility.
Every fixture is synthetic and is safe to reset in a disposable local database.
