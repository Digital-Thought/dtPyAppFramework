"""
Simple Application Example - One-Shot Pattern

This example demonstrates a one-shot application that performs its work
and exits automatically. For long-running applications (daemons, services),
see the daemon_app.py example.

Application Patterns:
    1. One-shot: Just return from main() - the app exits automatically
    2. Long-running: Call ProcessManager().wait_for_shutdown() to keep running
"""
import sys
import os

sys.path.append(os.path.abspath('../../src'))

from dtPyAppFramework.application import AbstractApp
from dtPyAppFramework.settings import Settings

import logging


class SimpleApp(AbstractApp):
    """
    A simple one-shot application example.

    One-shot applications perform their work in main() and then return.
    The framework automatically handles cleanup and shutdown.
    """

    def define_args(self, arg_parser):
        """Define any custom command-line arguments here."""
        pass

    def main(self, args):
        """
        Main application logic.

        For one-shot applications, simply perform your work and return.
        The framework will handle cleanup automatically.
        """
        logging.info("Running your code")

        # Example: Access settings and secrets
        logging.info(f'Secrets Store Index: {Settings().secret_manager.get_local_stores_index()}')

        # Example: Set and retrieve settings
        Settings()['test1'] = 'hello world'
        logging.info(f'test1 setting: {Settings().get("test1")}')

        # Example: Work with secrets
        Settings().secret_manager.set_secret('bob', 'hello world')

        # Example: Access various settings
        logging.info(f'testing_1: {Settings().get("testing_1")}')
        logging.info(f'file_test: {Settings().get("file_test")}')

        print('Application work completed!')

        # For one-shot apps: just return - the framework handles shutdown automatically
        # No need to call ProcessManager().handle_shutdown() or request_shutdown()

    def exiting(self):
        """
        Custom cleanup logic executed during shutdown.

        This method is called automatically by the framework during shutdown.
        Use it for any cleanup that needs to happen (closing connections, etc.)
        """
        logging.info('Performing custom cleanup during exit...')


if __name__ == '__main__':
    os.environ['DEV_MODE'] = "True"
    SimpleApp(
        description="Simple App",
        version="1.0",
        short_name="simple_app",
        full_name="Simple Application",
        console_app=False
    ).run()
