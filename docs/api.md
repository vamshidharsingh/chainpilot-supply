# REST API

Base URL: `http://127.0.0.1:8013`. Supply `Authorization: Bearer <APP_TOKEN>` for every data endpoint. JSON writes require `Content-Type: application/json`. Bodies are limited to 65,536 bytes. All records are intended for one local demo operator.

| Method and route | Result |
| --- | --- |
| `GET /api/health` | Public status and project slug |
| `GET /api/meta` | Public project configuration and resource schemas; no record payloads |
| `GET /api/dashboard` | Four computed metrics, resource counts, chart values |
| `GET /api/audit` | Latest 50 metadata-only audit entries |
| `GET /api/resources/<name>` | Paginated list: items, total, limit, offset |
| `GET /api/resources/<name>/<id>` | Single record plus `_version` |
| `POST /api/resources/<name>` | Create an operator-managed record, status 201 |
| `PUT /api/resources/<name>/<id>` | Full replacement with current `_version` |
| `DELETE /api/resources/<name>/<id>?version=N` | Version-checked removal if unreferenced |
| `GET /api/export/<name>` | All rows as CSV |
| `POST /api/workflows/<action>` | Transactional business command |

List accepts `limit` (1–200, default 50), `offset` (nonnegative) and `search` (case-insensitive text). `total` is the entire resource count before filtering. A record ID is an opaque string. Writes reject unexpected fields. `_version` is response metadata and is supplied only for PUT; optional `id` can be provided on POST. For field definitions see `docs/resources/`.

## Read example
```bash
curl -H "Authorization: Bearer demo-local-token" http://127.0.0.1:8013/api/resources/suppliers
```

## Workflow bodies
POST the JSON object below to `/api/workflows/<action>`. Returned generated IDs should be pasted into follow-up requests. Change reference values when creating an independent operation; reuse them for a retry of the same operation.

### `receive` — Receive a purchase order

```json
{
  "purchase_order_id": "po-1",
  "reference": "receipt-demo-1"
}
```

### `dispatch` — Dispatch warehouse stock

```json
{
  "product_id": "product-1",
  "warehouse_id": "warehouse-1",
  "quantity": 5,
  "destination": "Demo customer depot",
  "reference": "shipment-demo-1"
}
```

### `move_stock` — Move stock between warehouses

```json
{
  "product_id": "product-1",
  "source_id": "warehouse-1",
  "target_id": "warehouse-2",
  "quantity": 10,
  "reference": "move-demo-1"
}
```

### `place_purchase_order` — Place a purchase order

```json
{
  "supplier_id": "supplier-1",
  "product_id": "product-2",
  "warehouse_id": "warehouse-1",
  "quantity": 50,
  "unit_cost_cents": 400
}
```

### `update_shipment` — Advance shipment status

```json
{
  "shipment_id": "PASTE_SHIPMENT_ID",
  "status": "in_transit"
}
```

## Error contract
JSON errors have an `error` string. Status 400 means invalid JSON, fields or business input; 401 means invalid/missing token; 403 means forbidden Host, protected generic write or missing consent; 404 means unknown resource/record/asset; 409 means version, unique key, stock/funds/capacity or scheduling conflict. Unexpected exceptions return a generic 500 without leaking server paths or payloads.

Business commands return 200 on success. Their idempotent retries preserve the original record ID. Read-only resource schemas expose `writable: false`. Health emergency summaries are still authenticated; the demo does not publish card URLs or QR links.
