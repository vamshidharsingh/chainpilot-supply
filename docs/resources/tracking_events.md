# Tracking Events

Operator-entered shipment milestones.

| Field | Type | Constraint |
| --- | --- | --- |
| `shipment_reference` | string | Required |
| `location` | string | Required |
| `event` | string | picked_up, arrived, delivered |
| `occurred_at` | string | datetime |

Read endpoint: `GET /api/resources/tracking_events`. A local operator bearer token is required.
Create, update and delete are supported by the operator resource API. PUT is a full replacement and requires `_version`; deletes require a version query parameter.

Foreign keys are checked before writes; referenced records cannot be deleted. Unique constraints: `[]`.
Fixture file: `fixtures/tracking_events.json`. Repository exact-match helper: `find_by_shipment_reference`.
Test module: `tests/test_tracking_events.py` checks persistence, validation, duplicate rollback and fixture compatibility.
Every fixture is synthetic and is safe to reset in a disposable local database.
