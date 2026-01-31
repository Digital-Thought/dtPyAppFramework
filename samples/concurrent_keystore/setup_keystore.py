"""
Concurrent Keystore Sample - Setup Script

This script initialises the shared keystore that will be accessed by multiple
worker processes. Run this before starting the workers.

Usage:
    python setup_keystore.py --password "test_password"

This will:
    1. Create/reset the shared keystore
    2. Initialise the shared counter to 0
    3. Clear any previous worker counts
"""
import sys
import os

sys.path.append(os.path.abspath('../../src'))

from dtPyAppFramework.application import AbstractApp
from dtPyAppFramework.paths import ApplicationPaths

import logging


class SetupKeystoreApp(AbstractApp):
    """
    Initialises the shared keystore for concurrent access testing.
    """

    def define_args(self, arg_parser):
        """Define custom command-line arguments."""
        arg_parser.add_argument(
            '--max-workers',
            type=int,
            default=10,
            help='Maximum number of workers to prepare for (default: 10)'
        )

    def main(self, args):
        """
        Initialise the shared keystore.
        """
        logging.info("=" * 60)
        logging.info("CONCURRENT KEYSTORE - SETUP")
        logging.info("=" * 60)

        # Check password is set
        password = os.environ.get('KEYSTORE_PASSWORD')
        if not password:
            logging.error("KEYSTORE_PASSWORD not set!")
            logging.error("Usage: python setup_keystore.py --password \"test_password\"")
            return

        logging.info(f"KEYSTORE_PASSWORD is SET (length: {len(password)} chars)")

        # Get keystore path
        keystore_dir = ApplicationPaths().usr_data_root_path
        keystore_path = os.path.join(keystore_dir, 'concurrent_test.v3keystore')
        lock_path = keystore_path + '.lock'

        logging.info(f"Keystore path: {keystore_path}")

        # Clean up old keystore if exists
        if os.path.exists(keystore_path):
            os.remove(keystore_path)
            logging.info("Removed existing keystore")
        if os.path.exists(lock_path):
            os.remove(lock_path)
            logging.info("Removed existing lock file")

        # Create and initialise keystore
        from dtPyAppFramework.settings.secrets.keystore import PasswordProtectedKeystoreWithHMAC
        keystore = PasswordProtectedKeystoreWithHMAC(keystore_path, password)

        # Initialise shared counter
        keystore.set('shared_counter', '0')
        logging.info("Initialised shared_counter = 0")

        # Clear worker counts
        for i in range(args.max_workers):
            keystore.delete(f'worker_{i}_count')

        logging.info(f"Cleared worker counts (0 to {args.max_workers - 1})")

        # Store test start timestamp
        import datetime
        keystore.set('test_started', datetime.datetime.now().isoformat())

        print("\n" + "=" * 60)
        print("KEYSTORE INITIALISED SUCCESSFULLY")
        print("=" * 60)
        print(f"\nKeystore: {keystore_path}")
        print("\nYou can now run workers in separate terminals:")
        print("  python worker.py --password \"<same_password>\" --worker-id 0 --iterations 10")
        print("  python worker.py --password \"<same_password>\" --worker-id 1 --iterations 10")
        print("  python worker.py --password \"<same_password>\" --worker-id 2 --iterations 10")
        print("\nOr use run_test.py to launch multiple workers automatically:")
        print("  python run_test.py --password \"<same_password>\" --workers 4 --iterations 10")
        print("=" * 60)

    def exiting(self):
        logging.info("Setup complete.")


if __name__ == '__main__':
    # Set up working directory
    work_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
    os.makedirs(work_dir, exist_ok=True)
    os.chdir(work_dir)

    # Enable container mode
    os.environ['CONTAINER_MODE'] = "True"

    SetupKeystoreApp(
        description="Setup Keystore",
        version="1.0",
        short_name="concurrent_test",  # Shared short_name for all scripts
        full_name="Concurrent Keystore Setup",
        console_app=True
    ).run()
