==================
Decorators
==================

The Decorators module provides utility decorators that implement common design patterns used throughout the dtPyAppFramework, with the singleton pattern being the primary focus for ensuring single instances of critical framework components.

Overview
========

dtPyAppFramework uses decorators to implement design patterns that enhance the framework's architecture and provide consistent behavior across components. The decorators help enforce:

* **Singleton Pattern**: Ensures single instances of critical framework components
* **Instance Management**: Controls object creation and lifecycle
* **Key-Based Instances**: Allows multiple instances based on key parameters
* **Thread Safety**: Provides safe concurrent access to singleton instances

Core Decorators
===============

Singleton Decorator
-------------------

The ``singleton`` decorator is the primary decorator used throughout the framework to implement the singleton pattern.

.. py:decorator:: dtPyAppFramework.decorators.singleton(key_name=None)

   Decorator to create a singleton class with optional key-based multiple instances.

   :param str key_name: Optional parameter name to monitor for creating multiple instances
   :return: Decorated class that behaves as a singleton
   :rtype: callable

**Key Features:**

**Basic Singleton Behavior**
  When used without parameters, ensures only one instance of the class exists throughout the application lifecycle.

**Key-Based Multiple Instances**  
  When provided with a ``key_name`` parameter, allows multiple instances based on the value of that key, while still maintaining singleton behavior for each unique key value.

**Thread-Safe Implementation**
  Uses proper synchronization to ensure safe access in multithreaded environments.

Basic Usage
===========

Simple Singleton
-----------------

.. code-block:: python

    from dtPyAppFramework.decorators import singleton

    @singleton()
    class DatabaseManager:
        def __init__(self):
            self.connection = None
            self.connected = False
            print("DatabaseManager instance created")

        def connect(self):
            if not self.connected:
                # Database connection logic
                self.connected = True
                print("Connected to database")

    # Usage
    db1 = DatabaseManager()  # Creates new instance
    db2 = DatabaseManager()  # Returns same instance

    print(db1 is db2)  # True - same instance
    # Output: DatabaseManager instance created
    #         True

Key-Based Singleton
-------------------

.. code-block:: python

    from dtPyAppFramework.decorators import singleton

    @singleton(key_name='database_name')
    class DatabaseConnection:
        def __init__(self, database_name='default', host='localhost'):
            self.database_name = database_name
            self.host = host
            self.connection = None
            print(f"DatabaseConnection created for {database_name}")

        def connect(self):
            print(f"Connecting to {self.database_name} at {self.host}")

    # Usage - multiple instances based on database_name
    db_users = DatabaseConnection(database_name='users')      # Creates new instance
    db_orders = DatabaseConnection(database_name='orders')    # Creates new instance  
    db_users2 = DatabaseConnection(database_name='users')     # Returns existing 'users' instance

    print(db_users is db_users2)   # True - same instance for 'users'
    print(db_users is db_orders)   # False - different instances
    
    # Output: DatabaseConnection created for users
    #         DatabaseConnection created for orders
    #         True
    #         False

Framework Integration
=====================

The singleton decorator is extensively used throughout the dtPyAppFramework:

ApplicationPaths Singleton
--------------------------

.. code-block:: python

    from dtPyAppFramework.decorators import singleton

    @singleton()
    class ApplicationPaths(object):
        def __init__(self, app_short_name, forced_os=None, ...):
            # Initialization logic
            self.app_short_name = app_short_name
            # ...

    # Framework ensures single paths instance
    paths1 = ApplicationPaths(app_short_name="myapp")
    paths2 = ApplicationPaths(app_short_name="myapp")  # Same instance returned

Settings Singleton
------------------

.. code-block:: python

    @singleton()
    class Settings(dict):
        def __init__(self, application_paths=None, app_short_name=None):
            # Settings initialization
            pass

    # Single settings instance throughout application
    settings1 = Settings()
    settings2 = Settings()  # Same instance

CloudSessionManager Singleton
-----------------------------

.. code-block:: python

    @singleton()
    class CloudSessionManager(object):
        def __init__(self):
            # Load cloud sessions
            pass

    # Single session manager for all cloud operations
    manager = CloudSessionManager()

Advanced Usage Patterns
=======================

Factory Pattern with Singleton
-------------------------------

Combine singleton with factory patterns for controlled object creation:

