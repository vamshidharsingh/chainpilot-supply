# Batches

Lot metadata for product traceability.

| Field | Type | Constraint |
| --- | --- | --- |
| `product_id` | string | Reference to `products` |
| `lot_number` | string | Required |
| `manufactured_on` | string | date |
| `quantity` | integer | Required |

Read endpoint: `GET /api/resources/batches`. A local operator bearer token is required.
Create, update and delete are supported by the operator resource API. PUT is a full replacement and requires `_version`; deletes require a version query parameter.

Foreign keys are checked before writes; referenced records cannot be deleted. Unique constraints: `["lot_number"]`.
Fixture file: `fixtures/batches.json`. Repository exact-match helper: `find_by_product_id`.
Test module: `tests/test_batches.py` checks persistence, validation, duplicate rollback and fixture compatibility.
Every fixture is synthetic and is safe to reset in a disposable local database.
