=========
Changelog
=========

All notable changes to dtPyAppFramework will be documented in this file.

The format is based on `Keep a Changelog <https://keepachangelog.com/en/1.0.0/>`_,
and this project adheres to `Semantic Versioning <https://semver.org/spec/v2.0.0.html>`_.

[Unreleased]
============

*No unreleased changes.*

[4.0.1] - 2025-12-18
====================

Added
-----
- **Multi-process file locking for local keystore**: Added thread-safe access to local secrets store via file locking, enabling multiple containers/processes to safely share the same keystore file
- **Atomic write operations for keystore**: Keystore writes now use atomic file operations (write to temp file, then rename) to prevent data corruption during concurrent access
- **Configurable lock timeout**: Lock acquisition timeout can be configured via ``KEYSTORE_LOCK_TIMEOUT`` environment variable (default: 30 seconds)
- Added ``filelock~=3.16.0`` dependency for cross-platform file locking support
- Documentation for multi-process and container access patterns in secrets management guide
- **Container-specific temp paths**: In container mode, temp directories now use ``{container_name}_{process_id}`` structure to prevent collisions between container instances
- **Container-specific log paths**: In container mode, logs are now organised under ``{container_name}/{timestamp}`` structure for easier log management across multiple containers
- **Container identifier resolution**: New ``_get_container_identifier()`` method supporting ``CONTAINER_NAME``, ``POD_NAME``, ``HOSTNAME`` environment variables

Changed
-------
- ``PasswordProtectedKeystoreWithHMAC`` class now supports multi-process concurrent access with automatic file locking
- Improved keystore write reliability with atomic file operations
- Container mode path structure now supports multiple containers sharing the same volume mounts

[4.0.0] - 2025-12-01
====================

Added
-----
- Comprehensive RST documentation with modular structure
- Component-specific documentation for all major framework parts
- API reference documentation with examples
- Installation and getting started guides
- Enhanced ``SystemPasswordGenerator`` for secure keystore access in containerised environments
- v3keystore format with improved security and entropy

Changed
-------
- Improved documentation organisation with separate component documents
- Enhanced code examples and usage patterns
- Migrated to v3keystore format with automatic migration from v2keystore

Removed
-------
- Deprecated v1 keystore format support

[3.1.0] - 2024-01-15
=====================

Added
-----
- Enhanced multiprocessing support with job coordination
- Improved secrets management with multi-cloud support
- Added Azure Key Vault integration
- Enhanced logging system with cross-process coordination
- Windows service support improvements

Changed
-------
- Updated configuration system for better hierarchical merging
- Improved error handling across all components
- Enhanced path management for cross-platform compatibility

Fixed
-----
- Fixed path resolution issues in development mode
- Corrected secret store initialization race conditions
- Improved memory management in multiprocessing scenarios

[3.0.0] - 2023-12-01
=====================

Added
-----
- Complete framework architecture redesign
- Singleton pattern implementation for core components
- Advanced configuration management with hot-reload
- Multi-cloud secrets integration (AWS, Azure)
- Sophisticated logging system with nested process support
- Cross-platform path management
- Resource management system
- Cloud session management

Changed
-------
- **BREAKING**: Restructured package organization
- **BREAKING**: Updated configuration file format
- **BREAKING**: Changed secrets management API
- Improved performance across all components
- Enhanced error handling and logging

Removed
-------
- Legacy configuration system
- Deprecated secret store implementations
- Old path management utilities

[2.x.x]
=======

Previous versions focused on basic application framework functionality.
See git history for detailed changes in 2.x releases.

Migration Guides
================

Migrating from 2.x to 3.x
--------------------------

The 3.x release includes significant breaking changes. Here are the key migration steps:

**Configuration Changes:**

.. code-block:: yaml

    # Old format (2.x)
    app_name: "MyApp"
    database_host: "localhost"
    
    # New format (3.x)
    app:
      name: "MyApp"
    database:
      host: "localhost"

**Application Class Changes:**

.. code-block:: python

    # Old format (2.x)
    class MyApp(BaseApp):
        def __init__(self):
            super().__init__("MyApp", "1.0.0")
    
    # New format (3.x)
    class MyApp(AbstractApp):
        def __init__(self):
            super().__init__(
                description="My Application",
                version="1.0.0",
                short_name="myapp",
                full_name="My Application"
            )

**Secrets Management Changes:**

.. code-block:: python

    # Old format (2.x)
    from dtPyAppFramework.secrets import SecretStore
    store = SecretStore()
    secret = store.get("api_key")
    
    # New format (3.x)
    from dtPyAppFramework.settings import Settings
    settings = Settings()
    secret = settings.secret_manager.get_secret("api_key")
    # Or through configuration
    secret = settings.get("SEC/api_key")

For detailed migration assistance, please refer to the migration guide in the documentation or contact support.

Deprecation Policy
==================

dtPyAppFramework follows semantic versioning:

- **Major versions** (X.0.0): May include breaking changes with migration path
- **Minor versions** (x.Y.0): Add new features, maintain backward compatibility
- **Patch versions** (x.y.Z): Bug fixes and security updates only

Features marked as deprecated will be removed in the next major version. 
Deprecation warnings will be added at least one minor version before removal.

Support Matrix
==============

Current Version Support
-----------------------

- **4.0.x**: Active development, full support
- **3.x**: Security updates only
- **2.x**: End of life, no updates

Python Version Support
----------------------

- **Python 3.12+**: Full support
- **Python 3.11**: Limited support (framework may work but not officially tested)
- **Python 3.10 and below**: Not supported

Platform Support
-----------------

- **Windows 10/11**: Full support
- **macOS 10.15+**: Full support
- **Linux (Ubuntu 20.04+, CentOS 8+)**: Full support
- **Other platforms**: Community support

Contributing
============

For information about contributing to dtPyAppFramework, please see the
:doc:`contributing` guide.

Reporting Issues
================

If you encounter any issues or have feature requests, please:

1. Check existing issues on the project repository
2. Create a new issue with detailed information
3. Include version information and platform details
4. Provide minimal reproduction examples when possible

Security Updates
================

Security vulnerabilities are taken seriously. If you discover a security issue:

1. **Do not** create a public issue
2. Email security details to the project maintainers
3. Allow reasonable time for response and fix
4. Coordinate disclosure timing with maintainers

Security updates will be released as patch versions and clearly marked in the changelog.