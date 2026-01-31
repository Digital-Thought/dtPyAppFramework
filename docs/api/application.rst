===============
Application API
===============

The Application API provides the core foundation for building applications with dtPyAppFramework through the AbstractApp base class and ProcessManager.

.. currentmodule:: dtPyAppFramework.application

AbstractApp
===========

.. autoclass:: AbstractApp
   :members:
   :undoc-members:
   :show-inheritance:

   .. automethod:: __init__

   **Abstract Methods**
   
   These methods must be implemented by subclasses:

   .. automethod:: define_args
   .. automethod:: main
   .. automethod:: exiting

   **Properties**
   
   .. autoproperty:: version
   .. autoproperty:: description
   .. autoproperty:: short_name
   .. autoproperty:: full_name

   **Methods**
   
   .. automethod:: run
   .. automethod:: exit

Process Manager
===============

.. currentmodule:: dtPyAppFramework.process

.. autofunction:: is_multiprocess_spawned_instance

ProcessManager
--------------

.. autoclass:: ProcessManager
   :members:
   :undoc-members:
   :show-inheritance:

   .. automethod:: __init__

   **Core Methods**

   .. automethod:: initialise_application
   .. automethod:: load_config
   .. automethod:: request_shutdown
   .. automethod:: wait_for_shutdown
   .. automethod:: call_shutdown
   .. automethod:: handle_shutdown

   **Internal Methods**

   .. automethod:: __initialise_spawned_application__
   .. automethod:: __initialise_stdout_capt__
   .. automethod:: __add_secret__
   .. automethod:: __main__

AppContext
=========

.. currentmodule:: dtPyAppFramework.app_context

.. autoclass:: AppContext
   :members:
   :undoc-members:
   :show-inheritance:

   **Metadata Properties**

   .. autoproperty:: version
   .. autoproperty:: full_name
   .. autoproperty:: short_name
   .. autoproperty:: description

   **Path Properties**

   .. autoproperty:: logging_path
   .. autoproperty:: app_data_path
   .. autoproperty:: usr_data_path
   .. autoproperty:: tmp_path

   **Configuration**

   .. autoproperty:: config_file_paths
   .. automethod:: get_setting
   .. automethod:: set_setting

   **Secrets**

   .. automethod:: get_secret
   .. automethod:: set_secret
   .. automethod:: delete_secret

   **Resources**

   .. automethod:: get_resource_path

Usage Examples
==============

Basic Application
-----------------

.. code-block:: python

    from dtPyAppFramework.application import AbstractApp
    import logging

    class SimpleApp(AbstractApp):
        def __init__(self):
            super().__init__(
                description="A simple application",
                version="1.0.0",
                short_name="simpleapp",
                full_name="Simple Application"
            )

        def define_args(self, arg_parser):
            arg_parser.add_argument('--config', help='Configuration file')

        def main(self, args):
            logger = logging.getLogger(__name__)
            logger.info("Application started")
            # Your application logic here

        def exiting(self):
            import logging
            logging.info("Application exiting")

    if __name__ == "__main__":
        app = SimpleApp()
        app.run()  # --run argument is optional; app runs by default

Metadata Auto-Discovery
-------------------------

.. code-block:: python

    from dtPyAppFramework.application import AbstractApp

    class AutoDiscoveredApp(AbstractApp):
        def __init__(self):
            # Metadata loaded from _version.txt, _short_name.txt,
            # _full_name.txt, _description.txt in the package directory
            super().__init__()

        def define_args(self, arg_parser):
            pass

        def main(self, args):
            from dtPyAppFramework.app_context import AppContext
            ctx = AppContext()
            print(f"{ctx.full_name} v{ctx.version}")

        def exiting(self):
            pass

Application with Configuration
------------------------------

.. code-block:: python

    class ConfigurableApp(AbstractApp):
        def __init__(self):
            super().__init__(
                description="Application with configuration",
                version="1.0.0",
                short_name="configapp",
                full_name="Configurable Application"
            )

        def define_args(self, arg_parser):
            arg_parser.add_argument('--debug', action='store_true')

        def main(self, args):
            from dtPyAppFramework.settings import Settings
            settings = Settings()
            
            # Access configuration
            database_url = settings.get('database.url', 'sqlite:///default.db')
            api_key = settings.get('SEC/api_key')  # From secrets
            
            if args.debug:
                import logging
                logging.getLogger().setLevel(logging.DEBUG)

        def exiting(self):
            # Cleanup resources
            pass

Container Mode Application
--------------------------

.. code-block:: python

    import os
    from dtPyAppFramework.application import AbstractApp

    class ContainerApp(AbstractApp):
        def __init__(self):
            super().__init__(
                description="Container-optimized application",
                version="1.0.0",
                short_name="containerapp",
                full_name="Container Application"
            )

        def define_args(self, arg_parser):
            arg_parser.add_argument('--task', choices=['config', 'secrets', 'all'], 
                                  default='all', help='Demonstration task')

        def main(self, args):
            import logging
            logger = logging.getLogger(__name__)
            
            # Check container mode status
            container_mode = os.environ.get('CONTAINER_MODE', 'False')
            logger.info(f"Container Mode: {container_mode}")
            
            if args.task in ['config', 'all']:
                self.demonstrate_configuration()
            
            if args.task in ['secrets', 'all']:
                self.demonstrate_secrets()

        def demonstrate_configuration(self):
            from dtPyAppFramework.settings import Settings
            settings = Settings()
            
            # In container mode, only one config layer
            import logging
            logging.info(f"Config layers: {len(settings.settings_readers)}")

        def demonstrate_secrets(self):
            from dtPyAppFramework.settings import Settings
            settings = Settings()
            
            # Store and retrieve secrets (stored in ./data/keystore/ in container mode)
            if hasattr(settings, 'secret_manager') and settings.secret_manager:
                settings.secret_manager.set_secret('sample_key', 'sample_value')
                retrieved = settings.secret_manager.get_secret('sample_key')
                import logging
                logging.info(f"Secret retrieved: {'*' * len(str(retrieved))}")

        def exiting(self):
            import logging
            logging.info("Container application cleanup")

    if __name__ == "__main__":
        # Auto-detect container environment
        if os.path.exists('/.dockerenv') or os.environ.get('KUBERNETES_SERVICE_HOST'):
            os.environ['CONTAINER_MODE'] = 'True'
            print("Auto-detected container environment")
        
        app = ContainerApp()
        app.run()  # Use --container flag or set CONTAINER_MODE=true