=========================
Paths and Resources Management
=========================

The Paths and Resources Management system provides cross-platform path handling, automatic directory creation, development/production mode support, and prioritized resource resolution for application assets.

Overview
========

dtPyAppFramework's path management system abstracts away platform-specific directory structures and provides consistent path handling across Windows, macOS, and Linux. The system automatically adapts to different deployment modes and handles:

* **Cross-Platform Compatibility**: Platform-specific standard locations for different types of data
* **Container Mode Support**: Simplified working directory-based structure for containerized deployments
* **Development Mode Support**: Simplified directory structure for development environments  
* **Automatic Directory Creation**: On-demand creation of required directories with proper permissions
* **Resource Resolution**: Priority-based resource file discovery and loading
* **Environment Integration**: Seamless integration with environment variables and configuration

Core Components
===============

ApplicationPaths
----------------

The ``ApplicationPaths`` class is the central component for managing all application directories.

.. autoclass:: dtPyAppFramework.paths.ApplicationPaths
   :members:
   :inherited-members:

Key Features:

**Singleton Pattern**
  Ensures consistent path handling across the entire application with a single source of truth for all directory paths.

**Cross-Platform Support**
  Automatically detects the operating system and uses appropriate standard locations:
  
  * **Windows**: Uses ``%LOCALAPPDATA%``, ``%APPDATA%``, ``%ALLUSERSPROFILE%``, ``%TEMP%``
  * **macOS**: Uses ``~/Library``, ``/Library/Application Support``, ``$TMPDIR``
  * **Linux**: Uses XDG directories for regular users; ``/var/log``, ``/var/lib``, ``/etc`` for root/service contexts

**Deployment Mode Detection**
  Automatically adapts directory structure based on deployment mode:
  
  * **Container Mode**: ``CONTAINER_MODE`` environment variable or ``--container`` argument
  * **Development Mode**: ``DEV_MODE`` environment variable or ``--single_folder`` argument

ResourceManager
---------------

The ``ResourceManager`` class handles discovery and loading of application resources with priority-based resolution.

.. autoclass:: dtPyAppFramework.resources.ResourceManager
   :members:
   :inherited-members:

Key Features:

**Priority-Based Resolution**
  Searches for resources in priority order, allowing for user customization and system defaults:
  
  1. User data directory (Priority 100) - Highest priority
  2. Application data directory (Priority 200) - Medium priority  
  3. Working directory (Priority 300) - Lowest priority

**Dynamic Path Management**
  Add and remove resource paths dynamically with custom priorities.

Directory Structure
===================

Production Mode Paths
----------------------

In production mode, the framework uses platform-specific standard locations:

**Windows**:

.. code-block:: text

    Logging: %LOCALAPPDATA%\AppName\logs\
    App Data: %ALLUSERSPROFILE%\AppName\
    User Data: %APPDATA%\AppName\
    Temp: %TEMP%\AppName\

**macOS**:

.. code-block:: text

    Logging: ~/Library/Logs/AppName/
    App Data: /Library/Application Support/AppName/
    User Data: ~/Library/Application Support/AppName/
    Temp: $TMPDIR/AppName/

**Linux (root/service)**:

.. code-block:: text

    Logging: /var/log/AppName/
    App Data: /var/lib/AppName/
    User Data: /etc/AppName/
    Temp: {tempdir}/AppName/

**Linux (regular user)**:

.. code-block:: text

    Logging: $XDG_STATE_HOME/AppName/log/  (default: ~/.local/state/AppName/log/)
    App Data: $XDG_CONFIG_HOME/AppName/    (default: ~/.config/AppName/)
    User Data: $XDG_DATA_HOME/AppName/     (default: ~/.local/share/AppName/)
    Temp: {tempdir}/AppName/

Container Mode Paths
---------------------

When ``CONTAINER_MODE`` is enabled (via ``--container`` flag or ``CONTAINER_MODE`` environment variable), all directories are created within the working directory with a structure optimised for multi-container deployments:

.. code-block:: text

    Working Directory/
    ├── config/                           # Configuration files (single layer)
    ├── data/                             # Unified data directory
    │   ├── keystore/                    # Secret storage
    │   └── resources/                   # Application resources
    ├── logs/
    │   └── {container_name}/            # Container-specific log folder
    │       └── {timestamp}/             # Timestamped log sessions
    └── temp/
        └── {container_name}_{pid}/      # Process-isolated temp folder

