=====================
Application Framework
=====================

The Application Framework provides the foundation for creating robust Python applications through the ``AbstractApp`` base class and ``ProcessManager`` system.

Overview
========

The framework follows a structured approach where applications inherit from ``AbstractApp``, which automatically orchestrates:

* Configuration loading and merging
* Secrets store initialization
* Logging setup
* Path management
* Command-line argument processing
* Process lifecycle management

Core Components
===============

AbstractApp Base Class
-----------------------

The ``AbstractApp`` class serves as the foundation for all applications built with dtPyAppFramework.

.. autoclass:: dtPyAppFramework.application.AbstractApp
   :members:
   :inherited-members:

Key Features:

**Application Metadata**
  Applications define their metadata through constructor parameters:
  
  * ``description``: A short description of the application
  * ``version``: The application version
  * ``short_name``: Short name or abbreviation
  * ``full_name``: Full descriptive name
  * ``console_app``: Whether the application runs in console mode

  .. note::

     Metadata can also be auto-discovered from text files in the subclass's package directory.
     If constructor arguments are omitted, ``AbstractApp`` looks for ``_version.txt``,
     ``_short_name.txt``, ``_full_name.txt``, and ``_description.txt`` files alongside the
     subclass module.

**Lifecycle Methods**
  Applications must implement these abstract methods:
  
  * ``define_args(arg_parser)``: Define command-line arguments
  * ``main(args)``: Main application logic
  * ``exiting()``: Cleanup logic before shutdown

**Built-in Command Line Arguments**
  The framework provides several built-in command-line arguments:

  * ``--init``: Initialise environment and secrets
  * ``--add_secret``: Add secrets to the secret store
  * ``--run``: Run the main application (default behaviour if no other mode specified)
  * ``--service``: Run as a Windows service
  * ``--console``: Enable console output
  * ``--single_folder``: Keep all directories in a single folder (development mode)
  * ``--container`` / ``-c``: Enable container mode with simplified directory structure
  * ``--working_dir``: Set the working directory
  * ``--password`` / ``-p``: Set keystore password (sets ``KEYSTORE_PASSWORD`` environment variable)

  **Note**: The ``--run`` argument is optional. If no specific mode (``--init``, ``--add_secret``, or ``--service``) is specified, the application runs in normal mode by default.

ProcessManager
--------------

The ``ProcessManager`` class handles application initialization and execution, including multiprocessing coordination.

.. autoclass:: dtPyAppFramework.process.ProcessManager
   :members:

Key Features:

**Application Initialization**
  * Initializes all framework components in correct order
  * Sets up logging with cross-process coordination
  * Configures paths and settings
  * Handles spawned process initialization

**Signal Handling**
  * Handles SIGINT and SIGTERM for graceful shutdown
  * Provides cleanup coordination
  * Manages exit procedures

**Shutdown Methods**
  * ``request_shutdown()``: Signal the application to shut down gracefully
  * ``wait_for_shutdown()``: Block until shutdown is requested (for long-running apps)
  * ``handle_shutdown()``: Internal cleanup method (called automatically)

**Service Integration**
  * Windows service support through pywin32
  * Service installation and management
  * Console and service mode switching

AppContext
----------

The ``AppContext`` class provides a unified facade for accessing application metadata, paths, settings, secrets, and resources through a single singleton.

.. autoclass:: dtPyAppFramework.app_context.AppContext
   :members:

Key Features:

**Unified Access**
  Single entry point for all framework components:

  * Application metadata: ``version``, ``full_name``, ``short_name``, ``description``
  * Paths: ``logging_path``, ``app_data_path``, ``usr_data_path``, ``tmp_path``
  * Configuration: ``get_setting()``, ``set_setting()``, ``config_file_paths``
  * Secrets: ``get_secret()``, ``set_secret()``, ``delete_secret()``
  * Resources: ``get_resource_path()``

**Usage Example:**

.. code-block:: python

    from dtPyAppFramework.app_context import AppContext

    ctx = AppContext()

    # Metadata
    print(f"{ctx.full_name} v{ctx.version}")

    # Settings and secrets
    timeout = ctx.get_setting('app.timeout', 30)
    api_key = ctx.get_secret('api_key')

    # Paths and resources
    log_dir = ctx.logging_path
    template = ctx.get_resource_path('templates/report.html')

Implementation Pattern
======================

