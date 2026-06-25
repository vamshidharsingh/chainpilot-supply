# Products

SKU catalog and replenishment thresholds.

| Field | Type | Constraint |
| --- | --- | --- |
| `sku` | string | Required |
| `name` | string | Required |
| `unit` | string | Required |
| `reorder_point` | integer | Required |

Read endpoint: `GET /api/resources/products`. A local operator bearer token is required.
Create, update and delete are supported by the operator resource API. PUT is a full replacement and requires `_version`; deletes require a version query parameter.

Foreign keys are checked before writes; referenced records cannot be deleted. Unique constraints: `["sku"]`.
Fixture file: `fixtures/products.json`. Repository exact-match helper: `find_by_sku`.
Test module: `tests/test_products.py` checks persistence, validation, duplicate rollback and fixture compatibility.
Every fixture is synthetic and is safe to reset in a disposable local database.
