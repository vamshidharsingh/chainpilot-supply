"""Human-entered supplier performance assessments."""
from app.repository import Repository

class ResourceRepository(Repository):
    resource = 'supplier_scores'

    def find_by_supplier_id(self, value):
        """Return exact matches, independent of the paginated UI listing."""
        rows = self.conn.execute('SELECT id FROM records WHERE resource=? ORDER BY id', (self.resource,))
        return [item for row in rows if (item := self.get(row['id']))['supplier_id'] == value]
