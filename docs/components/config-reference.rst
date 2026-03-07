======================
Configuration Reference
======================

This document provides a complete reference for the ``config.yaml`` configuration file, including all available settings, their default values, and usage examples.

Overview
========

dtPyAppFramework uses YAML configuration files with:

- **Layered configuration** in standard mode (three tiers merged by priority)
- **Single configuration** in container mode (working directory only)
- **Dynamic value resolution** for environment variables, secrets, and path aliases
- **Hot reload** via file system watching

Configuration File Locations
============================

Standard Mode
-------------

Configuration files are loaded and merged in priority order (higher priority wins):

.. list-table::
   :header-rows: 1
   :widths: 15 25 60

   * - Priority
     - Scope
     - Location
   * - 300
     - Working Directory
     - ``./config/config.yaml``
   * - 200
     - All Users
     - Platform-specific (see below)
   * - 100
     - Current User
     - Platform-specific (see below)

**Platform-Specific Locations:**

Windows:

- All Users: ``C:\ProgramData\{app_short_name}\config.yaml``
- Current User: ``C:\Users\{username}\AppData\Local\{app_short_name}\config.yaml``

macOS:

- All Users: ``/Library/Application Support/{app_short_name}/config.yaml``
- Current User: ``~/Library/Application Support/{app_short_name}/config.yaml``

Linux (Regular User):

- All Users: ``~/.local/share/{app_short_name}/config.yaml``
- Current User: ``~/.local/share/{app_short_name}/config.yaml``

Linux (Root):

- All Users: ``/etc/{app_short_name}/config.yaml``
- Current User: ``/etc/{app_short_name}/config.yaml``

Container Mode
--------------

When ``CONTAINER_MODE=TRUE``, only a single configuration layer is used:

- ``./config/config.yaml`` (working directory)

Disabling Configuration Files
-----------------------------

When ``CONFIG_FILES_ENABLED=FALSE``, no configuration files are read:

- No ``config.yaml`` files are loaded or watched
- ``settings.get()`` returns the default value (or ``None``)
- Configuration must come from environment variables or other sources
- Useful for containerised environments with external configuration management

.. code-block:: bash

    # Disable config file reading
    export CONFIG_FILES_ENABLED=FALSE
    python myapp.py

When disabled, you can still use:

- Environment variables directly in your code
- Cloud-based secret stores for sensitive configuration
- Command-line arguments for runtime configuration

Configuration Sections
======================

Logging Configuration
---------------------

Controls application logging behaviour.

.. code-block:: yaml

    logging:
      level: "INFO"                    # Log level: DEBUG, INFO, WARNING, ERROR, CRITICAL
      log_to_console: false            # Enable console output (coloured)
      rotation_backup_count: 5         # Number of log folders to retain

**Settings:**

.. list-table::
   :header-rows: 1
   :widths: 30 15 55

   * - Key
     - Default
     - Description
   * - ``logging.level``
     - ``INFO``
     - Minimum log level to capture
   * - ``logging.log_to_console``
     - ``false``
     - Enable coloured console logging output
   * - ``logging.rotation_backup_count``
     - ``5``
     - Number of timestamped log folders to retain

Proxy Configuration
-------------------

Configure proxy settings for TOR and other proxies.

.. code-block:: yaml

    settings:
      proxies:
        tor_proxy: "127.0.0.1:9150"    # TOR SOCKS5 proxy address

**Settings:**

.. list-table::
   :header-rows: 1
   :widths: 30 20 50

   * - Key
     - Default
     - Description
   * - ``settings.proxies.tor_proxy``
     - ``127.0.0.1:9150``
     - TOR proxy address (host:port)

Cloud Sessions
--------------

Define cloud provider sessions for secrets management and cloud integration.

.. code-block:: yaml

    cloud_sessions:
      - name: "aws_primary"
        session_type: "aws"
        region: "us-east-1"
        profile: "default"

      - name: "azure_primary"
        session_type: "azure"
        subscription_id: "ENV/AZURE_SUBSCRIPTION_ID"
        tenant_id: "ENV/AZURE_TENANT_ID"

**AWS Session Fields:**

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Field
     - Description
   * - ``name``
     - Unique session identifier (referenced by secret stores)
   * - ``session_type``
     - Must be ``aws``
   * - ``region``
     - AWS region (e.g., ``us-east-1``, ``eu-west-1``)
   * - ``profile``
     - AWS CLI profile name (default: ``default``)

**Azure Session Fields:**

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Field
     - Description
   * - ``name``
     - Unique session identifier (referenced by secret stores)
   * - ``session_type``
     - Must be ``azure``
   * - ``subscription_id``
     - Azure subscription ID
   * - ``tenant_id``
     - Azure tenant ID (optional, for service principal auth)

Secrets Manager Configuration
-----------------------------

Configure cloud-based secret stores.

