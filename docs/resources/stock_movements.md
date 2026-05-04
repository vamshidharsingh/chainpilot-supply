# Stock Movements

Signed stock events for inbound, outbound and transfer workflows.

| Field | Type | Constraint |
| --- | --- | --- |
| `product_id` | string | Reference to `products` |
| `warehouse_id` | string | Reference to `warehouses` |
| `quantity_delta` | integer | Required |
| `kind` | string | receipt, dispatch, transfer |
| `reference` | string | Required |

Read endpoint: `GET /api/resources/stock_movements`. A local operator bearer token is required.
This resource is read-only through the generic HTTP API. Use the documented business workflows so derived state remains consistent.

Foreign keys are checked before writes; referenced records cannot be deleted. Unique constraints: `[]`.
Fixture file: `fixtures/stock_movements.json`. Repository exact-match helper: `find_by_product_id`.
Test module: `tests/test_stock_movements.py` checks persistence, validation, duplicate rollback and fixture compatibility.
Every fixture is synthetic and is safe to reset in a disposable local database.
