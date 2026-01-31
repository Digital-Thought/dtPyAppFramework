==================
Secrets Management
==================

The Secrets Management system provides a unified interface for storing and retrieving sensitive data across multiple backends including Azure Key Vault, AWS Secrets Manager, and local encrypted storage.

Overview
========

dtPyAppFramework's secrets management system is designed for enterprise environments where sensitive data must be securely stored and accessed across different cloud providers and local environments. The system provides:

* **Multi-Cloud Support**: Azure Key Vault and AWS Secrets Manager integration
* **Local Encrypted Storage**: Secure local secrets using cryptography library
* **Priority-Based Resolution**: Configurable priority system for secret resolution
* **Seamless Integration**: Direct integration with configuration system
* **Cross-Process Sharing**: Secrets available to spawned processes

Core Components
===============

SecretsManager
--------------

The ``SecretsManager`` class is the main orchestrator for all secret stores.

.. autoclass:: dtPyAppFramework.settings.secrets.SecretsManager
   :members:
   :inherited-members:

Key Features:

**Store Management**
  * Automatic loading of configured secret stores
  * Priority-based secret resolution
  * Store availability monitoring
  * Read-only and read-write store support

**Multi-Store Resolution**
  Searches through stores in priority order until a secret is found:

.. code-block:: python

    from dtPyAppFramework.settings import Settings
    settings = Settings()
    
    # Searches all stores in priority order
    database_password = settings.secret_manager.get_secret('database_password')
    
    # Search specific store
    api_key = settings.secret_manager.get_secret('api_key', store_name='azure_keyvault')

AbstractSecretStore
-------------------

Base class for all secret store implementations.

.. autoclass:: dtPyAppFramework.settings.secrets.secret_store.AbstractSecretStore
   :members:

All secret stores inherit from this class and implement:

* ``get_secret(key, default_value)`` - Retrieve a secret
* ``set_secret(key, value)`` - Store a secret  
* ``delete_secret(key)`` - Remove a secret
* ``create_secret(name, length)`` - Generate and store a random secret

SystemPasswordGenerator
------------------------

Enhanced password generation system for secure keystore access.

.. autoclass:: dtPyAppFramework.settings.secrets.keystore.SystemPasswordGenerator
   :members:

**Key Features:**

* **Enhanced Entropy**: Combines multiple system attributes for password generation
* **Container Support**: Works reliably in Docker and containerized environments
* **Custom Password Integration**: Supports user-provided passwords with system strengthening
* **Cross-Platform**: Consistent behavior across Windows, Linux, macOS, and BSD systems
* **Secure Defaults**: Minimum 256-bit entropy with PBKDF2 key derivation

**Usage Examples:**

.. code-block:: python

    from dtPyAppFramework.settings.secrets.keystore import SystemPasswordGenerator
    
    # Basic usage with system-generated password
    generator = SystemPasswordGenerator(app_name="myapp")
    password = generator.generate_password()
    
    # With custom password (system-strengthened)
    password = generator.generate_password(custom_password="user_secret")
    
    # User override (custom password only, no system strengthening)
    password = generator.generate_password(custom_password="user_secret", user_override=True)

**Security Features:**

* **System Fingerprinting**: Uses multiple system identifiers for unique password generation
* **Salt Generation**: Automatic installation-specific salt generation
* **PBKDF2 Derivation**: Industry-standard key derivation with configurable iterations
* **Entropy Validation**: Ensures minimum entropy requirements are met
* **Container Awareness**: Adapts to containerized environments for consistent results

Secret Store Types
==================

Local Secret Stores
--------------------

Local secret stores provide encrypted storage on the local filesystem using the cryptography library.

**LocalSecretStore**

.. autoclass:: dtPyAppFramework.settings.secrets.local_secret_store.LocalSecretStore
   :members:

**Key Features:**
  * AES encryption with Fernet symmetric encryption
  * Password-based key derivation (PBKDF2)
  * Automatic keystore format migration (v2 to v3)
  * Enhanced ``SecureKeyGenerator`` for improved v3 password generation
  * ``LegacyKeyGenerator`` for backward-compatible v2 keystore access during migration
  * Direct store access with ``FileLock``-based synchronisation (no IPC pipes)
  * HMAC verification hardening: failures always raise exceptions
  * Atomic writes using ``tempfile.mkstemp()`` with ``os.replace()``
  * Support for both user-level and application-level stores

