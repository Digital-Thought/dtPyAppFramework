===============
Getting Started
===============

This guide will walk you through creating your first application with dtPyAppFramework, covering basic setup, configuration, and key concepts.

Prerequisites
=============

* Python 3.10 or higher
* pip (Python package installer)

Installation
============

Install dtPyAppFramework using pip:

.. code-block:: bash

    pip install dtPyAppFramework

Quick Start
===========

Let's create a simple application to demonstrate the framework's capabilities:

1. Create Your Application
--------------------------

Create a new Python file called ``my_first_app.py``:

.. code-block:: python

    from dtPyAppFramework.application import AbstractApp
    import logging

    class MyFirstApp(AbstractApp):
        def __init__(self):
            super().__init__(
                description="My first dtPyAppFramework application",
                version="1.0.0",
                short_name="myfirstapp",
                full_name="My First Application"
            )

        def define_args(self, arg_parser):
            """Define command-line arguments for your application."""
            arg_parser.add_argument(
                '--message', 
                type=str, 
                default="Hello, Framework!",
                help='Message to display'
            )

        def main(self, args):
            """Main application logic."""
            logger = logging.getLogger(__name__)
            
            logger.info("Application started successfully!")
            print(f"Message: {args.message}")
            
            # Demonstrate configuration access
            from dtPyAppFramework.settings import Settings
            settings = Settings()
            
            # This will use default value since no config exists yet
            timeout = settings.get('application.timeout', 30)
            logger.info(f"Application timeout: {timeout} seconds")

        def exiting(self):
            """Cleanup before exit."""
            import logging
            logging.info("Application shutting down gracefully")

    if __name__ == "__main__":
        app = MyFirstApp()
        app.run()

2. Run Your Application
-----------------------

Run your application:

.. code-block:: bash

    python my_first_app.py
    
    # Or explicitly with --run (optional)
    python my_first_app.py --run

You should see output similar to:

.. code-block:: text

    My First Application (myfirstapp), Version: 1.0.0. Process ID: 12345
    Log Path: /path/to/logs/20231215_143022
    Message: Hello, Framework!

3. Explore Built-in Features
-----------------------------

Try the built-in command-line options:

.. code-block:: bash

    # Display help
    python my_first_app.py --help

    # Initialize framework environment (creates directories)
    python my_first_app.py --init

    # Run with custom message (--run is optional)
    python my_first_app.py --message "Hello, World!"

    # Enable console output
    python my_first_app.py --console

    # You can also use --run explicitly if preferred
    python my_first_app.py --run --message "Hello, World!"

Framework Overview
==================

Your application inherits from ``AbstractApp``, which provides:

**Automatic Framework Integration**
  - Configuration management
  - Logging setup
  - Path management
  - Secrets handling
  - Process coordination

**Built-in Command Line Interface**
  - Standard arguments (``--init``, ``--add_secret``, ``--console``, ``--container``, etc.)
  - ``--run`` is optional (default behavior when no other mode is specified)
  - Container mode support with ``--container`` / ``-c``
  - Custom argument definition
  - Help system

**Default Execution Behavior**
  When you run your application without any arguments, it automatically executes your ``main()`` method. The framework uses this logic:
  
  - If ``--init`` is specified: Initialize environment and exit
  - If ``--add_secret`` is specified: Add secrets and exit
  - If ``--service`` is specified: Run as Windows service
  - Otherwise: Run your application's main logic (equivalent to ``--run``)

**Lifecycle Management**
  - Initialization
  - Main execution
  - Graceful shutdown

Configuration Setup
===================

Create a configuration file to customize your application:

1. Create Configuration Directory
---------------------------------

.. code-block:: bash

    mkdir config

2. Create Configuration File
----------------------------

Create ``config/config.yaml``:

.. code-block:: yaml

    # Application configuration
    application:
      timeout: 60
      debug: false
      name: "My First Application"
      
    # Logging configuration
    logging:
      level: "INFO"
      log_to_console: true
      rotation_backup_count: 5
      
    # Custom application settings
    features:
      enable_notifications: true
      max_concurrent_tasks: 4

3. Use Configuration in Your Application
----------------------------------------

Update your application to use the configuration:

.. code-block:: python

    def main(self, args):
        """Main application logic with configuration."""
        logger = logging.getLogger(__name__)
        
        # Access configuration
        from dtPyAppFramework.settings import Settings
        settings = Settings()
        
        app_name = settings.get('application.name', 'Unknown App')
        timeout = settings.get('application.timeout', 30)
        debug_mode = settings.get('application.debug', False)
        
        logger.info(f"Starting {app_name}")
        logger.info(f"Timeout: {timeout}s, Debug: {debug_mode}")
        
        # Use feature flags
        if settings.get('features.enable_notifications', False):
            logger.info("Notifications enabled")
        
        print(f"Message: {args.message}")

