# Supplier Scores

Human-entered supplier performance assessments.

| Field | Type | Constraint |
| --- | --- | --- |
| `supplier_id` | string | Reference to `suppliers` |
| `on_time_percent` | integer | Required |
| `quality_percent` | integer | Required |
| `notes` | string | Required |

Read endpoint: `GET /api/resources/supplier_scores`. A local operator bearer token is required.
Create, update and delete are supported by the operator resource API. PUT is a full replacement and requires `_version`; deletes require a version query parameter.

Foreign keys are checked before writes; referenced records cannot be deleted. Unique constraints: `[]`.
Fixture file: `fixtures/supplier_scores.json`. Repository exact-match helper: `find_by_supplier_id`.
Test module: `tests/test_supplier_scores.py` checks persistence, validation, duplicate rollback and fixture compatibility.
Every fixture is synthetic and is safe to reset in a disposable local database.