**Keystore Evolution:**
  * **v2keystore**: Legacy format using basic machine fingerprinting via ``LegacyKeyGenerator``
  * **v3keystore**: Enhanced format with ``SecureKeyGenerator`` providing improved entropy, HMAC verification, and atomic writes
  * **Migration**: Automatic detection and seamless migration from v2 to v3 format, with graceful fallback to v2 if migration fails
  * **Backup**: Original v2keystore renamed to ``v2keystore_old`` after successful migration
  * **Concurrency**: File-level locking via ``filelock`` prevents data corruption during concurrent access

**Store Locations:**
  * **User Local Store**: ``<user_data_path>/app_name.v3keystore`` (or ``app_name.v2keystore`` for legacy)
  * **App Local Store**: ``<app_data_path>/app_name.v3keystore`` (or ``app_name.v2keystore`` for legacy)

**Configuration:**

.. code-block:: yaml

    # Automatically configured - no YAML configuration needed
    # Local stores are always available with default priorities

Azure Key Vault Integration
----------------------------

**AzureSecretsStore**

.. autoclass:: dtPyAppFramework.settings.secrets.azure_secret_store.AzureSecretsStore
   :members:

**Configuration:**

.. code-block:: yaml

    cloud_sessions:
      - name: "azure_primary"
        session_type: "azure"
        subscription_id: "ENV/AZURE_SUBSCRIPTION_ID"
        
    secrets_manager:
      cloud_stores:
        azure_keyvault:
          store_type: "azure"
          priority: 100
          vault_url: "https://myvault.vault.azure.net/"
          session_name: "azure_primary"

**Authentication Methods:**
  * DefaultAzureCredential (recommended)
  * Service Principal with client secret
  * Managed Identity
  * Azure CLI authentication

AWS Secrets Manager Integration
-------------------------------

**AWSSecretsStore**

.. autoclass:: dtPyAppFramework.settings.secrets.aws_secret_store.AWSSecretsStore
   :members:

**Configuration:**

.. code-block:: yaml

    cloud_sessions:
      - name: "aws_primary"
        session_type: "aws"
        region: "us-east-1"
        profile: "default"
        
    secrets_manager:
      cloud_stores:
        aws_secrets:
          store_type: "aws"
          priority: 200
          region: "us-east-1"
          session_name: "aws_primary"

