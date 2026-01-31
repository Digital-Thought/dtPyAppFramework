=========
Changelog
=========

All notable changes to dtPyAppFramework will be documented in this file.

The format is based on `Keep a Changelog <https://keepachangelog.com/en/1.0.0/>`_,
and this project adheres to `Semantic Versioning <https://semver.org/spec/v2.0.0.html>`_.

[Unreleased]
============

*No unreleased changes.*

[4.1.1] - 2026-01-31
====================

Security
--------
- Increase PBKDF2 iteration count from 50,000 to 100,000 in password strengthening to meet OWASP PBKDF2-SHA256 minimum guidance

Fixed
-----
- Remove redundant try/except block in keystore that caught exceptions only to re-raise them
- Fix incorrect argument count in ``_add_secret_file`` call (blocker)
- Fix method in ``filesystem.py`` that always returned the same value (blocker)
- Replace bare ``except:`` clauses with specific exception types across source and test files
- Replace generic ``raise Exception(...)`` with specific exception types (``ValueError``, ``RuntimeError``)
- Merge nested ``if`` statements and remove redundant returns across secrets modules
- Remove unused variables and imports across source, test, and sample files
- Reduce cognitive complexity in 8 source functions by extracting helper methods
- Extract duplicated string literals into module-level constants
- Fix empty f-strings (no replacement fields) across sample files
- Add comments to intentionally empty method stubs in test fixtures
- Fix Kubernetes deployment: add ``automountServiceAccountToken: false``, storage limits, and specific image version tag
- Fix Dockerfile: merge consecutive RUN instructions
- Fix shell script: add explicit return statements, assign positional parameters to local variables, use ``[[`` for conditionals, redirect errors to stderr

Changed
-------
- Bump ``azure-core`` from ~=1.32.0 to ~=1.38.0 to address security vulnerability
- Bump ``filelock`` from ~=3.16.1 to ~=3.20.3 to address security vulnerability

[4.1.0] - 2026-01-31
====================

Added
-----
- **AppContext singleton facade**: New ``AppContext`` class providing unified access to application metadata, paths, settings, secrets, and resources
- **Metadata auto-discovery**: ``AbstractApp`` now loads version, short_name, full_name, and description from text files in the subclass's package directory when constructor arguments are omitted
- **Standardised metadata files**: ``_short_name.txt`` and ``_full_name.txt`` replace the previous ``_name.txt``
- **Sample applications**: New samples for AppContext usage and metadata auto-discovery
- **Project documentation**: CHANGELOG.md, SECURITY.md, CODE_OF_CONDUCT.md, CONTRIBUTING.md, GitHub issue/PR templates
- **Development dependencies**: ``requirements-dev.txt`` for development tooling
- **Test infrastructure**: ``tests/__init__.py`` and ``tests/conftest.py``

Changed
-------
- Update minimum Python version to 3.10 (from 3.9)
- Refactor ``LocalSecretStoresManager``: Remove two-class IPC pipe architecture in favour of direct store access with FileLock-based synchronisation
- Harden HMAC verification in ``PasswordProtectedKeystoreWithHMAC``: Verification failures now always raise exceptions rather than silently recreating the keystore
- Improve atomic write operations in keystore: Use ``tempfile.mkstemp()`` with ``os.replace()`` for safer file updates
- Correct ``ApplicationPaths`` for cross-platform compatibility: Replace f-string path concatenation with ``os.path.join()`` throughout, add XDG Base Directory compliance for Linux, and differentiate root vs non-root paths on Unix systems
- Update CI/CD workflow with test job, version verification, and tag-based triggers
- Reorganise samples README with updated learning path and feature matrix

Fixed
-----
- Fix AWS cloud session: ``ec2_session()`` now correctly returns the session object instead of returning ``None``
- Fix cloud secret store logging: AWS and Azure secret store success messages now log at INFO level instead of ERROR
- Fix AWS secret key parsing: Correct impossible ``len(parts) == 0`` condition after ``str.split()`` to properly handle single-segment and two-segment key formats

Removed
-------
- ``_name.txt`` metadata file (superseded by ``_short_name.txt`` and ``_full_name.txt``)

[4.0.4] - 2025-12-18
====================

Fixed
-----
- **Empty secret key handling**: Added defensive checks to prevent ``SecurityValidationError`` when empty keys are passed to ``get_secret`` methods. This can occur when configuration values contain ``SEC/`` without a key name, or when empty keys are passed programmatically. Empty keys now gracefully return ``None`` or the default value instead of raising an exception.

[4.0.3] - 2025-12-18
====================

Added
-----
- **Command-line keystore password**: New ``--password`` / ``-p`` argument to set ``KEYSTORE_PASSWORD`` environment variable from command line, providing an alternative to setting the environment variable directly

Changed
-------
- **Container mode keystore password**: In CONTAINER_MODE, ``KEYSTORE_PASSWORD`` or ``SECRETS_STORE_PASSWORD`` environment variables are now used directly without system fingerprint or path mixing, ensuring consistent keystore access across multiple containers sharing the same keystore file

[4.0.2] - 2025-12-18
====================

Added
-----
- **Container-specific temp paths**: In container mode, temp directories now use ``{container_name}_{process_id}`` structure to prevent collisions between container instances
- **Container-specific log paths**: In container mode, logs are now organised under ``{container_name}/{timestamp}`` structure for easier log management across multiple containers
- **Container identifier resolution**: New ``_get_container_identifier()`` method supporting ``CONTAINER_NAME``, ``POD_NAME``, ``HOSTNAME`` environment variables
- **Improved application shutdown handling**: New ``wait_for_shutdown()`` method for long-running applications and ``request_shutdown()`` for programmatic shutdown
- **Auto-exit for one-shot applications**: Applications that simply return from ``main()`` now exit automatically without needing to call shutdown methods
- New sample application ``daemon_app.py`` demonstrating long-running application pattern
- Updated documentation for application lifecycle patterns in ``application.rst``
- Updated documentation for container mode paths in ``paths-resources.rst``

Changed
-------
- Container mode path structure now supports multiple containers sharing the same volume mounts
- ``ProcessManager.__main__()`` now auto-detects one-shot vs long-running applications
- Signal handlers now use ``request_shutdown()`` instead of deprecated ``call_shutdown()``
- Updated ``simple_app/dev_app.py`` sample to demonstrate one-shot pattern (no explicit shutdown call needed)

Deprecated
----------
- ``ProcessManager.call_shutdown()`` is now deprecated in favour of ``request_shutdown()`` (still works for backward compatibility)

[4.0.1] - 2025-12-17
====================

Added
-----
- **Multi-process file locking for local keystore**: Added thread-safe access to local secrets store via file locking, enabling multiple containers/processes to safely share the same keystore file
- **Atomic write operations for keystore**: Keystore writes now use atomic file operations (write to temp file, then rename) to prevent data corruption during concurrent access
- **Configurable lock timeout**: Lock acquisition timeout can be configured via ``KEYSTORE_LOCK_TIMEOUT`` environment variable (default: 30 seconds)
- Added ``filelock~=3.16.0`` dependency for cross-platform file locking support
- Documentation for multi-process and container access patterns in secrets management guide

Changed
-------
- ``PasswordProtectedKeystoreWithHMAC`` class now supports multi-process concurrent access with automatic file locking
- Improved keystore write reliability with atomic file operations

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

- **4.1.x**: Active development, full support
- **4.0.x**: Security updates only
- **3.x**: Security updates only
- **2.x**: End of life, no updates

Python Version Support
----------------------

- **Python 3.12+**: Full support
- **Python 3.10-3.11**: Supported (minimum version is 3.10)
- **Python 3.9 and below**: Not supported

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