# Demand Forecasts

Manual forecast scenarios rather than model-generated predictions.

| Field | Type | Constraint |
| --- | --- | --- |
| `product_id` | string | Reference to `products` |
| `month` | string | Required |
| `forecast_units` | integer | Required |
| `method` | string | manual, moving_average |

Read endpoint: `GET /api/resources/demand_forecasts`. A local operator bearer token is required.
Create, update and delete are supported by the operator resource API. PUT is a full replacement and requires `_version`; deletes require a version query parameter.

Foreign keys are checked before writes; referenced records cannot be deleted. Unique constraints: `[]`.
Fixture file: `fixtures/demand_forecasts.json`. Repository exact-match helper: `find_by_product_id`.
Test module: `tests/test_demand_forecasts.py` checks persistence, validation, duplicate rollback and fixture compatibility.
Every fixture is synthetic and is safe to reset in a disposable local database.
