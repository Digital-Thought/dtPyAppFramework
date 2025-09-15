import argparse
import logging
import os
import sys

import psutil
import traceback

from multiprocessing import current_process
from argparse import ArgumentParser
from contextlib import redirect_stdout, redirect_stderr

# Importing modules from the same package
from . import logging as app_logging
from . import paths
from . import settings
from . import resources
from .decorators import singleton
from .process import ProcessManager


class AbstractApp(object):
    """
    An abstract base class for creating applications.

    Attributes:
        app_spec (dict): A dictionary containing application information.
        console_app (bool): Indicates whether the application is a console application.
        process_manager (ProcessManager): Manages the application process.
    """

    def __init__(self, description, version, short_name, full_name, console_app=True) -> None:
        """
        Initialize the AbstractApp.

        Args:
            description (str): A short description of the application.
            version (str): The version of the application.
            short_name (str): Short name or abbreviation of the application.
            full_name (str): Full name of the application.
            console_app (bool, optional): Indicates whether the application is a console application (default is True).
        """
        self.app_spec = {
            'description': description,
            'version': version,
            'short_name': short_name,
            'full_name': full_name
        }


        self.console_app = console_app or ('--console' in sys.argv)
        # Note: '-c' is now reserved for --container mode
        self.process_manager = None
        super().__init__()

    @property
    def version(self) -> str:
        """Get the version of the application."""
        return self.app_spec["version"]

    @property
    def description(self) -> str:
        """Get the description of the application."""
        return self.app_spec["description"]

    @property
    def short_name(self) -> str:
        """Get the short name of the application."""
        return self.app_spec["short_name"]

    @property
    def full_name(self) -> str:
        """Get the full name of the application."""
        return self.app_spec["full_name"]

    def define_args(self, arg_parser: ArgumentParser):
        """
        Define command-line arguments for the application.

        Args:
            arg_parser (ArgumentParser): The ArgumentParser object for defining command-line arguments.
        """
        raise NotImplementedError

    def main(self, args):
        """
        The main procedure of the application.

        Args:
            args: Command-line arguments passed to the application.
        """
        raise NotImplementedError

    def exiting(self):
        raise NotImplementedError

    def __define_args(self, arg_parser: ArgumentParser):
        """
        Define command-line arguments based on application state.

        Args:
            arg_parser (ArgumentParser): The ArgumentParser object for defining command-line arguments.
        """
        # Common arguments for various states
        arg_parser.add_argument('--init', action='store_true', required=False, help='Initialise environment')
        arg_parser.add_argument('--add_secret', action='store_true', required=False, help='Add secret to store')
        arg_parser.add_argument('--run', action='store_true', required=False, help='Run Processor')
        arg_parser.add_argument('--service', action='store_true', required=False, help='Run as Service')
        arg_parser.add_argument('--console', action='store_true', required=False, help='Output to Console')
        arg_parser.add_argument('--container', '-c', action='store_true', required=False, help='Enable container mode with simplified directory structure')
        arg_parser.add_argument('--single_folder', action='store_true', required=False, help='Keeps all Directories in a single folder')
        arg_parser.add_argument('--working_dir', action='store', type=str, required=False, help="Sets the Working Directory")

        self.define_args(arg_parser)
        # Check specific states and add corresponding arguments
        opts, rem_args = arg_parser.parse_known_args()

        if opts.working_dir:
            os.chdir(opts.working_dir)

        if opts.single_folder:
            os.environ['DEV_MODE'] = "True"

        # Set container mode based on command line argument or environment variable
        if opts.container or os.environ.get('CONTAINER_MODE', '').lower() in ('true', '1', 'yes'):
            os.environ['CONTAINER_MODE'] = "True"

        if opts.service:
            arg_parser.add_argument('--install', action='store_true')

        if opts.init:
            arg_parser.add_argument('--password', action='store', type=str, required=False,
                                    help="Secrets Store password")
        elif opts.add_secret:
            arg_parser.add_argument('--name', action='store', type=str, required=False, help="Secret Name")

            group = arg_parser.add_mutually_exclusive_group(required=False)
            group.add_argument('--value', action='store', type=str, help="Secret Value")
            group.add_argument('--file', action='store', type=str, help="File to add to secret")

            arg_parser.add_argument('--store_as', action='store', type=str, default='raw', choices=['raw', 'base64'],
                                    help="Store file as either base64 or raw")

    def exit(self):
        self.exiting()
        from dtPyAppFramework.settings import Settings
        Settings().close()

    def run(self):
        """
        Run the application.
        """
        arg_parser = argparse.ArgumentParser(prog=self.app_spec["short_name"], description=self.app_spec["description"])
        self.__define_args(arg_parser)
        self.process_manager = ProcessManager(description=self.description, version=self.version,
                                              short_name=self.short_name, full_name=self.full_name,
                                              console_app=self.console_app, main_procedure=self.main,
                                              exit_procedure=self.exit)
        self.process_manager.initialise_application(arg_parser)
