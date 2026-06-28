"""Operator-entered shipment milestones."""
from app.repository import Repository

class ResourceRepository(Repository):
    resource = 'tracking_events'

    def find_by_shipment_reference(self, value):
        """Return exact matches, independent of the paginated UI listing."""
        rows = self.conn.execute('SELECT id FROM records WHERE resource=? ORDER BY id', (self.resource,))
        return [item for row in rows if (item := self.get(row['id']))['shipment_reference'] == value]
