==============
Logging System
==============

The Logging System provides sophisticated logging capabilities with cross-process coordination, nested contexts for spawned processes, color-coded console output, and automatic log rotation with centralized configuration.

Overview
========

dtPyAppFramework's logging system is designed for complex applications that use multiprocessing and require coordinated logging across parent and child processes. Key features include:

* **Cross-Process Coordination**: Synchronized logging between parent and spawned processes
* **Nested Process Context**: Each spawned process gets its own log namespace and files
* **Color-Coded Console Output**: Enhanced readability with colorlog integration
* **Automatic Log Rotation**: Time-stamped directories with configurable retention
* **Centralized Configuration**: Single point of configuration for all logging needs
* **Hot Configuration Reload**: Dynamic logging configuration changes without restart

Architecture
============

The logging system consists of several key components:

**Logging Initialization**
  * Automatic setup during application startup
  * Detection of main vs. spawned process context
  * Configuration loading and application

**Default Configuration**
  * Built-in sensible defaults for immediate use
  * File and console handler configuration
  * Process-specific log file naming

**File Organization**
  * Timestamp-based log directories
  * Process-specific subdirectories for spawned processes
  * Automatic cleanup of old log directories

Core Functions
==============

Logging Initialization
----------------------

.. py:function:: dtPyAppFramework.logging.initialise_logging(spawned_process=False, job_id=None, worker_id=None, parent_log_path=None)

   Initialize logging configuration for main or spawned processes.

   :param bool spawned_process: Whether this is a spawned process
   :param int job_id: Job identifier for spawned processes
   :param int worker_id: Worker identifier for spawned processes  
   :param str parent_log_path: Path to parent process log directory
   :return: Absolute path to log directory if using default config
   :rtype: str or None

**Main Process Initialization:**

.. code-block:: python

    from dtPyAppFramework import logging as app_logging
    
    # Automatically called by framework during app startup
    log_path = app_logging.initialise_logging()
    # Returns: /path/to/logs/20231215_143022/

**Spawned Process Initialization:**

.. code-block:: python

    # Called automatically by framework for spawned processes
    log_path = app_logging.initialise_logging(
        spawned_process=True,
        job_id=123,
        worker_id=1,
        parent_log_path="/path/to/parent/logs/20231215_143022"
    )
    # Returns: /path/to/parent/logs/20231215_143022/job-123/1/

Log Configuration Management
----------------------------

.. py:function:: dtPyAppFramework.logging.get_logging_config(logging_source=None)

   Retrieve logging configuration from various sources.

   :param str logging_source: Path to custom logging configuration file
   :return: Tuple of (source_path, config_dict)
   :rtype: tuple

**Configuration Priority:**
1. Custom logging source (if specified)
2. User data directory: ``<user_data>/loggingConfig.yaml``
3. Application data directory: ``<app_data>/loggingConfig.yaml``  
4. Working directory: ``./config/loggingConfig.yaml``
5. Built-in default configuration

Log Directory Management
------------------------

.. py:function:: dtPyAppFramework.logging.purge_old_logs(log_path, rotation_backup_count)

   Remove old log directories based on retention policy.

   :param str log_path: Path to main logging directory
   :param int rotation_backup_count: Number of log directories to retain

**Automatic Cleanup:**
- Identifies timestamped directories (format: ``YYYYMMDD_HHMMSS``)
- Sorts by timestamp (newest first)
- Removes directories beyond retention limit
- Logs cleanup operations

Job Management for Multiprocessing
-----------------------------------

.. py:function:: dtPyAppFramework.logging.new_job()

   Generate a unique job ID for multiprocessing scenarios.

   :return: New job identifier
   :rtype: int

**Job ID Generation Logic:**
- Scans existing job directories
- Finds next available job number
- Handles concurrent job creation
- Includes stale job cleanup (jobs older than 10 seconds)

Configuration System
====================

Default Configuration
----------------------

The framework provides a built-in default configuration that can be customized:

.. code-block:: yaml

    version: 1
    disable_existing_loggers: false
    
    formatters:
      detailed:
        format: '%(asctime)s - %(levelname)-8s - %(processName)s.%(process)d - %(threadName)s.%(thread)d - %(module)s.%(funcName)s.%(lineno)-3d - %(message)s'
      simple:
        format: '%(levelname)s - %(message)s'
    
    handlers:
      console_ALL:
        class: logging.StreamHandler
        level: DEBUG
        formatter: detailed
        stream: ext://sys.stdout
      
      logfile_ALL:
        class: logging.handlers.RotatingFileHandler
        level: INFO
        formatter: detailed
        filename: ''  # Set dynamically
        maxBytes: 10485760  # 10MB
        backupCount: 5
      
      logfile_ERR:
        class: logging.handlers.RotatingFileHandler
        level: ERROR
        formatter: detailed
        filename: ''  # Set dynamically
        maxBytes: 10485760  # 10MB
        backupCount: 5
    
    loggers:
      defaultLogger:
        level: INFO
        handlers: [logfile_ALL, logfile_ERR]
        propagate: false
      
      console:
        level: DEBUG
        handlers: [console_ALL]
        propagate: false
    
    root:
      level: INFO
      handlers: [logfile_ALL, logfile_ERR]

Custom Configuration
--------------------

Create custom logging configuration files:

**loggingConfig.yaml:**

.. code-block:: yaml

    version: 1
    disable_existing_loggers: false
    
    formatters:
      production:
        format: '%(asctime)s [%(process)d] [%(levelname)s] %(name)s: %(message)s'
        datefmt: '%Y-%m-%d %H:%M:%S'
      
      development:
        format: '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
    
    handlers:
      file_handler:
        class: logging.handlers.TimedRotatingFileHandler
        level: INFO
        formatter: production
        filename: '/var/log/myapp/application.log'
        when: 'midnight'
        interval: 1
        backupCount: 30
      
      error_handler:
        class: logging.handlers.TimedRotatingFileHandler
        level: ERROR
        formatter: production
        filename: '/var/log/myapp/error.log'
        when: 'midnight'
        interval: 1
        backupCount: 30
      
      debug_handler:
        class: logging.FileHandler
        level: DEBUG
        formatter: development
        filename: '/var/log/myapp/debug.log'
    
    loggers:
      myapp:
        level: INFO
        handlers: [file_handler, error_handler]
        propagate: false
      
      myapp.database:
        level: DEBUG
        handlers: [debug_handler]
        propagate: false
    
    root:
      level: WARNING
      handlers: [file_handler]

Configuration Integration
=========================

Settings-Based Configuration
-----------------------------

Control logging behavior through application configuration:

.. code-block:: yaml

    # config.yaml
    logging:
      level: "INFO"                    # Default log level
      log_to_console: true             # Enable console output
      rotation_backup_count: 10        # Number of old log dirs to keep
      color_console: true              # Enable colored console output
      
    # Override specific logger levels
    loggers:
      database_operations:
        level: "DEBUG"
      external_api:
        level: "WARNING"

**Programmatic Access:**

.. code-block:: python

    from dtPyAppFramework.settings import Settings
    import logging
    
    settings = Settings()
    
    # Get configured log level
    log_level = settings.get('logging.level', 'INFO')
    
    # Configure specific loggers
    database_logger = logging.getLogger('database_operations')
    database_logger.setLevel(settings.get('loggers.database_operations.level', 'INFO'))

Cross-Process Logging
=====================

Main Process Setup
------------------

The main process initializes the logging system and establishes the log directory structure:

.. code-block:: python

    from dtPyAppFramework.application import AbstractApp
    import logging

    class MyApplication(AbstractApp):
        def main(self, args):
            # Logging already initialized by framework
            logger = logging.getLogger(__name__)
            
            logger.info("Main application started")
            
            # Spawn child processes
            from dtPyAppFramework.process import MultiProcessingManager
            manager = MultiProcessingManager()
            
            job = manager.new_multiprocessing_job(
                job_name="data_processing",
                worker_count=3,
                target=self.process_data
            )
            job.start()
            
            logger.info("Main application completed")