**Container Identifier Resolution**

The container name is determined from the following environment variables (in order of priority):

1. ``CONTAINER_NAME`` - Explicitly set container name
2. ``POD_NAME`` - Kubernetes pod name
3. ``HOSTNAME`` - Docker default (usually container ID or custom hostname)
4. Fallback to ``socket.gethostname()``

**Example Docker Compose Configuration:**

.. code-block:: yaml

    version: '3.8'
    services:
      coordinator:
        image: myapp:latest
        hostname: coordinator
        environment:
          - CONTAINER_MODE=true
          - CONTAINER_NAME=coordinator
        volumes:
          - app_logs:/app/logs
          - app_temp:/app/temp

      worker:
        image: myapp:latest
        deploy:
          replicas: 3
        environment:
          - CONTAINER_MODE=true
          # CONTAINER_NAME not set - uses HOSTNAME (e.g., worker_1, worker_2)
        volumes:
          - app_logs:/app/logs
          - app_temp:/app/temp

    volumes:
      app_logs:
      app_temp:

**Resulting Directory Structure (with 3 workers):**

.. code-block:: text

    /app/
    ├── logs/
    │   ├── coordinator/
    │   │   └── 20251217_140532/
    │   │       ├── info-myapp.log
    │   │       └── error-myapp.log
    │   ├── worker_1/
    │   │   └── 20251217_140535/
    │   ├── worker_2/
    │   │   └── 20251217_140536/
    │   └── worker_3/
    │       └── 20251217_140537/
    └── temp/
        ├── coordinator_1/
        ├── worker_1_42/
        ├── worker_2_43/
        └── worker_3_44/

Key characteristics of container mode:

- **Single Configuration Layer**: Only ``./config/config.yaml`` is used
- **Volume Mount Ready**: Directory structure designed for persistent volume mounting
- **Container Isolation**: Logs and temp files organised by container name
- **Process Isolation**: Temp directories include process ID to prevent collisions
- **Simplified Permissions**: No multi-user directory handling
- **Environment Integration**: Optimised for container orchestration platforms

Development Mode Paths
----------------------

When ``DEV_MODE`` is enabled, all directories are created relative to the current working directory:

.. code-block:: text

    Working Directory/
    ├── logs/                    # Logging directory
    ├── data/
    │   ├── app/                # Application data
    │   └── usr/                # User data  
    └── temp/                   # Temporary files

This simplified structure makes development easier and keeps all application files contained within the project directory.

Path Management Usage
=====================

Basic Path Access
-----------------

.. code-block:: python

    from dtPyAppFramework.paths import ApplicationPaths
    import os

    # Get the singleton paths instance
    paths = ApplicationPaths(app_short_name="myapp")

    # Access different directory types
    log_dir = paths.logging_root_path
    app_data_dir = paths.app_data_root_path
    user_data_dir = paths.usr_data_root_path
    temp_dir = paths.tmp_root_path

    # Use paths for file operations
    config_file = os.path.join(app_data_dir, "config", "settings.yaml")
    user_preferences = os.path.join(user_data_dir, "preferences.json")
    temp_file = os.path.join(temp_dir, "processing_data.tmp")

Environment Variable Integration
--------------------------------

The paths are automatically available as environment variables:

.. code-block:: python

    import os
    from dtPyAppFramework.paths import ApplicationPaths

    # Initialize paths (automatically sets environment variables)
    paths = ApplicationPaths(app_short_name="myapp")

    # Access through environment variables
    log_path = os.environ.get('dt_LOGGING_PATH')
    app_data_path = os.environ.get('dt_APP_DATA')
    usr_data_path = os.environ.get('dt_USR_DATA')
    tmp_path = os.environ.get('dt_TMP')

    # These can be used in configuration files
    # Example: log_file: "ENV/dt_LOGGING_PATH/application.log"

Advanced Path Configuration
---------------------------

