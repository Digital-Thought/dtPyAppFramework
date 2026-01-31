============
Settings API
============

The Settings API provides configuration management, settings readers, and integration with the secrets management system.

.. currentmodule:: dtPyAppFramework.settings

Settings
========

.. autoclass:: Settings
   :members:
   :undoc-members:
   :show-inheritance:
   :inherited-members: dict

   .. automethod:: __init__

   **Configuration Access**
   
   .. automethod:: get
   .. automethod:: set
   .. automethod:: __getitem__
   .. automethod:: __setitem__
   .. automethod:: __getattr__

   **Raw Settings Management**
   
   .. automethod:: get_raw_settings
   .. automethod:: persist_settings

   **Initialization**
   
   .. automethod:: init_settings_readers
   .. automethod:: close

   **Proxy Configuration**
   
   .. automethod:: get_requests_tor_proxy
   .. automethod:: get_selenium_tor_proxy

   **Internal Methods**
   
   .. automethod:: _replace_value
   .. automethod:: _lookup_alias_value

SettingsReader
==============

.. currentmodule:: dtPyAppFramework.settings.settings_reader

.. autoclass:: SettingsReader
   :members:
   :undoc-members:
   :show-inheritance:
   :inherited-members: dict

   .. automethod:: __init__

   **File Operations**
   
   .. automethod:: load_yaml_file
   .. automethod:: __getitem__

   **Properties**
   
   .. autoattribute:: CONFIG_FILE

ConfigFileWatcher
-----------------

.. autoclass:: ConfigFileWatcher
   :members:
   :undoc-members:
   :show-inheritance:

   .. automethod:: __init__

   **File Monitoring**
   
   .. automethod:: calculate_sha256
   .. automethod:: process
   .. automethod:: on_deleted
   .. automethod:: on_modified
   .. automethod:: on_created

Usage Examples
==============

Basic Configuration Access
---------------------------

.. code-block:: python

    from dtPyAppFramework.settings import Settings

    settings = Settings()

    # Get configuration values with defaults
    database_host = settings.get('database.host', 'localhost')
    database_port = settings.get('database.port', 5432)
    
    # Access nested configuration
    log_level = settings.get('logging.level', 'INFO')
    
    # Boolean values
    debug_mode = settings.get('application.debug', False)

Environment Variable Resolution
-------------------------------

.. code-block:: python

    # In config.yaml:
    # database:
    #   host: "ENV/DATABASE_HOST"
    #   port: "ENV/DATABASE_PORT"
    
    settings = Settings()
    
    # These resolve environment variables automatically
    db_host = settings.get('database.host')  # Gets os.environ['DATABASE_HOST']
    db_port = settings.get('database.port')  # Gets os.environ['DATABASE_PORT']

Secret Integration
------------------

.. code-block:: python

    # In config.yaml:
    # api:
    #   key: "SEC/api_key"
    #   secret: "SEC/api_secret"
    
    settings = Settings()
    
    # These resolve secrets automatically
    api_key = settings.get('api.key')      # Gets secret from secrets manager
    api_secret = settings.get('api.secret') # Gets secret from secrets manager

Path Aliases
------------

.. code-block:: python

    # In config.yaml:
    # application:
    #   data_dir: "<USR>/data"
    #   log_file: "<APP>/logs/app.log"
    
    settings = Settings()
    
    # These resolve to actual paths
    data_directory = settings.get('application.data_dir')  # User data path + /data
    log_file_path = settings.get('application.log_file')   # App data path + /logs/app.log

Custom Settings Reader
----------------------

.. code-block:: python

    from dtPyAppFramework.settings.settings_reader import SettingsReader
    from dtPyAppFramework.settings import Settings

    # Create custom settings reader
    custom_reader = SettingsReader('/custom/config/path', priority=50)
    
    # Add to settings
    settings = Settings()
    settings.settings_readers.append(custom_reader)
    settings.settings_readers.sort(key=lambda x: x.priority)

Configuration Validation
-------------------------

.. code-block:: python

    def validate_configuration():
        settings = Settings()
        
        required_settings = [
            'database.host',
            'database.name',
            'api.base_url'
        ]
        
        missing = []
        for setting in required_settings:
            if settings.get(setting) is None:
                missing.append(setting)
        
        if missing:
            raise ValueError(f"Missing required settings: {missing}")
        
        return True