Spawned Process Context
-----------------------

Spawned processes automatically inherit logging configuration with their own context:

.. code-block:: python

    def process_data():
        """Function executed in spawned process."""
        import logging
        
        # Logger automatically configured for this process
        logger = logging.getLogger(__name__)
        
        # Logs go to: /logs/20231215_143022/job-123/worker-1/
        logger.info("Spawned process started")
        logger.debug("Processing data batch")
        logger.info("Spawned process completed")

Directory Structure
-------------------

The logging system creates a hierarchical directory structure:

.. code-block:: text

    logs/
    ├── 20231215_143022/                    # Main process log directory
    │   ├── info-myapp.log                  # Main process info logs
    │   ├── error-myapp.log                 # Main process error logs
    │   ├── stdout.txt                      # Captured stdout (if not console app)
    │   ├── stderr.txt                      # Captured stderr (if not console app)
    │   └── job-123/                        # Multiprocessing job directory
    │       ├── 1/                          # Worker 1 logs
    │       │   ├── info-myapp.log
    │       │   ├── error-myapp.log
    │       │   ├── stdout.txt
    │       │   └── stderr.txt
    │       ├── 2/                          # Worker 2 logs
    │       └── 3/                          # Worker 3 logs
    ├── 20231215_120045/                    # Previous run (kept for rotation)
    └── 20231215_095533/                    # Older run (kept for rotation)

Console Output
==============

Color-Coded Display
-------------------

The framework uses ``colorlog`` for enhanced console readability:

.. code-block:: python

    from dtPyAppFramework.settings import Settings
    import logging
    
    settings = Settings()
    
    # Enable colored console output
    if settings.get('logging.log_to_console', False):
        logger = logging.getLogger('console')
        
        # These will appear in different colors
        logger.debug('Debug information')      # Blue
        logger.info('Information message')     # Green  
        logger.warning('Warning message')      # Yellow
        logger.error('Error message')          # Red
        logger.critical('Critical message')    # Bold red

**Default Color Format:**
``%(log_color)s%(asctime)s - %(levelname)-8s - %(processName)s.%(process)d - %(threadName)s.%(thread)d - %(module)s.%(funcName)s.%(lineno)-3d - %(message)s%(reset)s``

Console Configuration
---------------------

Control console output through settings:

.. code-block:: yaml

    logging:
      log_to_console: true               # Enable console output
      console_level: "DEBUG"             # Console-specific log level
      color_console: true                # Enable color coding
      
    # Development mode - verbose console output
    dev_mode:
      logging:
        console_format: "%(levelname)s: %(message)s"  # Simpler format
        show_process_info: false         # Hide process details

Advanced Features
=================

Structured Logging
------------------

Implement structured logging for better log analysis:

.. code-block:: python

    import logging
    import json
    from datetime import datetime

    class StructuredLogger:
        def __init__(self, name):
            self.logger = logging.getLogger(name)
        
        def log_structured(self, level, message, **kwargs):
            """Log structured data as JSON."""
            log_data = {
                'timestamp': datetime.utcnow().isoformat(),
                'level': level,
                'message': message,
                'data': kwargs
            }
            self.logger.log(getattr(logging, level.upper()), json.dumps(log_data))

    # Usage
    structured_logger = StructuredLogger('myapp.api')
    structured_logger.log_structured(
        'info',
        'API request processed',
        user_id='12345',
        endpoint='/api/data',
        response_time_ms=245,
        status_code=200
    )

Context Managers
----------------

Use context managers for operation tracking:

.. code-block:: python

    import logging
    from contextlib import contextmanager
    import time

    @contextmanager
    def log_operation(operation_name, logger=None):
        """Context manager for logging operation duration."""
        if logger is None:
            logger = logging.getLogger(__name__)
        
        start_time = time.time()
        logger.info(f"Starting operation: {operation_name}")
        
        try:
            yield
        except Exception as ex:
            logger.error(f"Operation '{operation_name}' failed: {ex}")
            raise
        finally:
            duration = time.time() - start_time
            logger.info(f"Operation '{operation_name}' completed in {duration:.2f}s")

    # Usage
    with log_operation("database_query"):
        # Database operation code
        pass

Custom Log Handlers
-------------------

Implement custom handlers for specialized logging needs:

.. code-block:: python

    import logging
    from logging import Handler
    
    class DatabaseLogHandler(Handler):
        """Custom handler that logs to database."""
        
        def __init__(self, connection_string):
            super().__init__()
            self.connection_string = connection_string
            # Initialize database connection
        
        def emit(self, record):
            """Write log record to database."""
            try:
                log_entry = {
                    'timestamp': record.created,
                    'level': record.levelname,
                    'message': record.getMessage(),
                    'module': record.module,
                    'process_id': record.process
                }
                # Insert into database
                self.write_to_database(log_entry)
            except Exception:
                self.handleError(record)

Performance Considerations
==========================

Log Level Management
--------------------

Optimize performance with appropriate log levels:

.. code-block:: python

    import logging

    logger = logging.getLogger(__name__)

    # Expensive operation - only evaluate if needed
    if logger.isEnabledFor(logging.DEBUG):
        debug_data = expensive_debug_calculation()
        logger.debug(f"Debug data: {debug_data}")

    # Use lazy evaluation for complex log messages
    logger.info("Processing %d items with %s configuration", 
                item_count, lambda: get_config_summary())

Buffered Logging
----------------

For high-throughput scenarios, consider buffered logging:

.. code-block:: python

    import logging.handlers

    # Configure buffered handler in logging config
    buffer_handler = logging.handlers.MemoryHandler(
        capacity=1000,
        flushLevel=logging.ERROR,
        target=logging.FileHandler('application.log')
    )

Monitoring and Alerting
=======================

Log Analysis
------------

Set up log analysis for production monitoring:

.. code-block:: python

    import logging
    import re
    from collections import defaultdict

    class LogAnalyzer:
        def __init__(self, log_file_path):
            self.log_file_path = log_file_path
            self.error_patterns = defaultdict(int)
        
        def analyze_errors(self):
            """Analyze error patterns in log files."""
            error_pattern = re.compile(r'ERROR.*?- (.+)')
            
            with open(self.log_file_path, 'r') as log_file:
                for line in log_file:
                    match = error_pattern.search(line)
                    if match:
                        error_msg = match.group(1)
                        self.error_patterns[error_msg] += 1
            
            return dict(self.error_patterns)

Health Check Integration
------------------------

Include logging health in application health checks:

.. code-block:: python

    def check_logging_health():
        """Check logging system health."""
        import os
        from dtPyAppFramework.paths import ApplicationPaths
        
        paths = ApplicationPaths()
        log_path = paths.logging_root_path
        
        health_status = {
            'log_directory_exists': os.path.exists(log_path),
            'log_directory_writable': os.access(log_path, os.W_OK),
            'recent_logs_present': len(os.listdir(log_path)) > 0
        }
        
        return all(health_status.values()), health_status

Best Practices
==============

1. **Use Appropriate Log Levels**: Reserve DEBUG for development, INFO for normal operations
2. **Structured Messages**: Include context information in log messages
3. **Avoid Logging Sensitive Data**: Never log passwords, tokens, or personal information
4. **Performance Awareness**: Use lazy evaluation for expensive log message generation
5. **Centralized Configuration**: Manage logging configuration through the framework's settings system
6. **Monitor Log Volume**: Implement log rotation and cleanup to manage disk space
7. **Cross-Process Coordination**: Let the framework handle multiprocess logging coordination

The logging system provides a robust foundation for application observability with enterprise-grade features while maintaining ease of use and configuration flexibility.