.. code-block:: python

    from dtPyAppFramework.paths import ApplicationPaths

    class MyApplication(AbstractApp):
        def __init__(self):
            super().__init__(
                description="My Application",
                version="1.0.0", 
                short_name="myapp",
                full_name="My Application"
            )

        def initialize_custom_paths(self):
            """Initialize paths with custom configuration."""
            paths = ApplicationPaths(
                app_short_name=self.short_name,
                forced_os="Linux",          # Force specific OS behavior
                forced_dev_mode=True,       # Force development mode
                auto_create=True,           # Automatically create directories
                clean_temp=True,            # Clean temp directory on startup
                spawned_instance=False,     # Not a spawned process
                worker_id=None              # No worker ID
            )
            
            # Log the configured paths
            paths.log_paths()
            
            return paths

Spawned Process Path Handling
-----------------------------

In multiprocessing scenarios, each spawned process gets its own temporary directory:

.. code-block:: python

    from dtPyAppFramework.paths import ApplicationPaths

    def worker_function(worker_id):
        """Function executed in spawned process."""
        # Worker gets its own path context
        paths = ApplicationPaths(
            app_short_name="myapp",
            spawned_instance=True,
            worker_id=worker_id
        )
        
        # Worker temp directory: /temp/myapp/worker_1/
        worker_temp = paths.tmp_root_path
        
        # Process-specific logging and data handling
        import logging
        logging.info(f"Worker {worker_id} using temp dir: {worker_temp}")

Resource Management
===================

Basic Resource Usage
--------------------

.. code-block:: python

    from dtPyAppFramework.resources import ResourceManager
    import json

    # Get resource manager instance
    resources = ResourceManager()

    # Find and load a resource file
    config_template_path = resources.get_resource_path("templates/config.yaml")
    if config_template_path:
        with open(config_template_path, 'r') as f:
            template_content = f.read()

    # Load JSON resource
    data_file_path = resources.get_resource_path("data/reference_data.json")
    if data_file_path:
        with open(data_file_path, 'r') as f:
            reference_data = json.load(f)

Custom Resource Paths
---------------------

.. code-block:: python

    from dtPyAppFramework.resources import ResourceManager

    # Get resource manager
    resources = ResourceManager()

    # Add custom resource paths with priorities
    resources.add_resource_path("/opt/myapp/resources", priority=50)  # High priority
    resources.add_resource_path("/usr/share/myapp", priority=250)     # Low priority

    # Resource resolution order is now:
    # 1. /opt/myapp/resources (priority 50)
    # 2. ~/.config/AppName/resources (priority 100) - user data
    # 3. /etc/AppName/resources (priority 200) - app data  
    # 4. /usr/share/myapp (priority 250)
    # 5. ./resources (priority 300) - working directory

    # Find resource (searches in priority order)
    template_path = resources.get_resource_path("email_template.html")

Resource Directory Structure
----------------------------

Organize resources in a logical directory structure:

.. code-block:: text

    resources/
    ├── templates/
    │   ├── email/
    │   │   ├── welcome.html
    │   │   └── notification.txt
    │   └── config/
    │       └── default_settings.yaml
    ├── data/
    │   ├── reference_data.json
    │   ├── lookup_tables.csv
    │   └── translations/
    │       ├── en.json
    │       └── es.json
    ├── static/
    │   ├── css/
    │   ├── js/
    │   └── images/
    └── schemas/
        ├── api_schema.json
        └── config_schema.yaml

Advanced Resource Management
============================

Resource Loading Utilities
---------------------------

Create utility functions for common resource loading patterns:

.. code-block:: python

    from dtPyAppFramework.resources import ResourceManager
    import json
    import yaml
    import logging

    class ResourceLoader:
        def __init__(self):
            self.resources = ResourceManager()
            self.logger = logging.getLogger(__name__)
        
        def load_json_resource(self, resource_name, default=None):
            """Load a JSON resource with error handling."""
            try:
                resource_path = self.resources.get_resource_path(resource_name)
                if resource_path:
                    with open(resource_path, 'r', encoding='utf-8') as f:
                        return json.load(f)
                else:
                    self.logger.warning(f"Resource not found: {resource_name}")
                    return default
            except Exception as ex:
                self.logger.error(f"Error loading JSON resource {resource_name}: {ex}")
                return default
        
        def load_yaml_resource(self, resource_name, default=None):
            """Load a YAML resource with error handling."""
            try:
                resource_path = self.resources.get_resource_path(resource_name)
                if resource_path:
                    with open(resource_path, 'r', encoding='utf-8') as f:
                        return yaml.safe_load(f)
                else:
                    self.logger.warning(f"Resource not found: {resource_name}")
                    return default
            except Exception as ex:
                self.logger.error(f"Error loading YAML resource {resource_name}: {ex}")
                return default
        
        def load_text_resource(self, resource_name, encoding='utf-8'):
            """Load a text resource."""
            try:
                resource_path = self.resources.get_resource_path(resource_name)
                if resource_path:
                    with open(resource_path, 'r', encoding=encoding) as f:
                        return f.read()
                return None
            except Exception as ex:
                self.logger.error(f"Error loading text resource {resource_name}: {ex}")
                return None

    # Usage
    loader = ResourceLoader()
    config_template = loader.load_yaml_resource("templates/config/default.yaml")
    translations = loader.load_json_resource("data/translations/en.json", {})

