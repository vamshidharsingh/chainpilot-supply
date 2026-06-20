# Quality Checks

Inspection results for supplier products.

| Field | Type | Constraint |
| --- | --- | --- |
| `product_id` | string | Reference to `products` |
| `result` | string | pass, fail, pending |
| `notes` | string | Required |
| `sample_count` | integer | Required |

Read endpoint: `GET /api/resources/quality_checks`. A local operator bearer token is required.
Create, update and delete are supported by the operator resource API. PUT is a full replacement and requires `_version`; deletes require a version query parameter.

Foreign keys are checked before writes; referenced records cannot be deleted. Unique constraints: `[]`.
Fixture file: `fixtures/quality_checks.json`. Repository exact-match helper: `find_by_product_id`.
Test module: `tests/test_quality_checks.py` checks persistence, validation, duplicate rollback and fixture compatibility.
Every fixture is synthetic and is safe to reset in a disposable local database.
