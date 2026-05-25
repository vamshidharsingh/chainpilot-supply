"""Transactional domain commands. Generic CRUD never writes derived state."""
import uuid
from datetime import date, datetime, timezone
from .repository import Repository
from .db import transaction
from .errors import AppError, Conflict, Forbidden

def rows(conn, name):
    repo = Repository(conn, name)
    return [repo.get(r['id']) for r in conn.execute('SELECT id FROM records WHERE resource=? ORDER BY id', (name,))]

def find(conn, name, **criteria):
    return next((r for r in rows(conn, name) if all((r.get(k) == v for k, v in criteria.items()))), None)

def update(conn, name, row, **changes):
    data = {k: v for k, v in row.items() if k not in ('id', '_version')}
    data.update(changes)
    return Repository(conn, name).update(row['id'], data, row['_version'])

def positive(value, name='quantity'):
    if type(value) is not int or not 0 < value <= 10 ** 12:
        raise AppError(name + ' must be a positive integer')
    return value

def text(value, name):
    if not isinstance(value, str) or not value.strip() or len(value) > 200:
        raise AppError(name + ' must be non-empty text (max 200)')
    return value

def execute(conn, action, data):
    if not isinstance(data, dict):
        raise AppError('JSON object required')
    if action not in ACTIONS:
        raise AppError('Unknown workflow')
    with transaction(conn):
        try:
            return ACTIONS[action](conn, data)
        except KeyError as exc:
            raise AppError('Missing workflow field: ' + str(exc.args[0]))

def inventory(conn, product_id, warehouse_id):
    Repository(conn, 'products').get(product_id)
    Repository(conn, 'warehouses').get(warehouse_id)
    existing = find(conn, 'inventory', product_id=product_id, warehouse_id=warehouse_id)
    return existing or Repository(conn, 'inventory').create(dict(product_id=product_id, warehouse_id=warehouse_id, quantity=0))

def capacity(conn, warehouse_id, extra):
    warehouse = Repository(conn, 'warehouses').get(warehouse_id)
    occupied = sum((r['quantity'] for r in rows(conn, 'inventory') if r['warehouse_id'] == warehouse_id))
    if occupied + extra > warehouse['capacity_units']:
        raise Conflict('Warehouse capacity exceeded')

def receive(conn, data):
    order = Repository(conn, 'purchase_orders').get(text(data['purchase_order_id'], 'purchase_order_id'))
    reference = text(data['reference'], 'reference')
    prior = find(conn, 'receipts', purchase_order_id=order['id'])
    if prior:
        if prior['reference'] != reference:
            raise Conflict('Purchase order already received with another reference')
        return prior
    if order['status'] != 'approved':
        raise Conflict('Purchase order is not approved')
    positive(order['quantity'])
    capacity(conn, order['warehouse_id'], order['quantity'])
    position = inventory(conn, order['product_id'], order['warehouse_id'])
    receipt = Repository(conn, 'receipts').create(dict(purchase_order_id=order['id'], quantity=order['quantity'], reference=reference))
    update(conn, 'inventory', position, quantity=position['quantity'] + order['quantity'])
    update(conn, 'purchase_orders', order, status='received')
    Repository(conn, 'stock_movements').create(dict(product_id=order['product_id'], warehouse_id=order['warehouse_id'], quantity_delta=order['quantity'], kind='receipt', reference=reference))
    return receipt

def dispatch(conn, data):
    product_id = text(data['product_id'], 'product_id')
    warehouse_id = text(data['warehouse_id'], 'warehouse_id')
    quantity = positive(data['quantity'])
    reference = text(data['reference'], 'reference')
    destination = text(data['destination'], 'destination')
    prior = find(conn, 'shipments', reference=reference)
    if prior:
        if (prior['product_id'], prior['warehouse_id'], prior['quantity'], prior['destination']) != (product_id, warehouse_id, quantity, destination):
            raise Conflict('Shipment reference reused')
        return prior
    position = inventory(conn, product_id, warehouse_id)
    if position['quantity'] < quantity:
        raise Conflict('Insufficient stock')
    shipment = Repository(conn, 'shipments').create(dict(product_id=product_id, warehouse_id=warehouse_id, quantity=quantity, destination=destination, status='dispatched', reference=reference))
    update(conn, 'inventory', position, quantity=position['quantity'] - quantity)
    Repository(conn, 'stock_movements').create(dict(product_id=product_id, warehouse_id=warehouse_id, quantity_delta=-quantity, kind='dispatch', reference=reference))
    return shipment

def move_stock(conn, data):
    product_id = text(data['product_id'], 'product_id')
    source_id = text(data['source_id'], 'source_id')
    target_id = text(data['target_id'], 'target_id')
    quantity = positive(data['quantity'])
    reference = text(data['reference'], 'reference')
    if source_id == target_id:
        raise AppError('Warehouses must differ')
    prior = [r for r in rows(conn, 'stock_movements') if r['reference'] == reference]
    if prior:
        expected = {(source_id, -quantity), (target_id, quantity)}
        if len(prior) != 2 or any((r['product_id'] != product_id or r['kind'] != 'transfer' for r in prior)) or {(r['warehouse_id'], r['quantity_delta']) for r in prior} != expected:
            raise Conflict('Reference reused with different movement')
        return dict(reference=reference, movements=prior)
    source = inventory(conn, product_id, source_id)
    target = inventory(conn, product_id, target_id)
    if source['quantity'] < quantity:
        raise Conflict('Insufficient stock')
    capacity(conn, target_id, quantity)
    update(conn, 'inventory', source, quantity=source['quantity'] - quantity)
    update(conn, 'inventory', target, quantity=target['quantity'] + quantity)
    movements = [Repository(conn, 'stock_movements').create(dict(product_id=product_id, warehouse_id=warehouse, quantity_delta=delta, kind='transfer', reference=reference)) for warehouse, delta in ((source_id, -quantity), (target_id, quantity))]
    return dict(reference=reference, movements=movements)
ACTIONS = {'receive': receive, 'dispatch': dispatch, 'move_stock': move_stock}

def place_purchase_order(conn, data):
    return Repository(conn, 'purchase_orders').create(dict(supplier_id=text(data['supplier_id'], 'supplier_id'), product_id=text(data['product_id'], 'product_id'), warehouse_id=text(data['warehouse_id'], 'warehouse_id'), quantity=positive(data['quantity']), unit_cost_cents=positive(data['unit_cost_cents'], 'unit_cost_cents'), status='approved'))

def update_shipment(conn, data):
    shipment = Repository(conn, 'shipments').get(text(data['shipment_id'], 'shipment_id'))
    status = text(data['status'], 'status')
    if shipment['status'] == status:
        return shipment
    allowed = {'dispatched': 'in_transit', 'in_transit': 'delivered'}
    if allowed.get(shipment['status']) != status:
        raise Conflict('Invalid shipment transition')
    return update(conn, 'shipments', shipment, status=status)
ACTIONS.update(place_purchase_order=place_purchase_order, update_shipment=update_shipment)