.. code-block:: yaml

    secrets_manager:
      cloud_stores:
        azure_keyvault:
          store_type: "azure"
          priority: 100
          vault_url: "https://myvault.vault.azure.net/"
          session_name: "azure_primary"

        aws_secrets:
          store_type: "aws"
          priority: 200
          region: "us-east-1"
          session_name: "aws_primary"

**Azure Key Vault Store Fields:**

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Field
     - Description
   * - ``store_type``
     - Must be ``azure``
   * - ``priority``
     - Resolution order (lower = checked first)
   * - ``vault_url``
     - Azure Key Vault URL
   * - ``session_name``
     - Reference to cloud session defined above

**AWS Secrets Manager Store Fields:**

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Field
     - Description
   * - ``store_type``
     - Must be ``aws``
   * - ``priority``
     - Resolution order (lower = checked first)
   * - ``region``
     - AWS region for Secrets Manager
   * - ``session_name``
     - Reference to cloud session defined above

**Built-in Local Store Priorities:**

- ``User_Local_Store``: priority 0 (highest)
- ``App_Local_Store``: priority 1 (only if ``ALL_USER_KS=TRUE``)

Dynamic Value Resolution
========================

Environment Variables
---------------------

Reference environment variables using the ``ENV/`` prefix:

.. code-block:: yaml

    database:
      host: "ENV/DATABASE_HOST"        # Reads os.environ['DATABASE_HOST']
      port: "ENV/DATABASE_PORT"        # Falls back to literal if not set

    cloud_sessions:
      - name: "azure"
        subscription_id: "ENV/AZURE_SUBSCRIPTION_ID"

**Behaviour:**

- If the environment variable exists, its value is substituted
- If the environment variable does not exist, the literal string (including ``ENV/``) is returned
- Works in all configuration values (strings only)

Secrets References
------------------

Reference secrets using the ``SEC/`` prefix:

.. code-block:: yaml

    database:
      username: "app_user"
      password: "SEC/database_password"    # Retrieved from secrets manager

    api:
      key: "SEC/external_api.key"          # Dot notation supported in secret names
      token: "SEC/api.oauth.token"

**Behaviour:**

- Secret is retrieved from configured secret stores in priority order
- Returns ``None`` if secret is not found in any store
- Dot notation in secret names is preserved (not interpreted as nested keys)

Path Aliases
------------

Reference application paths using angle-bracket aliases:

.. code-block:: yaml

    storage:
      database: "<USR>/database.db"        # User data directory
      cache: "<TMP>/cache"                 # Temporary directory
      templates: "<APP>/templates"         # Application data directory

    logging:
      custom_path: "<USR>/logs/custom.log"

**Available Aliases:**

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - Alias
     - Property
     - Example (Windows)
   * - ``<USR>``
     - ``usr_data_root_path``
     - ``C:\Users\{user}\AppData\Local\{app}``
   * - ``<APP>``
     - ``app_data_root_path``
     - ``C:\ProgramData\{app}``
   * - ``<TMP>``
     - ``tmp_root_path``
     - ``C:\Users\{user}\AppData\Local\Temp\{app}``

Logging Configuration File
==========================

In addition to ``config.yaml``, you can provide a custom logging configuration.

**File Name:** ``loggingConfig.yaml``

**Search Order:**

1. ``{usr_data_root_path}/loggingConfig.yaml``
2. ``{app_data_root_path}/loggingConfig.yaml``
3. ``./config/loggingConfig.yaml``

**Example Custom Logging Configuration:**

.. code-block:: yaml

    version: 1
    disable_existing_loggers: false

    formatters:
      standard:
        format: '%(asctime)s - %(levelname)s - %(name)s - %(message)s'

    handlers:
      console:
        class: logging.StreamHandler
        level: DEBUG
        formatter: standard
        stream: ext://sys.stdout

      file:
        class: logging.handlers.RotatingFileHandler
        level: INFO
        formatter: standard
        filename: logs/app.log
        maxBytes: 10485760
        backupCount: 5

    loggers:
      myapp:
        level: DEBUG
        handlers: [console, file]
        propagate: false

    root:
      level: INFO
      handlers: [console]

If no custom logging configuration is found, the framework uses its default configuration with settings from ``config.yaml``.

Configuration Merging
=====================

In standard mode, configurations from all three layers are deep-merged:

**User Config (Priority 100):**

.. code-block:: yaml

    logging:
      level: "DEBUG"
    database:
      timeout: 60

**All Users Config (Priority 200):**

.. code-block:: yaml

    logging:
      level: "INFO"
      rotation_backup_count: 10
    database:
      host: "db.internal"
      port: 5432

**Working Directory Config (Priority 300):**

.. code-block:: yaml

    database:
      host: "localhost"

**Merged Result:**

.. code-block:: yaml

    logging:
      level: "DEBUG"                 # From User (lowest priority for this key)
      rotation_backup_count: 10      # From All Users (only source)
    database:
      host: "localhost"              # From Working Dir (highest priority)
      port: 5432                     # From All Users (only source)
      timeout: 60                    # From User (only source)