**Authentication Methods:**
  * AWS CLI profiles
  * IAM roles
  * Environment variables (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
  * EC2 instance profiles

Configuration Integration
=========================

Direct Configuration Access
----------------------------

Secrets can be directly referenced in configuration files using the ``SEC/`` prefix:

.. code-block:: yaml

    database:
      host: "localhost"
      username: "app_user"
      password: "SEC/database_password"  # Retrieved from secrets manager
      
    api:
      base_url: "https://api.example.com"
      key: "SEC/external_api.key"
      
    email:
      smtp_password: "SEC/email.smtp_password"

**Programmatic Access:**

.. code-block:: python

    from dtPyAppFramework.settings import Settings
    
    settings = Settings()
    
    # Direct secret access
    db_password = settings.secret_manager.get_secret('database_password')
    
    # Access through configuration system (preferred)
    db_password = settings.get('database.password')  # Resolves SEC/ prefix automatically

Store Priority System
---------------------

Secrets are resolved based on store priority (lower numbers = higher priority):

.. code-block:: yaml

    secrets_manager:
      cloud_stores:
        azure_primary:
          store_type: "azure"
          priority: 100        # Checked first
          vault_url: "https://prod-vault.vault.azure.net/"
          
        aws_backup:
          store_type: "aws" 
          priority: 200        # Checked second
          region: "us-east-1"
          
    # Local stores have built-in priorities:
    # User_Local_Store: priority 50
    # App_Local_Store: priority 75

Command Line Secret Management
==============================

Auto-Import from YAML
----------------------

The LocalSecretStore supports automatic import of secrets from a ``secrets.yaml`` file placed in the keystore directory. This feature is useful for batch secret import during application initialization or deployment.

**File Format:**

Create a ``secrets.yaml`` file in your keystore directory with the following structure:

.. code-block:: yaml

    secrets:
      - name: "database_password"
        value: "my_secret_password"
        
      - name: "api_key"
        value: "abc123xyz789"
        
      - name: "ssl_certificate"
        file: "/path/to/certificate.pem"
        store_as: "raw"
        
      - name: "binary_data"
        file: "/path/to/data.bin"  
        store_as: "base64"

**Field Descriptions:**

* **name**: Required. The secret key name
* **value**: Secret value for text-based secrets
* **file**: Path to file for file-based secrets
* **store_as**: How to store file content (``raw`` for text files, ``base64`` for binary files)

**Behavior:**

* Auto-import runs automatically when LocalSecretStore is initialized
* The ``secrets.yaml`` file is **automatically deleted** after successful import
* File-based secrets can be stored as raw text or base64-encoded
* Import failures are logged to stderr but don't stop the process
* Secrets are imported into the current keystore (v3keystore format)

**Usage Example:**

.. code-block:: bash

    # Place secrets.yaml in your keystore directory
    # Run your application - secrets are automatically imported
    python myapp.py
    
    # The secrets.yaml file will be deleted after import
    # Secrets are now available in your keystore

**Security Notes:**

* The ``secrets.yaml`` file should have restricted permissions (readable only by the application user)
* Consider the file temporary - it will be deleted after import
* File paths in the YAML should be accessible to the application
* Use this feature for deployment automation, not manual secret management

Interactive Secret Addition
----------------------------

The framework provides built-in command-line tools for managing secrets:

.. code-block:: bash

    # Interactive secret addition
    python myapp.py --add_secret
    
    # Specify secret name
    python myapp.py --add_secret --name "database_password"
    
    # Add secret from file
    python myapp.py --add_secret --name "ssl_cert" --file "/path/to/cert.pem"
    
    # Add file as base64
    python myapp.py --add_secret --name "binary_data" --file "/path/to/data.bin" --store_as base64

**Interactive Menu Example:**

.. code-block:: text

    Enter the secret name: database_password
    What form of secret do you wish to add?
    1. File
    2. Value
    
    Selection: 2
    Enter Secret Value: [hidden input]
    
    Added secret "database_password" to Secret Store.
    Do you wish to add another secret? (y/N): n

Secret Initialization
---------------------

Initialize local secret stores with password protection:

.. code-block:: bash

    # Initialize with password prompt
    python myapp.py --init
    
    # Initialize with specific password
    python myapp.py --init --password "secure_password"

Local Secret Store Management
=============================

Keystore Format
----------------

The framework uses an evolving keystore format with automatic migration:

**Current Format (v3keystore):**
  * AES-256 encryption using Fernet
  * ``SecureKeyGenerator`` with enhanced entropy combining application name, keystore path, and system fingerprint
  * PBKDF2 key derivation with 100,000 iterations
  * JSON-based secret storage with HMAC integrity verification
  * Atomic write operations to prevent corruption during concurrent access
  * File-level locking for multi-process safety

**Legacy Format (v2keystore):**
  * Basic machine fingerprinting for password generation via ``LegacyKeyGenerator``
  * Automatically migrated to v3 format on first access
  * Graceful fallback to v2 if migration fails (e.g. corrupted keystore)
  * Backed up as ``v2keystore_old`` after successful migration

**Migration Process:**
  1. System detects existing v2keystore
  2. Loads v2keystore using legacy password generation
  3. Creates new v3keystore using SystemPasswordGenerator
  4. Copies all secrets from v2 to v3 format
  5. Renames original v2keystore to ``v2keystore_old``

**File Structure:**
.. code-block:: text

    # Current format
    app_name.v3keystore
    ├── Encrypted metadata with enhanced security
    ├── Salt for key derivation
    └── Encrypted secrets data
    
    # Legacy backup after migration
    app_name.v2keystore_old
    ├── Original encrypted metadata
    ├── Original salt
    └── Original encrypted secrets data

Cross-Process Sharing
---------------------

Local secrets are accessible from spawned processes through the shared keystore file protected by file locking:

.. code-block:: python

    # In main process
    from dtPyAppFramework.settings import Settings
    settings = Settings()
    settings.secret_manager.set_secret('shared_key', 'secret_value')

    # Spawn child process
    from dtPyAppFramework.process import MultiProcessingManager
    manager = MultiProcessingManager()
    job = manager.new_multiprocessing_job(
        job_name="worker",
        worker_count=1,
        target=worker_function
    )

    def worker_function():
        # Child process automatically has access to secrets
        from dtPyAppFramework.settings import Settings
        settings = Settings()
        shared_key = settings.secret_manager.get_secret('shared_key')

Multi-Process and Container Access
----------------------------------

The local keystore supports concurrent access from multiple processes or containers sharing the same keystore file. This is essential for containerised deployments where multiple worker containers need access to shared secrets.

**File Locking Mechanism**

The keystore uses advisory file locking via the ``filelock`` library to prevent race conditions and data corruption when multiple processes access the same keystore file simultaneously.

.. code-block:: text

    ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
    │  Worker 1   │     │  Worker 2   │     │  Worker N   │
    └──────┬──────┘     └──────┬──────┘     └──────┬──────┘
           │                   │                   │
           └───────────────────┼───────────────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │  File Lock (.lock)  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │  Local Keystore     │
                    │  (.v3keystore)      │
                    └─────────────────────┘

**Key Features:**

* **Exclusive Locking**: Write operations (set, delete) acquire an exclusive lock
* **Atomic Writes**: Data is written to a temporary file first, then atomically renamed
* **Configurable Timeout**: Lock acquisition timeout can be configured via environment variable
* **Cross-Platform**: Works on Linux, Windows, and macOS

**Container Mode Password Handling:**

In container environments, the keystore password is handled specially to ensure consistency across multiple containers:

* When ``CONTAINER_MODE=true`` (or running in Docker/Kubernetes), the ``KEYSTORE_PASSWORD`` or ``SECRETS_STORE_PASSWORD`` environment variable is used **directly** without any system fingerprint or path mixing
* This ensures all containers sharing the same keystore file use the same encryption key
* Without this, each container would generate a different key based on its unique system fingerprint (hostname, container ID, etc.)

.. important::

   In container deployments with shared keystores, you **MUST** set the ``KEYSTORE_PASSWORD`` environment variable to the same value across all containers. Without this, each container will be unable to decrypt secrets stored by other containers.

**Configuration:**

The lock timeout can be configured via the ``KEYSTORE_LOCK_TIMEOUT`` environment variable:

.. code-block:: bash

    # Set lock timeout to 60 seconds (default is 30 seconds)
    export KEYSTORE_LOCK_TIMEOUT=60

**Docker Compose Example:**

.. code-block:: yaml

    version: '3.8'
    services:
      coordinator:
        image: myapp:latest
        environment:
          - KEYSTORE_PASSWORD=secure_shared_password
          - KEYSTORE_LOCK_TIMEOUT=60
        volumes:
          - keystore_data:/app/data

      worker:
        image: myapp:latest
        deploy:
          replicas: 3
        environment:
          - KEYSTORE_PASSWORD=secure_shared_password
          - KEYSTORE_LOCK_TIMEOUT=60
        volumes:
          - keystore_data:/app/data

    volumes:
      keystore_data:

**Important Considerations:**

1. **Shared Volume Required**: All containers must mount the same volume for the keystore file
2. **Consistent Password**: All processes must use the same ``KEYSTORE_PASSWORD`` environment variable
3. **Network Filesystems**: File locking behaviour may vary on network filesystems (NFS, CIFS). For production deployments on network storage, consider using a cloud-based secrets manager instead
4. **Lock Contention**: Under heavy concurrent access, processes may need to wait for the lock. Adjust ``KEYSTORE_LOCK_TIMEOUT`` as needed

**Error Handling:**

When a lock cannot be acquired within the timeout period, a ``FileLockTimeout`` exception is raised:

.. code-block:: python

    from filelock import Timeout as FileLockTimeout
    from dtPyAppFramework.settings import Settings

    settings = Settings()

    try:
        secret = settings.secret_manager.get_secret('my_secret')
    except FileLockTimeout:
        logging.error("Could not acquire keystore lock - another process may be holding it")
        # Implement retry logic or fallback behaviour

**Read-Only Worker Pattern:**

For deployments where workers only need to read secrets, consider using read-only mode to reduce lock contention:

.. code-block:: python

    # In worker configuration
    # Workers can still read but cannot modify the keystore
    # This reduces write lock contention in high-concurrency scenarios

Advanced Usage
==============

Custom Secret Stores
---------------------

Applications can implement custom secret stores by inheriting from ``AbstractSecretStore``:

.. code-block:: python

    from dtPyAppFramework.settings.secrets.secret_store import AbstractSecretStore
    
    class CustomSecretStore(AbstractSecretStore):
        def __init__(self, store_name, store_priority, application_settings):
            super().__init__(store_name, "custom", store_priority, application_settings)
            # Initialize your custom store
            self.store_available = True
            self.store_read_only = False
            
        def get_secret(self, key, default_value=None):
            # Implement secret retrieval logic
            pass
            
        def set_secret(self, key, value):
            # Implement secret storage logic
            pass
            
        def delete_secret(self, key):
            # Implement secret deletion logic
            pass

Secret Rotation
---------------

Implement secret rotation patterns:

.. code-block:: python

    from dtPyAppFramework.settings.secrets import SecretsManager
    import logging
    
    def rotate_secret(secret_name, new_value, backup_store=None):
        """Rotate a secret with backup."""
        secrets_manager = SecretsManager()
        
        # Backup current secret if needed
        if backup_store:
            current_value = secrets_manager.get_secret(secret_name)
            if current_value:
                backup_key = f"{secret_name}_backup_{int(time.time())}"
                secrets_manager.set_secret(backup_key, current_value, backup_store)
        
        # Update secret
        secrets_manager.set_secret(secret_name, new_value)
        logging.info(f"Secret '{secret_name}' rotated successfully")

Health Monitoring
-----------------

Monitor secret store availability:

.. code-block:: python

    def check_secret_stores_health():
        """Check health of all configured secret stores."""
        from dtPyAppFramework.settings.secrets import SecretsManager
        
        secrets_manager = SecretsManager()
        health_status = {}
        
        # Check local stores
        local_health = secrets_manager.local_secrets_store_manager.get_health_status()
        health_status.update(local_health)
        
        # Check cloud stores
        for store in secrets_manager.stores:
            try:
                # Test store connectivity
                test_result = store.get_secret("__health_check__", "not_found")
                health_status[store.store_name] = {
                    "available": store.store_available,
                    "read_only": store.store_read_only,
                    "connectivity": "ok"
                }
            except Exception as ex:
                health_status[store.store_name] = {
                    "available": False,
                    "error": str(ex)
                }
        
        return health_status

Security Best Practices
=======================

Secret Storage Guidelines
-------------------------

1. **Use Appropriate Secret Stores**: 
   - Cloud stores for production environments
   - Local stores for development and testing
   
2. **Implement Secret Rotation**: Regularly rotate sensitive secrets

3. **Principle of Least Privilege**: Grant minimal required permissions

4. **Audit Secret Access**: Log secret retrieval operations

5. **Encrypt in Transit**: Use HTTPS/TLS for all cloud communications

6. **Secure Local Storage**: Protect local keystore files with appropriate file permissions

Configuration Security
----------------------

.. code-block:: yaml

    # Good practices in configuration
    secrets_manager:
      cloud_stores:
        production_vault:
          store_type: "azure"
          priority: 100
          vault_url: "https://prod-vault.vault.azure.net/"
          session_name: "azure_prod"
          # Never store credentials directly in config files
          
    # Use environment variables for sensitive configuration
    cloud_sessions:
      - name: "azure_prod"
        session_type: "azure"
        subscription_id: "ENV/AZURE_SUBSCRIPTION_ID"  # From environment
        tenant_id: "ENV/AZURE_TENANT_ID"              # From environment

Error Handling
==============

The secrets management system provides comprehensive error handling:

.. code-block:: python

    from dtPyAppFramework.settings.secrets.secret_store import SecretsStoreException
    from dtPyAppFramework.settings import Settings
    import logging
    
    settings = Settings()
    
    try:
        critical_secret = settings.secret_manager.get_secret('critical_api_key')
        if not critical_secret:
            raise ValueError("Critical secret 'critical_api_key' not found")
            
    except SecretsStoreException as ex:
        logging.error(f"Secret store error: {ex}")
        # Handle secret store connectivity issues
        
    except Exception as ex:
        logging.error(f"Unexpected error accessing secrets: {ex}")
        # Handle other potential issues

Common Error Scenarios:

* **Store Unavailable**: Network connectivity issues with cloud providers
* **Authentication Failures**: Invalid credentials or expired tokens
* **Permission DCanenied**: Insufficient access rights to secret stores
* **Secret Not Found**: Requested secret doesn't exist in any store
* **Encryption Errors**: Local keystore corruption or wrong password

The secrets management system provides a robust, secure foundation for handling sensitive data across diverse deployment environments while maintaining ease of use and configuration flexibility.