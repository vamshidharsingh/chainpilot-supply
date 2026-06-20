# Suppliers

Supplier contact directory.

| Field | Type | Constraint |
| --- | --- | --- |
| `name` | string | Required |
| `email` | string | email |
| `lead_days` | integer | Required |

Read endpoint: `GET /api/resources/suppliers`. A local operator bearer token is required.
Create, update and delete are supported by the operator resource API. PUT is a full replacement and requires `_version`; deletes require a version query parameter.

Foreign keys are checked before writes; referenced records cannot be deleted. Unique constraints: `[]`.
Fixture file: `fixtures/suppliers.json`. Repository exact-match helper: `find_by_name`.
Test module: `tests/test_suppliers.py` checks persistence, validation, duplicate rollback and fixture compatibility.
Every fixture is synthetic and is safe to reset in a disposable local database.
