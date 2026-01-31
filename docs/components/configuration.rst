=====================
Configuration Management
=====================

The Configuration Management system provides flexible configuration approaches that adapt to deployment modes: a sophisticated three-tier layered system for standard deployments, and a simplified single-layer approach for containerized environments.

Overview
========

dtPyAppFramework implements adaptive configuration management that changes based on deployment mode:

Standard Mode Configuration
---------------------------

A hierarchical configuration system that automatically merges settings from multiple sources in order of precedence:

1. **Working Directory Config** (``./config/config.yaml``) - Highest priority (300)
2. **Application Data Config** - System-wide configuration (200)  
3. **User Data Config** - User-specific configuration (100)

This layered approach allows for flexible deployment scenarios where system administrators can set defaults, users can override with personal preferences, and applications can override with specific configurations.

Container Mode Configuration
-----------------------------

In container mode (enabled with ``--container`` or ``CONTAINER_MODE=true``), the framework uses a simplified single-layer configuration:

1. **Working Directory Config** (``./config/config.yaml``) - Only configuration layer

This simplified approach is optimized for containerized deployments where multi-user configuration layers are not needed, and all configuration is typically managed through external configuration management systems, environment variables, or mounted volumes.

Core Components
===============

Settings Class
--------------

The ``Settings`` class is the main interface for accessing configuration values.

.. autoclass:: dtPyAppFramework.settings.Settings
   :members:
   :inherited-members:

Key Features:

**Singleton Pattern**
  Only one Settings instance exists per application, ensuring configuration consistency.

**Dot Notation Access**
  Configuration values can be accessed using dot notation:

.. code-block:: python

    settings = Settings()
    database_host = settings.get('database.host', 'localhost')
    log_level = settings.get('logging.level', 'INFO')

**Dynamic Value Resolution**
  Settings supports dynamic resolution of:

  * **Environment Variables**: ``ENV/VARIABLE_NAME``
  * **Secrets**: ``SEC/secret_name`` 
  * **Path Aliases**: ``<USR>`` for user data path, ``<APP>`` for app data path

SettingsReader Class
--------------------

The ``SettingsReader`` class handles loading and monitoring of individual configuration files.

.. autoclass:: dtPyAppFramework.settings.settings_reader.SettingsReader
   :members:

Key Features:

**File Watching**
  Automatically detects changes to configuration files and reloads them using the watchdog library.

**Priority System**
  Each reader has a priority level that determines the order of configuration precedence.

**YAML Support**
  Native support for YAML configuration files with UTF-8 encoding.

Configuration Hierarchy
========================

Working Directory Configuration
-------------------------------

**Location**: ``./config/config.yaml`` (relative to application working directory)
**Priority**: 300 (Highest)

This is the primary configuration file for application-specific settings.

.. code-block:: yaml

    # ./config/config.yaml
    app:
      name: "MyApplication"
      version: "1.0.0"
      
    database:
      host: "localhost"
      port: 5432
      name: "myapp_db"
      
    logging:
      level: "INFO"
      log_to_console: true

Application Data Configuration
------------------------------

**Location**: Platform-specific system directory
**Priority**: 200 (Medium)

* **Windows**: ``%ALLUSERSPROFILE%/AppName/config.yaml``
* **macOS**: ``/Library/Application Support/AppName/config.yaml``
* **Linux (root)**: ``/var/lib/AppName/config.yaml``
* **Linux (user)**: ``$XDG_CONFIG_HOME/AppName/config.yaml`` (default: ``~/.config/AppName/config.yaml``)

Used for system-wide default settings that apply to all users.

User Data Configuration  
-----------------------

**Location**: Platform-specific user directory
**Priority**: 100 (Lowest)

* **Windows**: ``%APPDATA%/AppName/config.yaml``
* **macOS**: ``~/Library/Application Support/AppName/config.yaml``
* **Linux (root)**: ``/etc/AppName/config.yaml``
* **Linux (user)**: ``$XDG_DATA_HOME/AppName/config.yaml`` (default: ``~/.local/share/AppName/config.yaml``)

Used for user-specific preferences and overrides.

Dynamic Value Resolution
========================

Environment Variables
---------------------

Configuration values can reference environment variables using the ``ENV/`` prefix:

.. code-block:: yaml

    database:
      host: "ENV/DATABASE_HOST"  # Resolves to os.environ['DATABASE_HOST']
      port: "ENV/DATABASE_PORT"  # Falls back to the literal string if env var doesn't exist

Secrets Integration
-------------------

Configuration can directly reference secrets using the ``SEC/`` prefix:

.. code-block:: yaml

    database:
      username: "ENV/DB_USER"
      password: "SEC/database_password"  # Retrieved from secrets manager
      
    api:
      key: "SEC/external_api.key"  # Supports dot notation in secret names

Path Aliases
------------

Built-in path aliases for common directory references:

.. code-block:: yaml

    logging:
      file_path: "<USR>/logs/application.log"  # User data directory
      
    resources:
      templates: "<APP>/templates"  # Application data directory

Hot Reload and File Watching
=============================

The configuration system automatically monitors configuration files for changes using the watchdog library:

**File Monitoring Features**:
  * SHA-256 hash comparison to detect actual content changes
  * Automatic reload when files are modified
  * Handling of file creation and deletion events
  * Support for configuration file replacement scenarios

**Implementation Example**:

