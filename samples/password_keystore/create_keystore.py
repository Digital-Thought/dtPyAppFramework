"""
Password Keystore Sample - Step 1: Create Keystore

This script demonstrates creating a keystore with a specific password.
The keystore can then be accessed from a different location using the
same password via the --password argument.

Usage:
    python create_keystore.py --password "my_secure_password"

This will:
    1. Create a keystore in ./location_a/data/keystore/
    2. Store a test secret in the keystore
    3. Display the keystore path for use in the next step
"""
import sys
import os
import shutil

sys.path.append(os.path.abspath('../../src'))

from dtPyAppFramework.application import AbstractApp
from dtPyAppFramework.settings import Settings
from dtPyAppFramework.paths import ApplicationPaths

import logging


class CreateKeystoreApp(AbstractApp):
    """
    Creates a keystore with a specific password and stores test secrets.
    """

    def define_args(self, arg_parser):
        """Define custom command-line arguments."""
        arg_parser.add_argument(
            '--secret-name',
            type=str,
            default='test_secret',
            help='Name of the test secret to create'
        )
        arg_parser.add_argument(
            '--secret-value',
            type=str,
            default='Hello from password_keystore sample!',
            help='Value of the test secret'
        )

    def main(self, args):
        """
        Create a keystore and store a test secret.
        """
        logging.info("=" * 60)
        logging.info("PASSWORD KEYSTORE SAMPLE - CREATE KEYSTORE")
        logging.info("=" * 60)

        # Show the password source (should be from --password argument)
        keystore_pwd = os.environ.get('KEYSTORE_PASSWORD')
        if keystore_pwd:
            logging.info(f"KEYSTORE_PASSWORD is SET (length: {len(keystore_pwd)} chars)")
        else:
            logging.warning("KEYSTORE_PASSWORD is NOT SET - using system-generated password")
            logging.warning("This keystore will NOT be portable to other locations!")

        # Get the keystore path (keystores are stored in usr_data_root_path)
        keystore_dir = ApplicationPaths().usr_data_root_path
        logging.info(f"Keystore directory: {keystore_dir}")

        # Store a test secret
        secret_name = args.secret_name
        secret_value = args.secret_value

        logging.info(f"Storing secret: '{secret_name}'")
        Settings().secret_manager.set_secret(secret_name, secret_value)

        # Verify the secret was stored
        retrieved = Settings().secret_manager.get_secret(secret_name)
        if retrieved == secret_value:
            logging.info("Secret stored and verified successfully!")
        else:
            logging.error("Secret verification failed!")
            return

        # Store a timestamp to prove this is the same keystore
        import datetime
        timestamp = datetime.datetime.now().isoformat()
        Settings().secret_manager.set_secret('creation_timestamp', timestamp)
        logging.info(f"Creation timestamp stored: {timestamp}")

        # Display instructions for next step
        print("\n" + "=" * 60)
        print("KEYSTORE CREATED SUCCESSFULLY")
        print("=" * 60)
        print(f"\nKeystore directory: {keystore_dir}")
        print(f"Secret stored: {secret_name}")
        print("\nTo test accessing this keystore from a different location:")
        print("  1. The keystore will be automatically copied to ./location_b/data/")
        print("  2. Run: python access_keystore.py --password \"<same_password>\"")
        print("\nThe keystore file is:")

        # List the keystore files
        if os.path.exists(keystore_dir):
            for f in os.listdir(keystore_dir):
                if f.endswith('.v3keystore') or f.endswith('.v2keystore'):
                    print(f"    {os.path.join(keystore_dir, f)}")

    def exiting(self):
        logging.info("CreateKeystoreApp exiting...")


if __name__ == '__main__':
    # Use a specific working directory for this sample
    work_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'location_a')
    os.makedirs(work_dir, exist_ok=True)
    os.chdir(work_dir)

    # Enable container mode to use simplified paths and direct password
    os.environ['CONTAINER_MODE'] = "True"

    CreateKeystoreApp(
        description="Create Keystore Sample",
        version="1.0",
        short_name="keystore_sample",  # Must match access_keystore.py for shared keystore
        full_name="Create Keystore Sample Application",
        console_app=True
    ).run()
