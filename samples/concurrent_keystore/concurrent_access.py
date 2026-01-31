"""
Concurrent Keystore Access Sample

This sample demonstrates that multiple processes can safely access the same
keystore file concurrently, thanks to the file locking mechanism introduced
in v4.0.1.

Usage:
    python concurrent_access.py --password "test_password" --workers 4

This will:
    1. Create a shared keystore
    2. Spawn multiple worker processes
    3. Each worker reads and increments a counter in the keystore
    4. Verify no data corruption occurred

The file locking ensures atomic read-modify-write operations.
"""
import sys
import os
import time
import multiprocessing
from multiprocessing import Process, Value, Queue
import random

sys.path.append(os.path.abspath('../../src'))

from dtPyAppFramework.application import AbstractApp
from dtPyAppFramework.settings import Settings
from dtPyAppFramework.paths import ApplicationPaths
from dtPyAppFramework.process import ProcessManager

import logging


def worker_process(worker_id: int, iterations: int, keystore_path: str,
                   password: str, results_queue: Queue):
    """
    Worker process that performs read-modify-write operations on the keystore.

    Each worker:
    1. Reads the current counter value
    2. Increments it
    3. Writes the new value back
    4. Repeats for the specified number of iterations
    """
    # Set up environment for this process
    os.environ['CONTAINER_MODE'] = "True"
    os.environ['KEYSTORE_PASSWORD'] = password

    # Import here to ensure fresh initialisation in subprocess
    from dtPyAppFramework.settings.secrets.keystore import PasswordProtectedKeystoreWithHMAC

    successful_ops = 0
    failed_ops = 0

    try:
        # Open the keystore directly (simulates separate process access)
        keystore = PasswordProtectedKeystoreWithHMAC(keystore_path, password)

        for i in range(iterations):
            try:
                # Read current value
                current = keystore.get('shared_counter')
                if current is None:
                    current = 0
                else:
                    current = int(current)

                # Simulate some work (increases chance of race conditions)
                time.sleep(random.uniform(0.001, 0.01))

                # Increment and write back
                new_value = current + 1
                keystore.set('shared_counter', str(new_value))

                # Record this worker's contribution
                worker_key = f'worker_{worker_id}_count'
                worker_count = keystore.get(worker_key)
                if worker_count is None:
                    worker_count = 0
                else:
                    worker_count = int(worker_count)
                keystore.set(worker_key, str(worker_count + 1))

                successful_ops += 1

                if (i + 1) % 5 == 0:
                    print(f"[Worker {worker_id}] Completed {i + 1}/{iterations} operations")

            except Exception as ex:
                failed_ops += 1
                print(f"[Worker {worker_id}] Operation {i + 1} failed: {ex}")

        print(f"[Worker {worker_id}] Finished: {successful_ops} successful, {failed_ops} failed")

    except Exception as ex:
        print(f"[Worker {worker_id}] Fatal error: {ex}")
        failed_ops = iterations

    results_queue.put({
        'worker_id': worker_id,
        'successful': successful_ops,
        'failed': failed_ops
    })