Basic Application Structure
---------------------------

.. code-block:: python

    from dtPyAppFramework.application import AbstractApp

    class MyApplication(AbstractApp):
        def __init__(self):
            super().__init__(
                description="My Application Description",
                version="1.0.0",
                short_name="myapp",
                full_name="My Application Full Name"
            )

        def define_args(self, arg_parser):
            """Define application-specific command-line arguments."""
            arg_parser.add_argument('--config-file', 
                                   help='Custom configuration file path')
            arg_parser.add_argument('--debug', 
                                   action='store_true',
                                   help='Enable debug mode')

        def main(self, args):
            """Main application logic."""
            import logging
            logger = logging.getLogger(__name__)
            
            logger.info("Application starting...")
            
            # Access configuration
            from dtPyAppFramework.settings import Settings
            settings = Settings()
            database_url = settings.get('database.url', 'sqlite:///default.db')
            
            # Your application logic here
            self.run_application_logic(args, settings)

        def exiting(self):
            """Cleanup before exit."""
            import logging
            logging.info("Application shutting down...")
            # Perform cleanup tasks

        def run_application_logic(self, args, settings):
            """Separate method for main application logic."""
            pass

    if __name__ == "__main__":
        app = MyApplication()
        app.run()

Metadata Auto-Discovery
-------------------------

Applications can use file-based metadata instead of passing constructor arguments. Place text files alongside your application module:

.. code-block:: text

    my_package/
    ├── __init__.py
    ├── app.py              # Your AbstractApp subclass
    ├── _version.txt         # Contains: 1.0.0
    ├── _short_name.txt      # Contains: myapp
    ├── _full_name.txt       # Contains: My Application
    └── _description.txt     # Contains: A sample application

.. code-block:: python

    from dtPyAppFramework.application import AbstractApp

    class MyApplication(AbstractApp):
        def __init__(self):
            # No metadata arguments needed — auto-discovered from text files
            super().__init__()

        def define_args(self, arg_parser):
            pass

        def main(self, args):
            # Metadata is available via self or AppContext
            from dtPyAppFramework.app_context import AppContext
            ctx = AppContext()
            print(f"Running {ctx.full_name} v{ctx.version}")

        def exiting(self):
            pass

Application Lifecycle Patterns
------------------------------

The framework supports two primary application patterns:

**One-Shot Applications**

One-shot applications perform their work in ``main()`` and then exit automatically.
Simply return from your ``main()`` method - the framework handles cleanup.

.. code-block:: python

    class OneShotApp(AbstractApp):
        def main(self, args):
            # Do your work
            process_data()
            generate_report()

            # Just return - framework handles shutdown automatically
            # No need to call request_shutdown() or handle_shutdown()

        def exiting(self):
            logging.info('Cleanup complete')

**Long-Running Applications (Daemons/Services)**

Long-running applications start background services and wait for a shutdown signal.
Use ``ProcessManager().wait_for_shutdown()`` to block until shutdown is requested.

.. code-block:: python

    from dtPyAppFramework.process import ProcessManager

    class DaemonApp(AbstractApp):
        def main(self, args):
            # Start background services
            self.start_http_server()
            self.start_worker_threads()

            logging.info('Services started, waiting for shutdown signal...')

            # Block until Ctrl+C, SIGTERM, or request_shutdown() is called
            ProcessManager().wait_for_shutdown()

            # After wait_for_shutdown() returns, stop services
            self.stop_services()

        def exiting(self):
            logging.info('Daemon shutdown complete')

**Programmatic Shutdown**

For long-running applications, you can trigger shutdown programmatically:

.. code-block:: python

    from dtPyAppFramework.process import ProcessManager

    # From anywhere in your application (e.g., REST endpoint, scheduled task)
    ProcessManager().request_shutdown()

**Shutdown Flow**

1. Shutdown signal received (SIGINT, SIGTERM, or ``request_shutdown()`` call)
2. ``wait_for_shutdown()`` returns (if called)
3. ``main()`` method completes
4. ``exiting()`` callback is executed
5. Framework performs final cleanup

Console vs Service Mode
-----------------------

The framework supports both console and service modes:

**Console Mode**
  * Direct execution with console output
  * Interactive command-line interface
  * Suitable for development and interactive use

**Service Mode** (Windows only)
  * Background service execution
  * Automatic startup capability
  * Service installation and management
  * Logging to files instead of console

