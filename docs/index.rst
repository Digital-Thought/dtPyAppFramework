=============================
dtPyAppFramework Documentation
=============================

Welcome to dtPyAppFramework
===========================

dtPyAppFramework is a comprehensive Python framework library designed as the foundation for creating robust Python applications. It provides enterprise-grade features including layered configuration management, multi-cloud secrets storage, advanced multi-processing task management, sophisticated logging with nested support for spawned processes, singleton pattern utilities, and application path management.

Key Features
============

* **Container Mode Support**: Full containerization support with ``--container`` flag for Docker and Kubernetes deployments
* **AppContext Unified Facade**: Single singleton providing convenient access to metadata, paths, settings, secrets, and resources
* **Metadata Auto-Discovery**: Application metadata loaded from text files when constructor arguments are omitted
* **AbstractApp Base Class**: Structured application foundation with built-in lifecycle management
* **Layered Configuration Management**: Three-tier configuration system with automatic merging (single layer in container mode)
* **Multi-Cloud Secrets Management**: Unified interface for Azure Key Vault, AWS Secrets Manager, and local encrypted storage
* **Advanced Multi-Processing**: Process spawning, coordination, and monitoring with psutil integration
* **Sophisticated Logging**: Nested logging contexts with cross-process synchronization and color coding
* **Cross-Platform Path Management**: Automatic application path detection and management
* **Security Framework**: Comprehensive validation, encryption, and secure file handling
* **Singleton Pattern Utilities**: Thread-safe singleton generation with key-based multiple instances
* **Resource Management**: Prioritized resource path resolution system

Quick Start
===========

.. code-block:: python

    from dtPyAppFramework.application import AbstractApp

    class MyApplication(AbstractApp):
        def __init__(self):
            super().__init__(
                description="My Application",
                version="1.0.0",
                short_name="myapp",
                full_name="My Application"
            )

        def define_args(self, arg_parser):
            # Define your command-line arguments here
            arg_parser.add_argument('--config', help='Configuration file path')

        def main(self, args):
            # Your application logic here
            self.logger.info("Application started")

        def exiting(self):
            # Cleanup logic here
            pass

    if __name__ == "__main__":
        app = MyApplication()
        app.run()  # Runs by default; --run argument is optional

Documentation Sections
======================

.. toctree::
   :maxdepth: 2
   :caption: User Guides

   guides/installation
   guides/getting-started

.. toctree::
   :maxdepth: 2
   :caption: Framework Components

   components/application
   components/configuration
   components/secrets-management
   components/logging
   components/multiprocessing
   components/paths-resources
   components/cloud-integration
   components/decorators

.. toctree::
   :maxdepth: 2
   :caption: Examples

   examples/basic-application
   examples/multiprocessing-application
   examples/cloud-secrets
   examples/advanced-configuration

.. toctree::
   :maxdepth: 2
   :caption: API Reference

   api/application
   api/settings
   api/secrets
   api/logging
   api/process
   api/paths
   api/resources
   api/cloud
   api/decorators

.. toctree::
   :maxdepth: 1
   :caption: Additional Information

   changelog
   contributing
   license

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`