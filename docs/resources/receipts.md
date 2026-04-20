# Receipts

Immutable purchase-order receipt confirmations.

| Field | Type | Constraint |
| --- | --- | --- |
| `purchase_order_id` | string | Reference to `purchase_orders` |
| `quantity` | integer | Required |
| `reference` | string | Required |

Read endpoint: `GET /api/resources/receipts`. A local operator bearer token is required.
This resource is read-only through the generic HTTP API. Use the documented business workflows so derived state remains consistent.

Foreign keys are checked before writes; referenced records cannot be deleted. Unique constraints: `["purchase_order_id", "reference"]`.
Fixture file: `fixtures/receipts.json`. Repository exact-match helper: `find_by_purchase_order_id`.
Test module: `tests/test_receipts.py` checks persistence, validation, duplicate rollback and fixture compatibility.
Every fixture is synthetic and is safe to reset in a disposable local database.