.. code-block:: python

    # Configuration changes are automatically detected and reloaded
    # No application restart required
    
    from dtPyAppFramework.settings import Settings
    import time
    
    settings = Settings()
    print(settings.get('logging.level'))  # INFO
    
    # Modify config.yaml file externally
    # Change logging.level to DEBUG
    
    time.sleep(1)  # Allow file watcher to detect change
    print(settings.get('logging.level'))  # DEBUG (automatically updated)

Configuration File Format
==========================

YAML Structure
--------------

Configuration files use YAML format with hierarchical structure:

.. code-block:: yaml

    # Application metadata
    app:
      name: "MyApplication"
      version: "1.2.0"
      description: "Application description"
    
    # Database configuration
    database:
      host: "ENV/DB_HOST"
      port: 5432
      name: "myapp"
      username: "ENV/DB_USER"
      password: "SEC/database_password"
      pool:
        min_connections: 1
        max_connections: 10
        timeout: 30
    
    # Logging configuration
    logging:
      level: "INFO"
      log_to_console: false
      rotation_backup_count: 5
      file_path: "<USR>/logs/app.log"
    
    # Multi-processing settings
    multiprocessing:
      max_workers: 4
      task_timeout: 300
    
    # Cloud session configuration
    cloud_sessions:
      - name: "aws_primary"
        session_type: "aws"
        region: "us-east-1"
        profile: "default"
      
      - name: "azure_primary" 
        session_type: "azure"
        subscription_id: "ENV/AZURE_SUBSCRIPTION_ID"
    
    # Secrets manager configuration
    secrets_manager:
      cloud_stores:
        aws_secrets:
          store_type: "aws"
          priority: 100
          region: "us-east-1"
          session_name: "aws_primary"
          
        azure_keyvault:
          store_type: "azure"
          priority: 200
          vault_url: "https://myvault.vault.azure.net/"
          session_name: "azure_primary"

Configuration Merging
======================

The framework automatically merges configurations from all three layers using deep dictionary merging:

**Example Merge Scenario**:

User Config (Priority 100):
.. code-block:: yaml

    logging:
      level: "DEBUG"
      file_path: "<USR>/logs/user.log"
    database:
      host: "user-db-server"

App Data Config (Priority 200):
.. code-block:: yaml

    logging:
      level: "INFO"
      rotation_backup_count: 10
    database:
      host: "app-db-server"  
      port: 5432
      
Working Dir Config (Priority 300):
.. code-block:: yaml

    database:
      host: "local-db-server"

**Resulting Merged Configuration**:
.. code-block:: yaml

    logging:
      level: "DEBUG"           # From Working Dir (highest priority)
      file_path: "<USR>/logs/user.log"  # From User Config
      rotation_backup_count: 10 # From App Data Config
    database:
      host: "local-db-server"   # From Working Dir (highest priority)
      port: 5432               # From App Data Config

Best Practices
==============

Configuration Design
---------------------

1. **Use Hierarchical Structure**: Organize related settings into logical groups
2. **Provide Sensible Defaults**: Ensure applications work with minimal configuration
3. **Document Configuration Options**: Include comments in example configuration files
4. **Validate Configuration**: Check for required settings and valid values
5. **Use Environment Variables**: For deployment-specific values like database hosts
6. **Use Secrets**: For sensitive data like passwords and API keys

Deployment Strategies
---------------------

**Development Environment**:
.. code-block:: yaml

    # ./config/config.yaml
    app:
      debug: true
    database:
      host: "localhost"
      name: "myapp_dev"
    logging:
      level: "DEBUG"
      log_to_console: true

**Production Environment**:
.. code-block:: yaml

    # System-wide config
    database:
      host: "ENV/PROD_DB_HOST"
      name: "ENV/PROD_DB_NAME"
      username: "ENV/PROD_DB_USER"
      password: "SEC/prod_database_password"
    logging:
      level: "INFO"
      log_to_console: false

Error Handling
==============

The configuration system provides robust error handling:

.. code-block:: python

    from dtPyAppFramework.settings import Settings
    
    settings = Settings()
    
    # Safe access with default values
    timeout = settings.get('api.timeout', 30)
    
    # Handle missing configuration gracefully
    try:
        required_setting = settings.get('required.setting')
        if required_setting is None:
            raise ValueError("Required setting 'required.setting' not configured")
    except Exception as ex:
        import logging
        logging.error(f"Configuration error: {ex}")
        # Handle configuration error appropriately

Advanced Features
=================

Custom Configuration Readers
-----------------------------

Applications can add custom configuration sources:

.. code-block:: python

    from dtPyAppFramework.settings import Settings
    from dtPyAppFramework.settings.settings_reader import SettingsReader
    
    settings = Settings()
    
    # Add custom configuration source
    custom_reader = SettingsReader("/path/to/custom/config", priority=50)
    settings.settings_readers.append(custom_reader)
    settings.settings_readers.sort(key=lambda x: x.priority)

Configuration Validation
-------------------------

Implement configuration validation in your application:

.. code-block:: python

    class MyApplication(AbstractApp):
        def validate_configuration(self):
            """Validate required configuration settings."""
            from dtPyAppFramework.settings import Settings
            settings = Settings()
            
            required_settings = [
                'database.host',
                'database.name', 
                'api.base_url'
            ]
            
            for setting in required_settings:
                if not settings.get(setting):
                    raise ValueError(f"Required setting '{setting}' not configured")

The configuration management system provides a powerful, flexible foundation for application configuration that scales from simple single-file configurations to complex multi-environment deployments with secrets management and hot-reload capabilities.