.. code-block:: python

    from dtPyAppFramework.decorators import singleton
    from abc import ABC, abstractmethod

    @singleton(key_name='service_type')
    class ServiceFactory:
        def __init__(self, service_type):
            self.service_type = service_type
            self.services = {}
        
        def create_service(self, service_name, **kwargs):
            """Create or return existing service instance."""
            if service_name not in self.services:
                if self.service_type == 'database':
                    self.services[service_name] = DatabaseService(**kwargs)
                elif self.service_type == 'api':
                    self.services[service_name] = ApiService(**kwargs)
                else:
                    raise ValueError(f"Unknown service type: {self.service_type}")
            
            return self.services[service_name]

    # Usage
    db_factory = ServiceFactory(service_type='database')
    api_factory = ServiceFactory(service_type='api')

    # Each factory type is a singleton
    db_factory2 = ServiceFactory(service_type='database')
    print(db_factory is db_factory2)  # True

Configuration-Based Singletons
-------------------------------

Create singletons that depend on configuration:

.. code-block:: python

    from dtPyAppFramework.decorators import singleton
    from dtPyAppFramework.settings import Settings

    @singleton(key_name='cache_type')
    class CacheManager:
        def __init__(self, cache_type='memory'):
            self.cache_type = cache_type
            self.cache = self._initialize_cache()
        
        def _initialize_cache(self):
            settings = Settings()
            
            if self.cache_type == 'redis':
                redis_host = settings.get('cache.redis.host', 'localhost')
                redis_port = settings.get('cache.redis.port', 6379)
                return RedisCache(host=redis_host, port=redis_port)
            elif self.cache_type == 'memory':
                max_size = settings.get('cache.memory.max_size', 1000)
                return MemoryCache(max_size=max_size)
            else:
                raise ValueError(f"Unsupported cache type: {self.cache_type}")

    # Usage - different cache types as separate singletons
    redis_cache = CacheManager(cache_type='redis')
    memory_cache = CacheManager(cache_type='memory')

Resource Management with Singletons
-----------------------------------

.. code-block:: python

    from dtPyAppFramework.decorators import singleton
    import threading
    import logging

    @singleton(key_name='resource_pool_name')
    class ResourcePool:
        def __init__(self, resource_pool_name, max_resources=10):
            self.pool_name = resource_pool_name
            self.max_resources = max_resources
            self.available_resources = []
            self.used_resources = set()
            self.lock = threading.Lock()
            self._initialize_pool()
        
        def _initialize_pool(self):
            """Initialize the resource pool."""
            for i in range(self.max_resources):
                resource = self._create_resource(f"{self.pool_name}_resource_{i}")
                self.available_resources.append(resource)
        
        def acquire_resource(self):
            """Acquire a resource from the pool."""
            with self.lock:
                if not self.available_resources:
                    raise RuntimeError(f"No resources available in pool '{self.pool_name}'")
                
                resource = self.available_resources.pop()
                self.used_resources.add(resource)
                logging.info(f"Resource acquired from pool '{self.pool_name}': {resource}")
                return resource
        
        def release_resource(self, resource):
            """Release a resource back to the pool."""
            with self.lock:
                if resource in self.used_resources:
                    self.used_resources.remove(resource)
                    self.available_resources.append(resource)
                    logging.info(f"Resource released to pool '{self.pool_name}': {resource}")

    # Usage - separate pools for different resource types
    db_pool = ResourcePool(resource_pool_name='database', max_resources=5)
    api_pool = ResourcePool(resource_pool_name='api_clients', max_resources=10)

Testing with Singletons
========================

Singleton Cleanup for Tests
----------------------------

When testing code that uses singletons, you may need to reset singleton state:

.. code-block:: python

    import unittest
    from dtPyAppFramework.decorators import singleton

    @singleton()
    class TestableService:
        def __init__(self):
            self.data = []
            self.initialized = True
        
        def add_data(self, item):
            self.data.append(item)

    class TestSingletonService(unittest.TestCase):
        def setUp(self):
            """Clear singleton instances before each test."""
            # The singleton decorator uses a closure-based instances dict.
            # Access it through __closure__ to clear cached instances.
            if hasattr(TestableService, '__closure__') and TestableService.__closure__:
                for cell in TestableService.__closure__:
                    try:
                        contents = cell.cell_contents
                        if isinstance(contents, dict):
                            contents.clear()
                            break
                    except ValueError:
                        pass
        
        def test_service_functionality(self):
            service = TestableService()
            service.add_data("test_item")
            self.assertEqual(len(service.data), 1)
        
        def test_service_isolation(self):
            # This test should start with a clean service
            service = TestableService()
            self.assertEqual(len(service.data), 0)  # Should be empty due to setUp

