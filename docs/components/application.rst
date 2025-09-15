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

**Lifecycle Methods**
  Applications must implement these abstract methods:
  
  * ``define_args(arg_parser)``: Define command-line arguments
  * ``main(args)``: Main application logic
  * ``exiting()``: Cleanup logic before shutdown

**Built-in Command Line Arguments**
  The framework provides several built-in command-line arguments:
  
  * ``--init``: Initialize environment and secrets
  * ``--add_secret``: Add secrets to the secret store
  * ``--run``: Run the main application (default behavior if no other mode specified)
  * ``--service``: Run as a Windows service
  * ``--console``: Enable console output
  * ``--single_folder``: Keep all directories in a single folder (development mode)
  * ``--container`` / ``-c``: Enable container mode with simplified directory structure
  * ``--working_dir``: Set the working directory
  
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

**Service Integration**
  * Windows service support through pywin32
  * Service installation and management
  * Console and service mode switching

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