"""
Password Keystore Sample - Step 2: Access Keystore

This script demonstrates accessing a keystore from a different location
using the --password argument. The keystore must have been created with
the same password.

Usage:
    python access_keystore.py --password "my_secure_password"

Prerequisites:
    1. Run create_keystore.py first with a password
    2. Copy the keystore file from location_a to location_b (this is done automatically)
    3. Use the SAME password when running this script
"""
import sys
import os
import shutil

sys.path.append(os.path.abspath('../../src'))

from dtPyAppFramework.application import AbstractApp
from dtPyAppFramework.settings import Settings
from dtPyAppFramework.paths import ApplicationPaths

import logging


class AccessKeystoreApp(AbstractApp):
    """
    Accesses a keystore using a password from a different location.
    """

    def define_args(self, arg_parser):
        """Define custom command-line arguments."""
        arg_parser.add_argument(
            '--secret-name',
            type=str,
            default='test_secret',
            help='Name of the secret to retrieve'
        )
        arg_parser.add_argument(
            '--skip-copy',
            action='store_true',
            help='Skip automatic keystore copy (assume already done)'
        )

    def main(self, args):
        """
        Access the keystore and retrieve the test secret.
        """
        logging.info("=" * 60)
        logging.info("PASSWORD KEYSTORE SAMPLE - ACCESS KEYSTORE")
        logging.info("=" * 60)

        # Show the password source
        keystore_pwd = os.environ.get('KEYSTORE_PASSWORD')
        if keystore_pwd:
            logging.info(f"KEYSTORE_PASSWORD is SET (length: {len(keystore_pwd)} chars)")
        else:
            logging.error("KEYSTORE_PASSWORD is NOT SET!")
            logging.error("You must provide the same password used to create the keystore.")
            logging.error("Usage: python access_keystore.py --password \"your_password\"")
            return

        # Get the keystore directory for this location (keystores are stored in usr_data_root_path)
        keystore_dir = ApplicationPaths().usr_data_root_path
        logging.info(f"Keystore directory: {keystore_dir}")

        # Try to retrieve the secret
        secret_name = args.secret_name
        logging.info(f"Attempting to retrieve secret: '{secret_name}'")

        try:
            secret_value = Settings().secret_manager.get_secret(secret_name)

            if secret_value:
                logging.info("SUCCESS! Secret retrieved from keystore.")
                print("\n" + "=" * 60)
                print("SECRET RETRIEVED SUCCESSFULLY")
                print("=" * 60)
                print(f"\nSecret name: {secret_name}")
                print(f"Secret value: {secret_value}")

                # Also retrieve the timestamp to prove it's the same keystore
                timestamp = Settings().secret_manager.get_secret('creation_timestamp')
                if timestamp:
                    print(f"\nKeystore creation timestamp: {timestamp}")
                    print("\nThis proves the same keystore is being accessed!")

            else:
                logging.error(f"Secret '{secret_name}' not found in keystore.")
                logging.error("Possible causes:")
                logging.error("  - Wrong password provided")
                logging.error("  - Keystore not copied to this location")
                logging.error("  - Secret was not created")

        except Exception as ex:
            logging.error(f"Failed to access keystore: {ex}")
            logging.error("This usually means the password is incorrect.")
            logging.error("Make sure you use the SAME password used in create_keystore.py")

    def exiting(self):
        logging.info("AccessKeystoreApp exiting...")


def setup_keystore_copy():
    """
    Copy the keystore from location_a to location_b.
    This simulates having the same keystore in a different container/location.

    In container mode, keystores are stored directly in the data directory
    (usr_data_root_path), not in a separate keystore subdirectory.
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    # In container mode, keystores are in {working_dir}/data/
    source_keystore_dir = os.path.join(base_dir, 'location_a', 'data')
    dest_keystore_dir = os.path.join(base_dir, 'location_b', 'data')

    if not os.path.exists(source_keystore_dir):
        print("ERROR: Source data directory not found!")
        print(f"Expected location: {source_keystore_dir}")
        print("\nPlease run create_keystore.py first:")
        print('  python create_keystore.py --password "your_password"')
        return False

    # Create destination directory
    os.makedirs(dest_keystore_dir, exist_ok=True)

    # Copy all keystore files
    copied = False
    for filename in os.listdir(source_keystore_dir):
        if filename.endswith('.v3keystore') or filename.endswith('.v2keystore'):
            src = os.path.join(source_keystore_dir, filename)
            dst = os.path.join(dest_keystore_dir, filename)
            shutil.copy2(src, dst)
            print(f"Copied keystore: {filename}")
            copied = True

    if not copied:
        print("WARNING: No keystore files found to copy!")
        print(f"Searched in: {source_keystore_dir}")
        return False

    return True


if __name__ == '__main__':
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Check if --skip-copy is in arguments
    skip_copy = '--skip-copy' in sys.argv

    if not skip_copy:
        print("Setting up keystore copy from location_a to location_b...")
        if not setup_keystore_copy():
            sys.exit(1)
        print()

    # Use a different working directory for this sample
    work_dir = os.path.join(base_dir, 'location_b')
    os.makedirs(work_dir, exist_ok=True)
    os.chdir(work_dir)

    # Enable container mode to use simplified paths and direct password
    os.environ['CONTAINER_MODE'] = "True"

    AccessKeystoreApp(
        description="Access Keystore Sample",
        version="1.0",
        short_name="keystore_sample",  # Must match create_keystore.py for shared keystore
        full_name="Access Keystore Sample Application",
        console_app=True
    ).run()
