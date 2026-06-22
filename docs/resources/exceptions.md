# Exceptions

Operational issue queue.

| Field | Type | Constraint |
| --- | --- | --- |
| `subject` | string | Required |
| `severity` | string | low, medium, high |
| `status` | string | open, resolved |
| `reference` | string | Required |

Read endpoint: `GET /api/resources/exceptions`. A local operator bearer token is required.
Create, update and delete are supported by the operator resource API. PUT is a full replacement and requires `_version`; deletes require a version query parameter.

Foreign keys are checked before writes; referenced records cannot be deleted. Unique constraints: `[]`.
Fixture file: `fixtures/exceptions.json`. Repository exact-match helper: `find_by_subject`.
Test module: `tests/test_exceptions.py` checks persistence, validation, duplicate rollback and fixture compatibility.
Every fixture is synthetic and is safe to reset in a disposable local database.
