"""
Concurrent Keystore Stress Test

A more intensive stress test for concurrent keystore access.
This test performs rapid read/write operations to verify file locking
works correctly under heavy load.

Usage:
    python stress_test.py --password "test_password" --workers 8 --iterations 50

Warning: This test may take several minutes to complete depending on
the number of workers and iterations.
"""
import sys
import os
import time
import multiprocessing
from multiprocessing import Process, Queue
import random
import traceback

sys.path.append(os.path.abspath('../../src'))

from dtPyAppFramework.application import AbstractApp
from dtPyAppFramework.paths import ApplicationPaths

import logging


def stress_worker(worker_id: int, iterations: int, keystore_path: str,
                  password: str, results_queue: Queue):
    """
    Stress test worker that performs rapid operations on the keystore.
    """
    os.environ['CONTAINER_MODE'] = "True"
    os.environ['KEYSTORE_PASSWORD'] = password

    from dtPyAppFramework.settings.secrets.keystore import PasswordProtectedKeystoreWithHMAC

    operations = {'get': 0, 'set': 0, 'delete': 0}
    errors = []
    start_time = time.time()

    try:
        keystore = PasswordProtectedKeystoreWithHMAC(keystore_path, password)

        for i in range(iterations):
            # Randomly choose operation type
            op_type = random.choice(['get', 'set', 'set', 'set'])  # More writes than reads
            key = f'stress_key_{random.randint(0, 19)}'  # 20 possible keys

            try:
                if op_type == 'get':
                    keystore.get(key)
                    operations['get'] += 1
                elif op_type == 'set':
                    value = f'worker_{worker_id}_iter_{i}_time_{time.time()}'
                    keystore.set(key, value)
                    operations['set'] += 1

                # Very short random delay
                time.sleep(random.uniform(0.001, 0.005))

            except Exception as ex:
                errors.append(f"Op {i} ({op_type}): {str(ex)}")

        elapsed = time.time() - start_time
        ops_per_sec = iterations / elapsed if elapsed > 0 else 0

        print(f"[Worker {worker_id}] Completed {iterations} ops in {elapsed:.2f}s "
              f"({ops_per_sec:.1f} ops/sec)")

    except Exception as ex:
        errors.append(f"Fatal: {str(ex)}\n{traceback.format_exc()}")

    results_queue.put({
        'worker_id': worker_id,
        'operations': operations,
        'errors': errors,
        'elapsed': time.time() - start_time
    })


