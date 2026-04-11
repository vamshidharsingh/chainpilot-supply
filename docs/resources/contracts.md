# Contracts

Supplier contract planning metadata.

| Field | Type | Constraint |
| --- | --- | --- |
| `supplier_id` | string | Reference to `suppliers` |
| `reference` | string | Required |
| `expires_on` | string | date |
| `status` | string | active, expired |

Read endpoint: `GET /api/resources/contracts`. A local operator bearer token is required.
Create, update and delete are supported by the operator resource API. PUT is a full replacement and requires `_version`; deletes require a version query parameter.

Foreign keys are checked before writes; referenced records cannot be deleted. Unique constraints: `["reference"]`.
Fixture file: `fixtures/contracts.json`. Repository exact-match helper: `find_by_supplier_id`.
Test module: `tests/test_contracts.py` checks persistence, validation, duplicate rollback and fixture compatibility.
Every fixture is synthetic and is safe to reset in a disposable local database.