Mock-Friendly Singleton Testing
-------------------------------

.. code-block:: python

    import unittest
    from unittest.mock import patch, MagicMock

    class TestWithMockedSingleton(unittest.TestCase):
        @patch('dtPyAppFramework.settings.Settings')
        def test_with_mocked_settings(self, mock_settings_class):
            # Configure mock
            mock_settings_instance = MagicMock()
            mock_settings_instance.get.return_value = "test_value"
            mock_settings_class.return_value = mock_settings_instance
            
            # Test code that uses Settings
            from dtPyAppFramework.settings import Settings
            settings = Settings()
            value = settings.get('test.key')
            
            self.assertEqual(value, "test_value")
            mock_settings_instance.get.assert_called_with('test.key')

Performance Considerations
==========================

Singleton Performance Impact
----------------------------

The singleton decorator adds minimal overhead:

.. code-block:: python

    import time
    from dtPyAppFramework.decorators import singleton

    # Measure singleton access performance
    @singleton()
    class PerformanceTestSingleton:
        def __init__(self):
            self.created_at = time.time()

    # First access - creates instance
    start_time = time.time()
    instance1 = PerformanceTestSingleton()
    creation_time = time.time() - start_time

    # Subsequent accesses - returns existing instance
    start_time = time.time()
    for i in range(10000):
        instance = PerformanceTestSingleton()
    access_time = (time.time() - start_time) / 10000

    print(f"Instance creation time: {creation_time:.6f}s")
    print(f"Average access time: {access_time:.6f}s")

Memory Management
-----------------

Singletons persist for the application lifetime, which can impact memory:

.. code-block:: python

    from dtPyAppFramework.decorators import singleton
    import weakref

    @singleton()
    class MemoryAwareSingleton:
        def __init__(self):
            self.cache = {}
            self.weak_refs = set()
        
        def store_reference(self, obj):
            """Store weak reference to avoid memory leaks."""
            weak_ref = weakref.ref(obj, self._cleanup_reference)
            self.weak_refs.add(weak_ref)
            return weak_ref
        
        def _cleanup_reference(self, weak_ref):
            """Callback for when referenced object is garbage collected."""
            self.weak_refs.discard(weak_ref)
        
        def cleanup_cache(self):
            """Manually clean up cache to free memory."""
            self.cache.clear()
            # Weak references will be cleaned up automatically

Best Practices
==============

1. **Use Sparingly**: Only use singletons when truly needed (shared state, expensive initialization)
2. **Thread Safety**: Consider thread safety implications in multithreaded applications
3. **Testing**: Design singletons to be testable with proper cleanup mechanisms
4. **Configuration-Driven**: Use key-based singletons for configuration-dependent instances
5. **Resource Management**: Implement proper cleanup for singletons that hold resources
6. **Documentation**: Clearly document singleton behavior and lifetime expectations
7. **Avoid Global State**: Minimize global state within singleton instances

Common Anti-Patterns
=====================

Avoid these common mistakes when using singletons:

**Anti-Pattern: Overuse of Singletons**

.. code-block:: python

    # Bad - everything doesn't need to be a singleton
    @singleton()
    class MathUtils:
        def add(self, a, b):
            return a + b

    # Good - use regular class for stateless utilities
    class MathUtils:
        @staticmethod
        def add(a, b):
            return a + b

**Anti-Pattern: Hidden Dependencies**

.. code-block:: python

    # Bad - hidden singleton dependency
    @singleton()
    class ServiceA:
        def __init__(self):
            self.service_b = ServiceB()  # Hidden singleton dependency

    # Good - explicit dependency injection
    @singleton()
    class ServiceA:
        def __init__(self, service_b=None):
            self.service_b = service_b or ServiceB()

**Anti-Pattern: Mutable Global State**

.. code-block:: python

    # Bad - mutable global state
    @singleton()
    class GlobalConfig:
        def __init__(self):
            self.settings = {}
        
        def set_global_setting(self, key, value):
            self.settings[key] = value

    # Good - immutable or controlled state
    @singleton()
    class ConfigManager:
        def __init__(self):
            self._settings = {}
        
        def get_setting(self, key, default=None):
            return self._settings.get(key, default)
        
        def update_settings(self, new_settings):
            # Controlled update with validation
            validated_settings = self._validate_settings(new_settings)
            self._settings.update(validated_settings)

The singleton decorator provides a robust foundation for implementing the singleton pattern in dtPyAppFramework while maintaining flexibility through key-based instances and ensuring thread-safe operation across the entire framework architecture.