.. note::

   Higher priority values **override** lower priority values for the same key.
   Keys that exist only in one layer are preserved in the merged result.

Hot Reload
==========

Configuration files are monitored for changes using the watchdog library:

- **File modification**: Configuration reloaded when content changes (SHA-256 verified)
- **File creation**: New configuration loaded when file is created
- **File deletion**: Configuration cleared when file is deleted

**Programmatic Access:**

.. code-block:: python

    from dtPyAppFramework.settings import Settings

    settings = Settings()

    # Initial value
    log_level = settings.get('logging.level', 'INFO')

    # After external file modification, value updates automatically
    # No application restart required

Complete Example
================

**./config/config.yaml:**

.. code-block:: yaml

    # Application settings
    app:
      name: "My Application"
      version: "1.0.0"
      environment: "ENV/APP_ENVIRONMENT"

    # Logging configuration
    logging:
      level: "INFO"
      log_to_console: true
      rotation_backup_count: 7

    # Database configuration
    database:
      host: "ENV/DB_HOST"
      port: 5432
      name: "myapp"
      username: "ENV/DB_USER"
      password: "SEC/database_password"
      pool:
        min_connections: 2
        max_connections: 20
        timeout: 30

    # API configuration
    api:
      base_url: "https://api.example.com"
      key: "SEC/api_key"
      timeout: 30
      retry_count: 3

    # Storage paths using aliases
    storage:
      data_dir: "<USR>/data"
      cache_dir: "<TMP>/cache"
      templates_dir: "<APP>/templates"

    # Cloud sessions for secrets
    cloud_sessions:
      - name: "azure_prod"
        session_type: "azure"
        subscription_id: "ENV/AZURE_SUBSCRIPTION_ID"

    # Cloud secret stores
    secrets_manager:
      cloud_stores:
        azure_vault:
          store_type: "azure"
          priority: 100
          vault_url: "ENV/AZURE_VAULT_URL"
          session_name: "azure_prod"

    # Proxy settings
    settings:
      proxies:
        tor_proxy: "127.0.0.1:9150"

**Accessing Configuration:**

.. code-block:: python

    from dtPyAppFramework.settings import Settings

    settings = Settings()

    # Simple value access
    app_name = settings.get('app.name')
    log_level = settings.get('logging.level', 'INFO')

    # Nested value access
    pool_size = settings.get('database.pool.max_connections', 10)

    # Environment variable resolution (automatic)
    db_host = settings.get('database.host')  # Resolved from ENV/DB_HOST

    # Secret resolution (automatic)
    db_password = settings.get('database.password')  # Retrieved from secrets

    # Path alias resolution (automatic)
    data_dir = settings.get('storage.data_dir')  # Resolved from <USR>/data

    # Direct secret access
    api_key = settings.secret_manager.get_secret('api_key')

Environment Variables Affecting Configuration
==============================================

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Variable
     - Default
     - Effect
   * - ``CONTAINER_MODE``
     - ``FALSE``
     - Use single-layer configuration (working directory only)
   * - ``DEV_MODE``
     - ``FALSE``
     - Use development paths (relative to working directory)
   * - ``USE_SYSTEM_TEMP``
     - ``FALSE``
     - Use native OS temp directory without app-specific subdirectory
   * - ``CONFIG_FILES_ENABLED``
     - ``TRUE``
     - Enable config.yaml reading; when ``FALSE``, no config files are read
   * - ``LOCAL_SECRETS_STORE``
     - ``TRUE``
     - Enable local keystore; when ``FALSE``, no keystore files are created
   * - ``ALL_USER_KS``
     - ``FALSE``
     - Create all-users keystore (App_Local_Store)
   * - ``KEYSTORE_PASSWORD``
     - (none)
     - Password for local keystore encryption
   * - ``KEYSTORE_LOCK_TIMEOUT``
     - ``30``
     - File lock timeout in seconds for concurrent keystore access

Quick Reference
===============

**Configuration Priorities:**

::

    Priority 300: ./config/config.yaml           (Working Directory)
    Priority 200: {app_data}/config.yaml         (All Users)
    Priority 100: {usr_data}/config.yaml         (Current User)

**Dynamic Prefixes:**

::

    ENV/VARIABLE_NAME  →  Environment variable lookup
    SEC/secret_name    →  Secrets manager lookup
    <USR>              →  User data path
    <APP>              →  Application data path
    <TMP>              →  Temporary path

**Common Settings:**

::

    logging.level                    →  DEBUG|INFO|WARNING|ERROR|CRITICAL
    logging.log_to_console           →  true|false
    logging.rotation_backup_count    →  integer (default: 5)
    settings.proxies.tor_proxy       →  host:port (default: 127.0.0.1:9150)

**Secret Store Configuration:**

::

    secrets_manager.cloud_stores.{name}.store_type   →  azure|aws
    secrets_manager.cloud_stores.{name}.priority     →  integer
    secrets_manager.cloud_stores.{name}.session_name →  cloud session reference
