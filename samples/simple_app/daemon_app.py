"""
Daemon Application Example - Long-Running Pattern

This example demonstrates a long-running application (daemon/service) that
keeps running until it receives a shutdown signal (SIGINT, SIGTERM, or
explicit request_shutdown() call).

Application Patterns:
    1. One-shot: Just return from main() - the app exits automatically
    2. Long-running: Call ProcessManager().wait_for_shutdown() to keep running

For one-shot applications, see the dev_app.py example.
"""
import sys
import os
import threading
import time

sys.path.append(os.path.abspath('../../src'))

from dtPyAppFramework.application import AbstractApp
from dtPyAppFramework.settings import Settings
from dtPyAppFramework.process import ProcessManager

import logging


class DaemonApp(AbstractApp):
    """
    A long-running daemon application example.

    This application starts background workers and keeps running until
    a shutdown signal is received (Ctrl+C, SIGTERM, etc.)
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.workers = []
        self.stop_event = threading.Event()

    def define_args(self, arg_parser):
        """Define any custom command-line arguments here."""
        arg_parser.add_argument(
            '--workers',
            type=int,
            default=2,
            help='Number of background workers to start'
        )

    def main(self, args):
        """
        Main application logic for a long-running daemon.

        This method:
        1. Starts background workers/services
        2. Calls wait_for_shutdown() to block until shutdown is requested
        3. Cleanup happens automatically after wait_for_shutdown() returns
        """
        logging.info("Starting daemon application")

        # Start background workers
        num_workers = getattr(args, 'workers', 2)
        self._start_workers(num_workers)

        logging.info(f"Started {num_workers} background workers")
        logging.info("Press Ctrl+C to stop the application")

        # Block until shutdown is requested
        # This is the key difference from one-shot apps!
        ProcessManager().wait_for_shutdown()

        # After wait_for_shutdown() returns, stop the workers
        logging.info("Shutdown signal received, stopping workers...")
        self._stop_workers()

    def _start_workers(self, count: int):
        """Start background worker threads."""
        for i in range(count):
            worker = threading.Thread(
                target=self._worker_loop,
                args=(i,),
                name=f"Worker-{i}",
                daemon=True
            )
            worker.start()
            self.workers.append(worker)

    def _stop_workers(self):
        """Signal workers to stop and wait for them."""
        self.stop_event.set()
        for worker in self.workers:
            worker.join(timeout=5.0)
            if worker.is_alive():
                logging.warning(f"{worker.name} did not stop gracefully")

    def _worker_loop(self, worker_id: int):
        """Background worker that runs until stop_event is set."""
        logging.info(f"Worker {worker_id} started")
        while not self.stop_event.is_set():
            # Simulate some work
            logging.debug(f"Worker {worker_id} doing work...")
            time.sleep(2)
        logging.info(f"Worker {worker_id} stopped")

    def exiting(self):
        """
        Custom cleanup logic executed during shutdown.

        This method is called automatically by the framework during shutdown.
        """
        logging.info('Daemon cleanup complete')


if __name__ == '__main__':
    os.environ['DEV_MODE'] = "True"
    DaemonApp(
        description="Daemon App",
        version="1.0",
        short_name="daemon_app",
        full_name="Daemon Application",
        console_app=True  # Set to True to see output in console
    ).run()
