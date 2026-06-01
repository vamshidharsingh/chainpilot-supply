# Cost Centers

Cost allocation categories.

| Field | Type | Constraint |
| --- | --- | --- |
| `code` | string | Required |
| `name` | string | Required |
| `budget_cents` | integer | Required |

Read endpoint: `GET /api/resources/cost_centers`. A local operator bearer token is required.
Create, update and delete are supported by the operator resource API. PUT is a full replacement and requires `_version`; deletes require a version query parameter.

Foreign keys are checked before writes; referenced records cannot be deleted. Unique constraints: `["code"]`.
Fixture file: `fixtures/cost_centers.json`. Repository exact-match helper: `find_by_code`.
Test module: `tests/test_cost_centers.py` checks persistence, validation, duplicate rollback and fixture compatibility.
Every fixture is synthetic and is safe to reset in a disposable local database.