.. code-block:: python

    # Run in console mode
    python myapp.py --console

    # Install and run as Windows service
    python myapp.py --service --install

Framework Integration
=====================

The ``AbstractApp`` automatically integrates with all framework components:

**Settings Integration**
  * Automatic settings loading from configuration hierarchy
  * Environment variable and secrets resolution
  * Configuration file watching and hot-reload

**Logging Integration**
  * Structured logging with process identification
  * Cross-process log coordination
  * File and console output management

**Secrets Management**
  * Automatic secrets store loading
  * Multi-cloud secrets access
  * Local encrypted secrets support

**Path Management**
  * Cross-platform path handling
  * Automatic directory creation
  * Development and production mode support

**Multiprocessing Support**
  * Spawned process coordination
  * Shared configuration and secrets
  * Inter-process communication

Error Handling
==============

The framework provides structured error handling:

.. code-block:: python

    class MyApplication(AbstractApp):
        def main(self, args):
            try:
                # Application logic
                pass
            except Exception as ex:
                import logging
                logging.exception("Application error occurred")
                # Framework handles cleanup automatically
                raise

Best Practices
==============

1. **Separation of Concerns**: Keep application logic separate from framework initialization
2. **Configuration-Driven**: Use configuration files instead of hard-coded values  
3. **Logging**: Use structured logging throughout the application
4. **Error Handling**: Implement proper exception handling and cleanup
5. **Resource Management**: Use context managers and proper resource cleanup
6. **Testing**: Design for testability with dependency injection

Deployment Modes
================

The framework automatically detects and handles different deployment modes:

Container Mode
--------------

Container mode provides a simplified directory structure optimized for containerized deployments (Docker, Kubernetes, etc.):

**Activation**
  Container mode can be enabled through:
  
  * Command line: ``--container`` or ``-c``
  * Environment variable: ``CONTAINER_MODE=true``
  * Auto-detection: Framework detects Docker (``/.dockerenv``) or Kubernetes (``KUBERNETES_SERVICE_HOST``)

**Directory Structure**
  In container mode, all directories are created within the working directory:
  
  .. code-block::
  
      /working_directory/
      ├── config/          # Single configuration layer
      ├── data/           # Unified data directory
      │   ├── keystore/   # Secret storage
      │   └── resources/  # Application resources
      ├── logs/           # All log files
      └── temp/           # Temporary files

**Key Differences from Standard Mode**
  * **Single Config Layer**: Only ``./config/config.yaml`` is used (no user/system layers)
  * **Working Directory Based**: All paths relative to application working directory
  * **Volume Mount Friendly**: Designed for persistent volume mounting in containers
  * **Simplified Permissions**: No complex permission handling for multi-user scenarios

**Usage Example**
  .. code-block:: python
  
      # Enable container mode
      python myapp.py --container
      
      # Or set environment variable
      import os
      os.environ['CONTAINER_MODE'] = 'True'
      app.run()
      
      # Auto-detection in containers
      if os.path.exists('/.dockerenv'):
          # Container mode automatically enabled
          pass

Development Mode
----------------

**Activation**
  * Triggered by ``DEV_MODE`` environment variable or ``--single_folder`` argument
  * All data directories created relative to current working directory
  * Simplified path structure for development

Production Mode
---------------

**Standard Production Mode**
  * Uses platform-specific standard locations
  * Proper separation of logs, configuration, and data
  * Enhanced security and isolation
  * Multi-tier configuration system

Advanced Features
=================

**Spawned Process Support**
  Applications can spawn child processes that inherit the framework configuration:

.. code-block:: python

    def main(self, args):
        from dtPyAppFramework.process import MultiProcessingManager
        manager = MultiProcessingManager()
        
        job = manager.new_multiprocessing_job(
            job_name="data_processing",
            worker_count=4,
            target=self.process_data,
            args=(data_batch,)
        )
        job.start()

**Secret Management Integration**
  Direct access to secrets within application code:

.. code-block:: python

    def main(self, args):
        from dtPyAppFramework.settings import Settings
        settings = Settings()
        
        # Access secrets through settings
        api_key = settings.get('SEC/api_key')
        database_password = settings.get('SEC/database.password')

This comprehensive application framework provides a solid foundation for building enterprise-grade Python applications with built-in best practices and cross-platform support.