Resource Caching
-----------------

Implement caching for frequently accessed resources:

.. code-block:: python

    from functools import lru_cache
    import os
    import time

    class CachedResourceManager:
        def __init__(self, cache_size=128, ttl_seconds=300):
            self.resources = ResourceManager()
            self.cache_size = cache_size
            self.ttl = ttl_seconds
            self._cache_timestamps = {}
        
        @lru_cache(maxsize=128)
        def _cached_resource_path(self, resource_name):
            """Cache resource paths with LRU eviction."""
            return self.resources.get_resource_path(resource_name)
        
        def get_cached_resource_content(self, resource_name):
            """Get resource content with time-based cache invalidation."""
            cache_key = f"content_{resource_name}"
            
            # Check if cache entry exists and is still valid
            if (cache_key in self._cache_timestamps and 
                time.time() - self._cache_timestamps[cache_key] < self.ttl):
                return getattr(self, cache_key, None)
            
            # Load fresh content
            resource_path = self._cached_resource_path(resource_name)
            if resource_path and os.path.exists(resource_path):
                with open(resource_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Cache the content
                setattr(self, cache_key, content)
                self._cache_timestamps[cache_key] = time.time()
                return content
            
            return None

Template and Asset Management
=============================

Template Loading
----------------

.. code-block:: python

    from jinja2 import Environment, FileSystemLoader
    from dtPyAppFramework.resources import ResourceManager

    class TemplateManager:
        def __init__(self):
            self.resources = ResourceManager()
            self._setup_template_environment()
        
        def _setup_template_environment(self):
            """Setup Jinja2 template environment with resource paths."""
            template_paths = []
            
            # Add all resource paths as template search paths
            for path_info in self.resources.resource_paths:
                template_dir = os.path.join(path_info[0], 'templates')
                if os.path.exists(template_dir):
                    template_paths.append(template_dir)
            
            # Create Jinja2 environment
            self.env = Environment(
                loader=FileSystemLoader(template_paths),
                trim_blocks=True,
                lstrip_blocks=True
            )
        
        def render_template(self, template_name, **kwargs):
            """Render a template with given context."""
            try:
                template = self.env.get_template(template_name)
                return template.render(**kwargs)
            except Exception as ex:
                import logging
                logging.error(f"Error rendering template {template_name}: {ex}")
                return None

    # Usage
    template_manager = TemplateManager()
    
    # Render email template
    email_content = template_manager.render_template(
        'email/welcome.html',
        user_name='John Doe',
        app_name='MyApp'
    )

Static Asset Management
-----------------------

.. code-block:: python

    import mimetypes
    from dtPyAppFramework.resources import ResourceManager

    class AssetManager:
        def __init__(self):
            self.resources = ResourceManager()
        
        def serve_asset(self, asset_path):
            """Serve static asset with proper content type."""
            full_path = self.resources.get_resource_path(f"static/{asset_path}")
            
            if full_path and os.path.exists(full_path):
                content_type, _ = mimetypes.guess_type(full_path)
                
                with open(full_path, 'rb') as f:
                    content = f.read()
                
                return {
                    'content': content,
                    'content_type': content_type or 'application/octet-stream',
                    'path': full_path
                }
            
            return None
        
        def get_asset_url(self, asset_path):
            """Get URL for static asset (useful for web applications)."""
            full_path = self.resources.get_resource_path(f"static/{asset_path}")
            if full_path:
                return f"/static/{asset_path}"
            return None

Configuration Integration
=========================

Path Aliases in Configuration
------------------------------

Use path aliases in configuration files:

.. code-block:: yaml

    # config.yaml
    application:
      data_directory: "<APP>/application_data"
      user_preferences: "<USR>/preferences.json"
      temp_workspace: "<TMP>/workspace"
      
    logging:
      file_path: "<USR>/logs/application.log"
      
    resources:
      template_cache: "<TMP>/template_cache"
      asset_cache: "<USR>/asset_cache"

These aliases are automatically resolved by the Settings system:

.. code-block:: python

    from dtPyAppFramework.settings import Settings

    settings = Settings()

    # Aliases automatically resolved to actual paths
    data_dir = settings.get('application.data_directory')
    # Returns: /home/user/.config/myapp/application_data (on Linux)

    preferences_file = settings.get('application.user_preferences')  
    # Returns: /home/user/.config/myapp/preferences.json

Cross-Platform Considerations
=============================

File System Permissions
------------------------

Handle platform-specific permission requirements:

.. code-block:: python

    import os
    import stat
    import platform
    from dtPyAppFramework.paths import ApplicationPaths

    def setup_secure_directory(directory_path):
        """Create directory with appropriate permissions."""
        os.makedirs(directory_path, exist_ok=True)
        
        if platform.system() != "Windows":
            # Set restrictive permissions on Unix-like systems
            os.chmod(directory_path, stat.S_IRWXU)  # Owner read/write/execute only
        
    def setup_shared_directory(directory_path):
        """Create directory for shared access."""
        os.makedirs(directory_path, exist_ok=True)
        
        if platform.system() != "Windows":
            # More permissive permissions for shared access
            os.chmod(directory_path, stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP)

Path Separator Handling
-----------------------

.. code-block:: python

    import os
    from dtPyAppFramework.resources import ResourceManager

    def cross_platform_resource_path(*path_parts):
        """Build resource path with proper separators."""
        resource_name = os.path.join(*path_parts)
        
        # Normalize path separators for current platform
        resource_name = os.path.normpath(resource_name)
        
        resources = ResourceManager()
        return resources.get_resource_path(resource_name)

    # Usage - works on all platforms
    config_path = cross_platform_resource_path('config', 'database', 'settings.yaml')
    template_path = cross_platform_resource_path('templates', 'email', 'welcome.html')

Best Practices
==============

1. **Use Framework Paths**: Always use ApplicationPaths instead of hard-coded paths
2. **Resource Priority**: Organize resources by priority (user > app > default)
3. **Development Mode**: Use ``DEV_MODE`` for simplified development workflows
4. **Cross-Platform Testing**: Test path handling on different operating systems
5. **Permissions**: Set appropriate file and directory permissions
6. **Cleanup**: Implement cleanup for temporary files and directories
7. **Error Handling**: Handle missing resources gracefully with fallbacks
8. **Caching**: Cache frequently accessed resources for better performance

Error Handling
==============

.. code-block:: python

    from dtPyAppFramework.paths import ApplicationPaths
    from dtPyAppFramework.resources import ResourceManager
    import logging
    import os

    def robust_path_handling():
        """Example of robust path and resource handling."""
        logger = logging.getLogger(__name__)
        
        try:
            # Initialize paths
            paths = ApplicationPaths(app_short_name="myapp")
            
            # Verify critical directories exist
            if not os.path.exists(paths.usr_data_root_path):
                logger.warning(f"User data directory does not exist: {paths.usr_data_root_path}")
                os.makedirs(paths.usr_data_root_path, exist_ok=True)
            
            # Handle resource loading with fallbacks
            resources = ResourceManager()
            
            config_path = resources.get_resource_path("config/default.yaml")
            if not config_path:
                logger.warning("Default config not found, using built-in defaults")
                # Use built-in configuration
                config_path = create_default_config(paths.usr_data_root_path)
            
            return config_path
            
        except PermissionError as ex:
            logger.error(f"Permission denied accessing paths: {ex}")
            raise
        except OSError as ex:
            logger.error(f"OS error with path operations: {ex}")
            raise
        except Exception as ex:
            logger.error(f"Unexpected error in path handling: {ex}")
            raise

The paths and resources management system provides a robust, cross-platform foundation for handling application directories and assets while maintaining simplicity for developers and flexibility for different deployment scenarios.