Adding Secrets Management
=========================

1. Initialize Secrets Store
----------------------------

.. code-block:: bash

    python my_first_app.py --init

This creates encrypted local storage for secrets.

2. Add Secrets
--------------

**Interactive Addition:**

.. code-block:: bash

    # Interactive secret addition
    python my_first_app.py --add_secret
    
    # Or specify directly
    python my_first_app.py --add_secret --name "api_key" --value "secret_value"

**Bulk Import via YAML:**

For bulk secret import, create a ``secrets.yaml`` file in your keystore directory:

.. code-block:: yaml

    secrets:
      - name: "database_password"
        value: "my_secure_password"
      - name: "api_key" 
        value: "abc123xyz789"
      - name: "ssl_cert"
        file: "/path/to/certificate.pem"
        store_as: "raw"

Then run your application - secrets are automatically imported and the YAML file is deleted:

.. code-block:: bash

    python my_first_app.py

**Note:** The framework automatically manages keystore format upgrades. If you have existing v2keystore files, they will be automatically migrated to the more secure v3keystore format, with your original keystore backed up as ``v2keystore_old``.

3. Use Secrets in Configuration
-------------------------------

Update your ``config/config.yaml``:

.. code-block:: yaml

    application:
      timeout: 60
      debug: false
      
    # Reference secrets using SEC/ prefix
    external_api:
      base_url: "https://api.example.com"
      api_key: "SEC/api_key"  # Retrieved from secrets store
      
    database:
      host: "localhost"
      username: "app_user"
      password: "SEC/database_password"

4. Access Secrets in Application
--------------------------------

.. code-block:: python

    def main(self, args):
        """Main application logic with secrets."""
        logger = logging.getLogger(__name__)
        
        from dtPyAppFramework.settings import Settings
        settings = Settings()
        
        # Secrets are automatically resolved
        api_key = settings.get('external_api.api_key')  # Gets secret value
        db_password = settings.get('database.password')  # Gets secret value
        
        logger.info("Retrieved secrets successfully")
        # Never log actual secret values!

Adding Multiprocessing
======================

Enhance your application with multiprocessing capabilities:

.. code-block:: python

    from dtPyAppFramework.application import AbstractApp
    from dtPyAppFramework.process import MultiProcessingManager
    import logging
    import time

    class MultiProcessApp(AbstractApp):
        def __init__(self):
            super().__init__(
                description="Multi-processing example application",
                version="1.0.0",
                short_name="multiapp",
                full_name="Multi-Processing Application"
            )

        def define_args(self, arg_parser):
            arg_parser.add_argument(
                '--workers', 
                type=int, 
                default=2,
                help='Number of worker processes'
            )
            arg_parser.add_argument(
                '--tasks', 
                type=int, 
                default=10,
                help='Number of tasks to process'
            )

        def main(self, args):
            logger = logging.getLogger(__name__)
            logger.info(f"Starting with {args.workers} workers")

            # Create multiprocessing job
            manager = MultiProcessingManager()
            job = manager.new_multiprocessing_job(
                job_name="data_processing",
                worker_count=args.workers,
                target=self.process_task,
                args=(args.tasks,)
            )

            # Start processing
            job.start()
            
            # Wait for completion
            job.join()
            
            logger.info("All workers completed")

        def process_task(self, task_count):
            """Function executed by worker processes."""
            import logging
            
            # Each worker has its own logging context
            logger = logging.getLogger(__name__)
            logger.info(f"Worker processing {task_count} tasks")
            
            # Simulate work
            for i in range(task_count):
                time.sleep(0.1)  # Simulate processing
                if i % 5 == 0:
                    logger.info(f"Completed task {i}")
            
            logger.info("Worker finished")

        def exiting(self):
            import logging
            logging.info("Application shutdown complete")

Development vs Production
=========================

The framework automatically adapts to different environments:

Development Mode
----------------

Enable development mode for simplified directory structure:

.. code-block:: bash

    # Use single folder for all data (--run is optional)
    python my_first_app.py --single_folder

    # Or set environment variable
    export DEV_MODE=True
    python my_first_app.py

This creates all directories relative to your project:

.. code-block:: text

    your_project/
    ├── logs/           # Application logs
    ├── data/
    │   ├── app/       # Application data
    │   └── usr/       # User data
    ├── temp/          # Temporary files
    └── config/        # Configuration files

Production Mode
---------------

In production, the framework uses system-standard locations:

* **Linux (root)**: ``/var/log/myapp/``, ``/var/lib/myapp/``, ``/etc/myapp/``
* **Linux (user)**: ``~/.local/state/myapp/log/``, ``~/.config/myapp/``, ``~/.local/share/myapp/``
* **Windows**: ``%LOCALAPPDATA%\myapp\``, ``%APPDATA%\myapp\``
* **macOS**: ``~/Library/Logs/myapp/``, ``~/Library/Application Support/myapp/``

