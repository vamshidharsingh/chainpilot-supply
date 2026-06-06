from .workflows import rows
from .schema import all_schemas
from .repository import Repository

def dashboard(conn):
    counts = {name: Repository(conn, name).count() for name in all_schemas()}
    inventory = rows(conn, 'inventory')
    products = rows(conn, 'products')
    positions = [dict(label=p['sku'], value=sum((r['quantity'] for r in inventory if r['product_id'] == p['id'])), target=p['reorder_point']) for p in products]
    return dict(counts=counts, metrics=[dict(label='Units in stock', value=sum((r['quantity'] for r in inventory))), dict(label='Below reorder threshold', value=sum((r['value'] < r['target'] for r in positions))), dict(label='Orders awaiting receipt', value=sum((r['status'] == 'approved' for r in rows(conn, 'purchase_orders')))), dict(label='Dispatched shipments', value=counts['shipments'])], bars=positions)
