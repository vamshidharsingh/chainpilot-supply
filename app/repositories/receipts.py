"""Immutable purchase-order receipt confirmations."""
from app.repository import Repository

class ResourceRepository(Repository):
    resource = 'receipts'

    def find_by_purchase_order_id(self, value):
        """Return exact matches, independent of the paginated UI listing."""
        rows = self.conn.execute('SELECT id FROM records WHERE resource=? ORDER BY id', (self.resource,))
        return [item for row in rows if (item := self.get(row['id']))['purchase_order_id'] == value]
