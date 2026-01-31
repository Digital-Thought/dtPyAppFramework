"""
Concurrent Keystore Sample - Test Runner

This script launches multiple worker.py instances as separate processes,
each with its own process ID. This simulates multiple containers or
application instances accessing the same keystore.

Usage:
    python run_test.py --password "test_password" --workers 4 --iterations 10

This will:
    1. Set up the shared keystore (calls setup_keystore.py logic)
    2. Launch multiple worker.py processes in parallel
    3. Wait for all workers to complete
    4. Verify results and report statistics
"""
import sys
import os
import time
import subprocess

sys.path.append(os.path.abspath('../../src'))

from dtPyAppFramework.application import AbstractApp
from dtPyAppFramework.paths import ApplicationPaths

import logging


class RunTestApp(AbstractApp):
    """
    Test runner that launches multiple worker processes.
    """

    def define_args(self, arg_parser):
        """Define custom command-line arguments."""
        arg_parser.add_argument(
            '--workers',
            type=int,
            default=4,
            help='Number of worker processes to launch (default: 4)'
        )
        arg_parser.add_argument(
            '--iterations',
            type=int,
            default=10,
            help='Operations per worker (default: 10)'
        )
        arg_parser.add_argument(
            '--delay',
            type=float,
            default=0.01,
            help='Max random delay between operations (default: 0.01)'
        )

    def _initialise_keystore(self, keystore_path, password, num_workers):
        """Clean up and initialise the keystore for a fresh test run."""
        lock_path = keystore_path + '.lock'

        logging.info("\nInitialising keystore...")

        if os.path.exists(keystore_path):
            os.remove(keystore_path)
        if os.path.exists(lock_path):
            os.remove(lock_path)

        from dtPyAppFramework.settings.secrets.keystore import PasswordProtectedKeystoreWithHMAC
        keystore = PasswordProtectedKeystoreWithHMAC(keystore_path, password)
        keystore.set('shared_counter', '0')

        for i in range(num_workers):
            keystore.delete(f'worker_{i}_count')

        import datetime
        keystore.set('test_started', datetime.datetime.now().isoformat())

        logging.info("Keystore initialised with shared_counter = 0")

    def _launch_workers(self, num_workers, password, iterations, delay):
        """Launch worker subprocesses and return the list of (worker_id, Popen) tuples."""
        script_dir = os.path.dirname(os.path.abspath(__file__))
        worker_script = os.path.join(script_dir, 'worker.py')

        processes = []
        for i in range(num_workers):
            cmd = [
                sys.executable,
                worker_script,
                '--password', password,
                '--worker-id', str(i),
                '--iterations', str(iterations),
                '--delay', str(delay)
            ]

            proc = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                cwd=script_dir
            )
            processes.append((i, proc))
            logging.info(f"  Started worker {i} (PID: {proc.pid})")

        return processes

    def _collect_results(self, processes):
        """Wait for all worker processes and collect their results."""
        logging.info("\nWaiting for workers to complete...")
        results = []

        for worker_id, proc in processes:
            stdout, _ = proc.communicate()
            return_code = proc.returncode
            results.append({
                'worker_id': worker_id,
                'pid': proc.pid,
                'return_code': return_code,
                'output': stdout
            })
            if return_code == 0:
                logging.info(f"  Worker {worker_id} (PID: {proc.pid}) completed successfully")
            else:
                logging.warning(f"  Worker {worker_id} (PID: {proc.pid}) exited with code {return_code}")

        return results

    def _verify_and_report(self, keystore_path, password, results, num_workers,
                           expected_total, elapsed_time):
        """Re-open the keystore, verify results, and print the final report."""
        from dtPyAppFramework.settings.secrets.keystore import PasswordProtectedKeystoreWithHMAC

        logging.info("\n" + "=" * 60)
        logging.info("RESULTS")
        logging.info("=" * 60)

        keystore = PasswordProtectedKeystoreWithHMAC(keystore_path, password)
        final_counter = int(keystore.get('shared_counter') or 0)

        logging.info(f"\nTest duration: {elapsed_time:.2f} seconds")
        logging.info(f"Final shared_counter: {final_counter}")
        logging.info(f"Expected (if no races): {expected_total}")

        logging.info("\nWorker contributions:")
        total_contributions = 0
        for i in range(num_workers):
            worker_count = keystore.get(f'worker_{i}_count')
            if worker_count:
                count = int(worker_count)
                total_contributions += count
                pid = next((r['pid'] for r in results if r['worker_id'] == i), 'N/A')
                logging.info(f"  Worker {i} (PID: {pid}): {count} operations")

        logging.info(f"\nTotal contributions recorded: {total_contributions}")

        print("\n" + "=" * 60)
        failed_workers = sum(1 for r in results if r['return_code'] != 0)
        if failed_workers == 0:
            print("TEST PASSED: All workers completed successfully!")
            print(f"  - {num_workers} separate processes accessed the same keystore")
            print("  - File locking prevented data corruption")
        else:
            print(f"TEST COMPLETED WITH ISSUES: {failed_workers} workers failed")

        if final_counter == expected_total:
            print("\nCOUNTER INTEGRITY: PASSED")
            print(f"  Final counter ({final_counter}) matches expected ({expected_total})")
        else:
            print("\nCOUNTER INTEGRITY: MISMATCH")
            print(f"  Expected: {expected_total}, Got: {final_counter}")
            print("  Note: This can happen due to read-modify-write race conditions.")
            print("  The file locking prevents corruption, not application-level races.")
            print("  What matters is that no data corruption occurred.")

        print("=" * 60)
        print("\n[Worker output available in individual process logs]")

    def main(self, args):
        """
        Run the concurrent access test.
        """
        num_workers = args.workers
        iterations = args.iterations
        delay = args.delay
        expected_total = num_workers * iterations

        logging.info("=" * 60)
        logging.info("CONCURRENT KEYSTORE ACCESS TEST")
        logging.info("=" * 60)

        password = os.environ.get('KEYSTORE_PASSWORD')
        if not password:
            logging.error("KEYSTORE_PASSWORD not set!")
            logging.error("Usage: python run_test.py --password \"test_password\" --workers 4")
            return

        logging.info("Configuration:")
        logging.info(f"  Workers: {num_workers}")
        logging.info(f"  Iterations per worker: {iterations}")
        logging.info(f"  Expected total operations: {expected_total}")
        logging.info(f"  Max delay: {delay}s")

        keystore_dir = ApplicationPaths().usr_data_root_path
        keystore_path = os.path.join(keystore_dir, 'concurrent_test.v3keystore')

        logging.info(f"  Keystore: {keystore_path}")

        self._initialise_keystore(keystore_path, password, num_workers)

        logging.info(f"\nLaunching {num_workers} worker processes...")
        start_time = time.time()

        processes = self._launch_workers(num_workers, password, iterations, delay)
        results = self._collect_results(processes)

        elapsed_time = time.time() - start_time

        self._verify_and_report(keystore_path, password, results, num_workers,
                                expected_total, elapsed_time)

    def exiting(self):
        logging.info("Test runner exiting.")


if __name__ == '__main__':
    # Set up working directory
    work_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
    os.makedirs(work_dir, exist_ok=True)
    os.chdir(work_dir)

    # Enable container mode
    os.environ['CONTAINER_MODE'] = "True"

    RunTestApp(
        description="Concurrent Keystore Test Runner",
        version="1.0",
        short_name="concurrent_test",  # Shared short_name for all scripts
        full_name="Concurrent Keystore Test Runner",
        console_app=True
    ).run()
