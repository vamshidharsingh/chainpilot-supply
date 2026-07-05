# Inventory

Transactional stock positions; balances are workflow-managed.

| Field | Type | Constraint |
| --- | --- | --- |
| `product_id` | string | Reference to `products` |
| `warehouse_id` | string | Reference to `warehouses` |
| `quantity` | integer | Required |

Read endpoint: `GET /api/resources/inventory`. A local operator bearer token is required.
This resource is read-only through the generic HTTP API. Use the documented business workflows so derived state remains consistent.

Foreign keys are checked before writes; referenced records cannot be deleted. Unique constraints: `[["product_id", "warehouse_id"]]`.
Fixture file: `fixtures/inventory.json`. Repository exact-match helper: `find_by_product_id`.
Test module: `tests/test_inventory.py` checks persistence, validation, duplicate rollback and fixture compatibility.
Every fixture is synthetic and is safe to reset in a disposable local database.
