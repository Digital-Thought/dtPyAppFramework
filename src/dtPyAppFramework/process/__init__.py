from ..decorators import singleton
from .. import logging as app_logging
from .. import paths
from .. import settings
from .. import resources
from multiprocessing import current_process
from argparse import ArgumentParser
from .multiprocessing import MultiProcessingManager
import platform
import sys
import os
import logging
import base64
import threading
import signal
import time

if platform.system() == "Windows":
    try:
        from dtPyAppFramework.process.windows_service import call_service
    except ImportError as ex:
        logging.error("pywin32 is not installed.")
        raise ex


def is_multiprocess_spawned_instance():
    """
    Check if the current process is a spawned instance in a multiprocessing environment.

    Returns:
        bool: True if the process is a spawned instance, False otherwise.
    """
    return current_process().name != "MainProcess"


@singleton()
class ProcessManager():
    """
    Singleton class for managing the initialization and execution of a multiprocessing-enabled application.

    Attributes:
        description (str): Application description.
        version (str): Application version.
        short_name (str): Short name or abbreviation of the application.
        full_name (str): Full name of the application.
        console_app (bool): True if the application is a console app, False otherwise.
        main_procedure (callable): Main procedure to be executed.
        application_paths (ApplicationPaths): Object managing application paths.
        application_settings (Settings): Object managing application settings.
        secrets_manager (SecretsManager): Object managing secrets.
        resource_manager (ResourceManager): Object managing application resources.
        log_path (str): Path to the log folder.
        multiprocessing_manager (MultiProcessingManager): Manager for multiprocessing functionality.
        stdout_txt_file (file): File object for capturing stdout to a text file.
        stderr_txt_file (file): File object for capturing stderr to a text file.
    """

    def __init__(self, description, version, short_name, full_name, console_app, main_procedure, exit_procedure=None):
        super().__init__()
        # Initialization of attributes
        self.description = description
        self.version = version
        self.short_name = short_name
        self.full_name = full_name
        self.console_app = console_app
        self.application_paths = None
        self.application_settings = None
        self.secrets_manager = None
        self.resource_manager = None
        self.log_path = None
        self.main_procedure = main_procedure
        self.exit_procedure = exit_procedure
        self.multiprocessing_manager = None
        self.stdout_txt_file = None
        self.stderr_txt_file = None
        self.running = threading.Event()

    def __initialise_spawned_application__(self, parent_log_path, job_id, worker_id, job_name, pipe_registry):
        """
        Initialize a spawned instance of the application in a multiprocessing environment.

        Args:
            parent_log_path (str): Path to the parent log folder for spawned processes.
            job_id (int): Job ID for the spawned process.
            worker_id (int): Worker ID for the spawned process.
            job_name (str): Name of the spawned job.
        """
        try:
            if is_multiprocess_spawned_instance():
                self.application_paths = paths.ApplicationPaths(app_short_name=self.short_name,
                                                                spawned_instance=True, worker_id=worker_id)
                self.application_settings = settings.Settings(application_paths=self.application_paths,
                                                              app_short_name=self.short_name)
                self.resource_manager = resources.ResourceManager(application_paths=self.application_paths)
                self.log_path = app_logging.initialise_logging(redirect_console=not self.console_app,
                                                               spawned_process=True,
                                                               job_id=job_id, worker_id=worker_id,
                                                               parent_log_path=parent_log_path)
                self.application_settings.init_settings_readers(pipe_registry=pipe_registry)
                self.application_settings.secret_manager.load_cloud_stores()

                self.__initialise_stdout_capt__()

                header_message = f'SPAWNED PROCESS --- {self.full_name} ({self.short_name}), ' \
                                 f'Version: {self.version}. '
                logging.info(header_message)
                print(header_message)

                self.load_config()


        except Exception as ex:
            logging.exception(ex)
            if not self.console_app:
                self.stdout_txt_file.close()
                self.stderr_txt_file.close()

    def __initialise_stdout_capt__(self):
        """
        Initialize capturing of stdout to a text file.
        """
        if not self.console_app:
            stdout_txt = '{}/stdout.txt'.format(self.log_path, self.application_paths.app_short_name)
            stderr_txt = '{}/stderr.txt'.format(self.log_path, self.application_paths.app_short_name)

            self.stdout_txt_file = open(stdout_txt, mode='w', buffering=1)
            self.stderr_txt_file = open(stderr_txt, mode='w', buffering=1)
            sys.stdout = self.stdout_txt_file
            sys.stderr = self.stderr_txt_file

    def initialise_application(self, arg_parser):
        """
        Initialize the application based on command-line arguments.

        Args:
            arg_parser (ArgumentParser): Command-line argument parser.
        """
        self.multiprocessing_manager = MultiProcessingManager()
        try:
            if not is_multiprocess_spawned_instance():
                self.application_paths = paths.ApplicationPaths(app_short_name=self.short_name)
                self.application_settings = settings.Settings(application_paths=self.application_paths)
                self.application_settings.init_settings_readers()
                self.resource_manager = resources.ResourceManager(application_paths=self.application_paths)
                self.log_path = app_logging.initialise_logging(redirect_console=not self.console_app)
                #self.application_settings.init_settings_readers()
                self.application_settings.secret_manager.load_cloud_stores()
                self.__initialise_stdout_capt__()

                header_message = f'{self.full_name} ({self.short_name}), ' \
                                 f'Version: {self.version}. Process ID: {os.getpid()}'
                logging.info(header_message)
                print(header_message)
                if self.log_path is not None:
                    print(f'Log Path: {self.log_path}')
                    self.multiprocessing_manager.set_log_path(self.log_path)
                args = arg_parser.parse_args()

                if args.add_secret:
                    self.__add_secret__(args)
                elif args.service:
                    if platform.system() == "Windows":
                        sys.argv = [sys.argv[0]]
                        call_service(svc_name=self.short_name, svc_display_name=self.full_name,
                                     svc_description=self.description, main_function=self.__main__,
                                     exit_function=self.call_shutdown)

                else:
                    signal.signal(signal.SIGINT, self.call_shutdown)
                    signal.signal(signal.SIGTERM, self.call_shutdown)
                    self.__main__(args)

        except KeyboardInterrupt as kbi:
            logging.warning('(KeyboardInterrupt) Exiting application.')
        except Exception as ex:
            logging.exception(str(ex))

    def load_config(self):
        """
        Load configuration settings for the application.
        """
        if not is_multiprocess_spawned_instance():
            self.application_paths.log_paths()

    def __add_secret__(self, args):
        """
        Add a secret to the application's secrets manager.

        Args:
            args: Parsed command-line arguments.
        """
        try:
            name = args.name
            value = None
            if args.value:
                value = args.value
            if args.file:
                file_path = args.file
                if not os.path.exists(file_path):
                    raise FileNotFoundError(f'The file "{file_path}" could not be found.')

                if args.store_as == 'raw':
                    with open(file_path, 'r') as file:
                        file_content = file.read()
                    value = file_content
                elif args.store_as == 'base64':
                    with open(file_path, 'rb') as file:
                        file_content = file.read()
                    value = base64.b64encode(file_content).decode('utf-8')
                else:
                    raise ValueError(f'Invalid store_as value: {args.store_as}')

            if value is None:
                raise ValueError(f'No "value" was specified for {name}')

            settings.SecretsManager().set_secret(name, value)
            logging.info(f'Added secret "{name}" to Secret Store.')
            settings.Settings().close()
        except Exception as ex:
            logging.error(f'Error occurred while adding secret {args.name}.  Error: {str(ex)}')
            raise ex

    def handle_shutdown(self):
        if self.exit_procedure:
            self.exit_procedure()
        if not self.console_app:
            self.stdout_txt_file.close()
            self.stderr_txt_file.close()

    def call_shutdown(self, signum=None, frame=None):
        self.running.clear()

    def __main__(self, args):
        """
        Execute the main procedure of the application.

        Args:
            args: Parsed command-line arguments.
        """
        self.running.set()
        self.load_config()
        self.main_procedure(args)

        while self.running.is_set():
            time.sleep(0.5)

        self.handle_shutdown()


