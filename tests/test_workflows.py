from app.workflows import execute, rows, update
from app.repository import Repository
from app.errors import AppError, Conflict, Forbidden, NotFound
from tests.helpers import DatabaseCase

class WorkflowTests(DatabaseCase):

    def receive(self, ref='receipt-1'):
        return execute(self.conn, 'receive', dict(purchase_order_id='po-1', reference=ref))

    def dispatch(self, qty=5, ref='ship-1'):
        return execute(self.conn, 'dispatch', dict(product_id='product-1', warehouse_id='warehouse-1', quantity=qty, reference=ref, destination='Demo depot'))

    def test_receipt_updates_stock_and_po(self):
        self.receive()
        self.assertEqual(Repository(self.conn, 'inventory').get('inventory-1')['quantity'], 150)
        self.assertEqual(Repository(self.conn, 'purchase_orders').get('po-1')['status'], 'received')

    def test_receipt_is_idempotent(self):
        self.receive()
        self.receive()
        self.assertEqual(Repository(self.conn, 'inventory').get('inventory-1')['quantity'], 150)
        self.assertEqual(len(rows(self.conn, 'receipts')), 1)

    def test_receipt_changed_reference_conflicts(self):
        self.receive()
        with self.assertRaises(Conflict):
            self.receive('another')

    def test_capacity_failure_rolls_back(self):
        warehouse = Repository(self.conn, 'warehouses').get('warehouse-1')
        update(self.conn, 'warehouses', warehouse, capacity_units=55)
        with self.assertRaises(Conflict):
            self.receive()
        self.assertEqual(rows(self.conn, 'receipts'), [])
        self.assertEqual(Repository(self.conn, 'inventory').get('inventory-1')['quantity'], 50)

    def test_dispatch_decrements_stock(self):
        self.dispatch()
        self.assertEqual(Repository(self.conn, 'inventory').get('inventory-1')['quantity'], 45)

    def test_dispatch_retry_and_conflict(self):
        first = self.dispatch()
        self.assertEqual(first['id'], self.dispatch()['id'])
        with self.assertRaises(Conflict):
            self.dispatch(6)

    def test_out_of_stock_rolls_back(self):
        with self.assertRaises(Conflict):
            self.dispatch(1000)
        self.assertEqual(rows(self.conn, 'shipments'), [])
        self.assertEqual(Repository(self.conn, 'inventory').get('inventory-1')['quantity'], 50)

    def move(self):
        return execute(self.conn, 'move_stock', dict(product_id='product-1', source_id='warehouse-1', target_id='warehouse-2', quantity=10, reference='move-1'))

    def test_move_conserves_total_stock(self):
        self.move()
        self.assertEqual(sum((r['quantity'] for r in rows(self.conn, 'inventory') if r['product_id'] == 'product-1')), 50)
        self.assertEqual(sum((r['quantity_delta'] for r in rows(self.conn, 'stock_movements'))), 0)

    def test_move_retry_is_idempotent(self):
        self.move()
        self.move()
        self.assertEqual(Repository(self.conn, 'inventory').get('inventory-1')['quantity'], 40)

    def test_invalid_quantities_rejected(self):
        for qty in (0, -1, True, 1.2):
            with self.assertRaises(AppError):
                self.dispatch(qty)

    def test_new_purchase_order_can_be_received(self):
        order = execute(self.conn, 'place_purchase_order', dict(supplier_id='supplier-1', product_id='product-2', warehouse_id='warehouse-2', quantity=7, unit_cost_cents=400))
        execute(self.conn, 'receive', dict(purchase_order_id=order['id'], reference='new-order'))
        self.assertTrue(any((r['product_id'] == 'product-2' and r['warehouse_id'] == 'warehouse-2' and (r['quantity'] == 7) for r in rows(self.conn, 'inventory'))))

    def test_shipment_transitions_are_monotonic(self):
        shipment = self.dispatch()
        with self.assertRaises(Conflict):
            execute(self.conn, 'update_shipment', dict(shipment_id=shipment['id'], status='delivered'))
        execute(self.conn, 'update_shipment', dict(shipment_id=shipment['id'], status='in_transit'))
        execute(self.conn, 'update_shipment', dict(shipment_id=shipment['id'], status='delivered'))
        with self.assertRaises(Conflict):
            execute(self.conn, 'update_shipment', dict(shipment_id=shipment['id'], status='dispatched'))
