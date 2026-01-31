"""
Concurrent Keystore Sample - Worker Application

This is a standalone worker application that accesses the shared keystore.
Each instance runs as a completely separate process with its own PID.

Usage:
    python worker.py --password "test_password" --worker-id 0 --iterations 10

Run multiple instances in separate terminals to test concurrent access:
    Terminal 1: python worker.py --password "test" --worker-id 0 --iterations 20
    Terminal 2: python worker.py --password "test" --worker-id 1 --iterations 20
    Terminal 3: python worker.py --password "test" --worker-id 2 --iterations 20

Prerequisites:
    Run setup_keystore.py first to initialise the shared keystore.
"""
import sys
import os
import time
import random

sys.path.append(os.path.abspath('../../src'))

from dtPyAppFramework.application import AbstractApp
from dtPyAppFramework.paths import ApplicationPaths

import logging


class WorkerApp(AbstractApp):
    """
    Worker application that performs read-modify-write operations on the shared keystore.
    """

    def define_args(self, arg_parser):
        """Define custom command-line arguments."""
        arg_parser.add_argument(
            '--worker-id',
            type=int,
            required=True,
            help='Unique worker ID (0, 1, 2, ...)'
        )
        arg_parser.add_argument(
            '--iterations',
            type=int,
            default=10,
            help='Number of operations to perform (default: 10)'
        )
        arg_parser.add_argument(
            '--delay',
            type=float,
            default=0.01,
            help='Max random delay between operations in seconds (default: 0.01)'
        )

    def main(self, args):
        """
        Perform read-modify-write operations on the shared keystore.
        """
        worker_id = args.worker_id
        iterations = args.iterations
        max_delay = args.delay
        pid = os.getpid()

        logging.info("=" * 60)
        logging.info(f"WORKER {worker_id} STARTED (PID: {pid})")
        logging.info("=" * 60)

        # Check password is set
        password = os.environ.get('KEYSTORE_PASSWORD')
        if not password:
            logging.error("KEYSTORE_PASSWORD not set!")
            logging.error("Usage: python worker.py --password \"test_password\" --worker-id 0")
            return

        # Get keystore path
        keystore_dir = ApplicationPaths().usr_data_root_path
        keystore_path = os.path.join(keystore_dir, 'concurrent_test.v3keystore')

        if not os.path.exists(keystore_path):
            logging.error(f"Keystore not found: {keystore_path}")
            logging.error("Run setup_keystore.py first!")
            return

        logging.info(f"Worker ID: {worker_id}")
        logging.info(f"Process ID: {pid}")
        logging.info(f"Iterations: {iterations}")
        logging.info(f"Keystore: {keystore_path}")

        # Open the keystore
        from dtPyAppFramework.settings.secrets.keystore import PasswordProtectedKeystoreWithHMAC
        keystore = PasswordProtectedKeystoreWithHMAC(keystore_path, password)

        start_time = time.time()
        logging.info("\nStarting operations...")

        successful_ops, failed_ops = self._run_operations(
            keystore, worker_id, iterations, max_delay
        )

        elapsed_time = time.time() - start_time

        self._print_summary(keystore, worker_id, pid, successful_ops,
                            failed_ops, elapsed_time)

    def _run_operations(self, keystore, worker_id, iterations, max_delay):
        """Execute the read-modify-write loop and return (successful, failed) counts."""
        successful_ops = 0
        failed_ops = 0

        for i in range(iterations):
            try:
                current = keystore.get('shared_counter')
                current = 0 if current is None else int(current)

                time.sleep(random.uniform(0.001, max_delay))

                keystore.set('shared_counter', str(current + 1))

                worker_key = f'worker_{worker_id}_count'
                worker_count = keystore.get(worker_key)
                worker_count = 0 if worker_count is None else int(worker_count)
                keystore.set(worker_key, str(worker_count + 1))

                successful_ops += 1

                if (i + 1) % 5 == 0 or (i + 1) == iterations:
                    logging.info(f"[Worker {worker_id}] Completed {i + 1}/{iterations} operations")

            except Exception as ex:
                failed_ops += 1
                logging.error(f"[Worker {worker_id}] Operation {i + 1} failed: {ex}")

        return successful_ops, failed_ops

    def _print_summary(self, keystore, worker_id, pid, successful_ops,
                       failed_ops, elapsed_time):
        """Print the final summary for this worker."""
        final_counter = int(keystore.get('shared_counter') or 0)
        my_contributions = int(keystore.get(f'worker_{worker_id}_count') or 0)

        print("\n" + "=" * 60)
        print(f"WORKER {worker_id} COMPLETED (PID: {pid})")
        print("=" * 60)
        print("\nResults:")
        print(f"  Successful operations: {successful_ops}")
        print(f"  Failed operations: {failed_ops}")
        print(f"  Time elapsed: {elapsed_time:.2f} seconds")
        print(f"  Operations/second: {successful_ops / elapsed_time:.1f}")
        print("\nKeystore state:")
        print(f"  My contributions: {my_contributions}")
        print(f"  Current shared_counter: {final_counter}")
        print("=" * 60)

    def exiting(self):
        logging.info(f"Worker exiting (PID: {os.getpid()})")


if __name__ == '__main__':
    # Set up working directory
    work_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
    os.makedirs(work_dir, exist_ok=True)
    os.chdir(work_dir)

    # Enable container mode
    os.environ['CONTAINER_MODE'] = "True"

    WorkerApp(
        description="Concurrent Keystore Worker",
        version="1.0",
        short_name="concurrent_test",  # Shared short_name for all scripts
        full_name="Concurrent Keystore Worker Application",
        console_app=True
    ).run()