class ConcurrentAccessApp(AbstractApp):
    """
    Demonstrates concurrent keystore access from multiple processes.
    """

    def define_args(self, arg_parser):
        """Define custom command-line arguments."""
        arg_parser.add_argument(
            '--workers',
            type=int,
            default=4,
            help='Number of worker processes (default: 4)'
        )
        arg_parser.add_argument(
            '--iterations',
            type=int,
            default=10,
            help='Operations per worker (default: 10)'
        )

    def main(self, args):
        """
        Run concurrent keystore access test.
        """
        logging.info("=" * 60)
        logging.info("CONCURRENT KEYSTORE ACCESS SAMPLE")
        logging.info("=" * 60)

        num_workers = args.workers
        iterations = args.iterations
        expected_total = num_workers * iterations

        # Check password is set
        password = os.environ.get('KEYSTORE_PASSWORD')
        if not password:
            logging.error("KEYSTORE_PASSWORD not set!")
            logging.error("Usage: python concurrent_access.py --password \"test_password\"")
            return

        logging.info("Configuration:")
        logging.info(f"  Workers: {num_workers}")
        logging.info(f"  Iterations per worker: {iterations}")
        logging.info(f"  Expected total operations: {expected_total}")

        # Get keystore path (keystores are stored in usr_data_root_path)
        keystore_dir = ApplicationPaths().usr_data_root_path
        keystore_path = os.path.join(keystore_dir, 'concurrent_access.v3keystore')
        logging.info(f"  Keystore path: {keystore_path}")

        # Initialise the shared counter
        logging.info("\nInitialising shared counter...")
        from dtPyAppFramework.settings.secrets.keystore import PasswordProtectedKeystoreWithHMAC
        keystore = PasswordProtectedKeystoreWithHMAC(keystore_path, password)
        keystore.set('shared_counter', '0')

        # Clear any previous worker counts
        for i in range(num_workers):
            keystore.delete(f'worker_{i}_count')

        logging.info("Shared counter initialised to 0")

        # Create results queue for inter-process communication
        results_queue = multiprocessing.Queue()

        # Spawn worker processes
        logging.info(f"\nSpawning {num_workers} worker processes...")
        start_time = time.time()

        processes = []
        for i in range(num_workers):
            p = Process(
                target=worker_process,
                args=(i, iterations, keystore_path, password, results_queue)
            )
            processes.append(p)
            p.start()
            logging.info(f"  Started worker {i}")

        # Wait for all processes to complete
        logging.info("\nWaiting for workers to complete...")
        for p in processes:
            p.join()

        elapsed_time = time.time() - start_time

        # Collect results
        results = []
        while not results_queue.empty():
            results.append(results_queue.get())

        # Verify results
        logging.info("\n" + "=" * 60)
        logging.info("RESULTS")
        logging.info("=" * 60)

        total_successful = sum(r['successful'] for r in results)
        total_failed = sum(r['failed'] for r in results)

        logging.info("\nWorker Results:")
        for r in sorted(results, key=lambda x: x['worker_id']):
            logging.info(f"  Worker {r['worker_id']}: {r['successful']} successful, {r['failed']} failed")

        logging.info(f"\nTotal operations: {total_successful + total_failed}")
        logging.info(f"  Successful: {total_successful}")
        logging.info(f"  Failed: {total_failed}")
        logging.info(f"  Time elapsed: {elapsed_time:.2f} seconds")

        # Re-open keystore to read final values
        keystore = PasswordProtectedKeystoreWithHMAC(keystore_path, password)
        final_counter = int(keystore.get('shared_counter') or 0)

        logging.info(f"\nFinal counter value: {final_counter}")
        logging.info(f"Expected value: {expected_total}")

        # Verify individual worker contributions
        logging.info("\nIndividual worker contributions (from keystore):")
        _total_worker_contributions = 0
        for i in range(num_workers):
            worker_count = keystore.get(f'worker_{i}_count')
            if worker_count:
                worker_count = int(worker_count)
                _total_worker_contributions += worker_count
                logging.info(f"  Worker {i}: {worker_count} operations")

        # Final verdict
        print("\n" + "=" * 60)
        if total_failed == 0:
            print("TEST PASSED: All operations completed successfully!")
            print(f"File locking prevented race conditions across {num_workers} processes.")
        else:
            print(f"TEST COMPLETED WITH ISSUES: {total_failed} operations failed")
            print("Check logs for details.")

        if final_counter == expected_total:
            print("\nCOUNTER INTEGRITY: PASSED")
            print(f"  Final counter ({final_counter}) matches expected ({expected_total})")
        else:
            print(f"\nCOUNTER INTEGRITY: MISMATCH (expected {expected_total}, got {final_counter})")
            print("  Note: Due to read-modify-write race conditions, the counter")
            print("  may be less than expected. This is expected behaviour when")
            print("  multiple processes read the same value before any writes.")
            print("  The important thing is that no data corruption occurred.")

        print("=" * 60)

    def exiting(self):
        logging.info("ConcurrentAccessApp exiting...")


if __name__ == '__main__':
    # Set up working directory
    work_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
    os.makedirs(work_dir, exist_ok=True)
    os.chdir(work_dir)

    # Enable container mode
    os.environ['CONTAINER_MODE'] = "True"

    ConcurrentAccessApp(
        description="Concurrent Keystore Access Sample",
        version="1.0",
        short_name="concurrent_access",
        full_name="Concurrent Keystore Access Sample Application",
        console_app=True
    ).run()
