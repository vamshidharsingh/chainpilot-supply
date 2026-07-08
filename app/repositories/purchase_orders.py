"""Approved purchase orders awaiting a single atomic receipt."""
from app.repository import Repository

class ResourceRepository(Repository):
    resource = 'purchase_orders'

    def find_by_supplier_id(self, value):
        """Return exact matches, independent of the paginated UI listing."""
        rows = self.conn.execute('SELECT id FROM records WHERE resource=? ORDER BY id', (self.resource,))
        return [item for row in rows if (item := self.get(row['id']))['supplier_id'] == value]