class StressTestApp(AbstractApp):
    """
    Stress test for concurrent keystore access.
    """

    def define_args(self, arg_parser):
        arg_parser.add_argument(
            '--workers',
            type=int,
            default=8,
            help='Number of worker processes (default: 8)'
        )
        arg_parser.add_argument(
            '--iterations',
            type=int,
            default=50,
            help='Operations per worker (default: 50)'
        )
        arg_parser.add_argument(
            '--timeout',
            type=int,
            default=120,
            help='Maximum test duration in seconds (default: 120)'
        )

    def _initialise_keystore(self, keystore_path, password):
        """Clean up and initialise the keystore with seed data."""
        if os.path.exists(keystore_path):
            os.remove(keystore_path)
            lock_path = keystore_path + '.lock'
            if os.path.exists(lock_path):
                os.remove(lock_path)

        from dtPyAppFramework.settings.secrets.keystore import PasswordProtectedKeystoreWithHMAC
        keystore = PasswordProtectedKeystoreWithHMAC(keystore_path, password)
        for i in range(20):
            keystore.set(f'stress_key_{i}', f'initial_value_{i}')

    def _run_workers(self, num_workers, iterations, keystore_path, password,
                     timeout):
        """Spawn worker processes, wait with timeout, and return results."""
        results_queue = multiprocessing.Queue()
        start_time = time.time()

        processes = []
        for i in range(num_workers):
            p = Process(
                target=stress_worker,
                args=(i, iterations, keystore_path, password, results_queue)
            )
            processes.append(p)
            p.start()

        for p in processes:
            remaining = timeout - (time.time() - start_time)
            if remaining > 0:
                p.join(timeout=remaining)
            if p.is_alive():
                logging.warning(f"Process {p.pid} timed out, terminating...")
                p.terminate()
                p.join(timeout=5)

        total_elapsed = time.time() - start_time

        results = []
        while not results_queue.empty():
            results.append(results_queue.get())

        return results, total_elapsed

    def _analyse_results(self, results, total_elapsed, keystore_path, password):
        """Analyse and print the stress test results."""
        from dtPyAppFramework.settings.secrets.keystore import PasswordProtectedKeystoreWithHMAC

        total_ops = sum(sum(r['operations'].values()) for r in results)
        total_errors = sum(len(r['errors']) for r in results)

        print("\n" + "=" * 60)
        print("STRESS TEST RESULTS")
        print("=" * 60)

        print(f"\nTotal time: {total_elapsed:.2f} seconds")
        print(f"Total operations: {total_ops}")
        print(f"Total errors: {total_errors}")
        print(f"Throughput: {total_ops / total_elapsed:.1f} ops/sec")

        print("\nPer-worker breakdown:")
        for r in sorted(results, key=lambda x: x['worker_id']):
            ops = r['operations']
            print(f"  Worker {r['worker_id']}: "
                  f"get={ops['get']}, set={ops['set']}, "
                  f"errors={len(r['errors'])}")

        all_errors = []
        for r in results:
            for e in r['errors']:
                all_errors.append(f"Worker {r['worker_id']}: {e}")

        if all_errors:
            print(f"\nErrors ({len(all_errors)} total):")
            for e in all_errors[:10]:
                print(f"  {e}")
            if len(all_errors) > 10:
                print(f"  ... and {len(all_errors) - 10} more")

        self._verify_integrity(keystore_path, password)

        print("\n" + "=" * 60)
        if total_errors == 0:
            print("STRESS TEST PASSED: No errors during concurrent access!")
        else:
            print(f"STRESS TEST COMPLETED: {total_errors} errors occurred")
        print("=" * 60)

    def _verify_integrity(self, keystore_path, password):
        """Verify keystore integrity after the stress test."""
        from dtPyAppFramework.settings.secrets.keystore import PasswordProtectedKeystoreWithHMAC

        print("\nVerifying keystore integrity...")
        try:
            keystore = PasswordProtectedKeystoreWithHMAC(keystore_path, password)
            verified = 0
            for i in range(20):
                val = keystore.get(f'stress_key_{i}')
                if val:
                    verified += 1
            print(f"  {verified}/20 keys readable after stress test")

            if verified == 20:
                print("\n  KEYSTORE INTEGRITY: PASSED")
            else:
                print("\n  KEYSTORE INTEGRITY: PARTIAL (some keys missing)")

        except Exception as ex:
            print(f"\n  KEYSTORE INTEGRITY: FAILED - {ex}")

    def main(self, args):
        logging.info("=" * 60)
        logging.info("KEYSTORE STRESS TEST")
        logging.info("=" * 60)

        password = os.environ.get('KEYSTORE_PASSWORD')
        if not password:
            logging.error("KEYSTORE_PASSWORD not set!")
            return

        num_workers = args.workers
        iterations = args.iterations
        timeout = args.timeout

        logging.info("Configuration:")
        logging.info(f"  Workers: {num_workers}")
        logging.info(f"  Iterations per worker: {iterations}")
        logging.info(f"  Total operations: {num_workers * iterations}")
        logging.info(f"  Timeout: {timeout}s")

        keystore_dir = ApplicationPaths().usr_data_root_path
        keystore_path = os.path.join(keystore_dir, 'stress_test.v3keystore')

        self._initialise_keystore(keystore_path, password)

        logging.info(f"  Keystore: {keystore_path}")
        logging.info(f"\nStarting stress test with {num_workers} workers...")

        results, total_elapsed = self._run_workers(
            num_workers, iterations, keystore_path, password, timeout
        )

        self._analyse_results(results, total_elapsed, keystore_path, password)

    def exiting(self):
        pass  # Intentionally empty - no cleanup required


if __name__ == '__main__':
    work_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
    os.makedirs(work_dir, exist_ok=True)
    os.chdir(work_dir)

    os.environ['CONTAINER_MODE'] = "True"

    StressTestApp(
        description="Keystore Stress Test",
        version="1.0",
        short_name="stress_test",
        full_name="Keystore Stress Test Application",
        console_app=True
    ).run()
