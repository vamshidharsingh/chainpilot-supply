from concurrent.futures import ThreadPoolExecutor
import threading
from app.db import connect
from app.workflows import execute, rows, update
from app.repository import Repository
from app.errors import Conflict
from tests.helpers import DatabaseCase

class ConcurrencyTests(DatabaseCase):

    def run_parallel(self, tasks):
        barrier = threading.Barrier(len(tasks))

        def worker(task):
            conn = connect(self.db_path)
            try:
                barrier.wait(timeout=5)
                try:
                    execute(conn, task[0], task[1])
                    return 'ok'
                except Conflict:
                    return 'conflict'
            finally:
                conn.close()
        with ThreadPoolExecutor(max_workers=len(tasks)) as pool:
            return list(pool.map(worker, tasks))

    def test_concurrent_commands_preserve_domain_invariant(self):
        stock = Repository(self.conn, 'inventory').get('inventory-1')
        update(self.conn, 'inventory', stock, quantity=1)
        tasks = [('dispatch', dict(product_id='product-1', warehouse_id='warehouse-1', quantity=1, destination='Demo depot', reference='concurrent-' + str(i))) for i in range(2)]
        outcomes = self.run_parallel(tasks)
        self.assertEqual(outcomes.count('ok'), 1)
        self.assertEqual(Repository(self.conn, 'inventory').get('inventory-1')['quantity'], 0)