Container Mode
--------------

For containerized deployments (Docker, Kubernetes), use container mode:

.. code-block:: bash

    # Enable container mode with command line
    python my_first_app.py --container
    
    # Or set environment variable
    export CONTAINER_MODE=true
    python my_first_app.py

Container mode creates a simplified directory structure in the working directory:

.. code-block:: text

    container_workdir/
    ├── config/         # Single configuration layer
    ├── data/           # Unified data directory
    │   ├── keystore/   # Secret storage
    │   └── resources/  # Application resources
    ├── logs/           # All log files
    └── temp/           # Temporary files

**Key Container Mode Benefits:**
- **Single Config Layer**: Only ``./config/config.yaml`` is used
- **Volume Mount Ready**: Perfect for persistent volume mounting
- **Auto-Detection**: Automatically enabled in Docker/Kubernetes environments
- **Simplified**: No multi-user directory complexity

**Container Example:**

.. code-block:: dockerfile

    FROM python:3.12-slim
    WORKDIR /app
    COPY requirements.txt .
    RUN pip install -r requirements.txt
    COPY . .
    ENV CONTAINER_MODE=true
    CMD ["python", "my_first_app.py"]

Next Steps
==========

Now that you have a basic application running, explore these topics:

1. **Configuration Management**: :doc:`../components/configuration` - Advanced configuration patterns and container mode
2. **Secrets Management**: :doc:`../components/secrets-management` - Cloud and local secrets
3. **Container Mode**: :doc:`../components/paths-resources` - Paths and containerization details
4. **Logging System**: :doc:`../components/logging` - Advanced logging patterns
5. **Multiprocessing**: :doc:`../components/multiprocessing` - Scaling across multiple processes
6. **Cloud Integration**: :doc:`../components/cloud-integration` - AWS and Azure integration

**Sample Applications:**
- :doc:`../../samples/container_mode/README` - Complete container deployment examples
- :doc:`../../samples/simple_app/README` - Basic application patterns
- :doc:`../../samples/multiprocessing/README` - Advanced parallel processing

Common Patterns
===============

Here are some common patterns you'll use:

Accessing Framework Components
------------------------------

.. code-block:: python

    def main(self, args):
        # AppContext (unified access - recommended)
        from dtPyAppFramework.app_context import AppContext
        ctx = AppContext()

        # Settings (configuration and secrets)
        from dtPyAppFramework.settings import Settings
        settings = Settings()
        
        # Paths (cross-platform directory management)
        from dtPyAppFramework.paths import ApplicationPaths
        paths = ApplicationPaths()
        
        # Resources (asset management)
        from dtPyAppFramework.resources import ResourceManager
        resources = ResourceManager()
        
        # Multiprocessing (if needed)
        from dtPyAppFramework.process import MultiProcessingManager
        mp_manager = MultiProcessingManager()

AppContext Unified Access
--------------------------

The ``AppContext`` singleton provides convenient unified access to all framework components:

.. code-block:: python

    def main(self, args):
        from dtPyAppFramework.app_context import AppContext

        ctx = AppContext()

        # Application metadata
        print(f"Version: {ctx.version}")
        print(f"Name: {ctx.full_name}")

        # Paths
        print(f"Logs: {ctx.logging_path}")
        print(f"Data: {ctx.app_data_path}")

        # Settings and secrets
        timeout = ctx.get_setting('app.timeout', 30)
        api_key = ctx.get_secret('api_key')

        # Resources
        template = ctx.get_resource_path('templates/email.html')

Error Handling
--------------

.. code-block:: python

    def main(self, args):
        logger = logging.getLogger(__name__)
        
        try:
            # Your application logic
            self.do_application_work(args)
        except Exception as ex:
            logger.exception("Unexpected error occurred")
            # Framework handles cleanup automatically
            raise

Configuration Validation
-------------------------

.. code-block:: python

    def validate_configuration(self):
        """Validate required configuration settings."""
        from dtPyAppFramework.settings import Settings
        settings = Settings()
        
        required_settings = [
            'application.timeout',
            'external_api.base_url'
        ]
        
        missing_settings = []
        for setting in required_settings:
            if settings.get(setting) is None:
                missing_settings.append(setting)
        
        if missing_settings:
            raise ValueError(f"Missing required settings: {missing_settings}")

    def main(self, args):
        # Validate configuration before proceeding
        self.validate_configuration()
        
        # Continue with application logic
        ...

This guide provides the foundation for building applications with dtPyAppFramework. The framework handles the complexity of configuration, logging, path management, and process coordination, allowing you to focus on your application's business logic.