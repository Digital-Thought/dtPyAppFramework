from functools import wraps
from typing import Any
import threading
import inspect


def singleton(key_name: str = None) -> Any:
    """
    Decorator to create a singleton class. If a key is passed, it will allow
    for multiple instances of the same singleton to exist.

    :param key_name: The name of the key to monitor for multiple
    instances
    """

    def wrap(class_: Any) -> Any:
        # Dictionary to store instances of the decorated class
        instances = {}
        # Lock for thread-safe instance creation
        _lock = threading.Lock()

        @wraps(class_)
        def get_instance(*args, **kwargs):
            # Get key to monitor
            key_to_monitor_value = "GLOBAL"
            
            if key_name is not None:
                # Check if key is in kwargs
                if key_name in kwargs:
                    key_to_monitor_value = kwargs[key_name]
                else:
                    # Check if key is a positional argument
                    sig = inspect.signature(class_.__init__)
                    param_names = list(sig.parameters.keys())[1:]  # Skip 'self'
                    
                    if key_name in param_names:
                        key_index = param_names.index(key_name)
                        if key_index < len(args):
                            key_to_monitor_value = args[key_index]
            
            # Create a unique key for the class instance
            if key_name is None:
                class_key = f"{class_.__name__}_GLOBAL"
            else:
                class_key = f"{class_.__name__}_{key_name}_{key_to_monitor_value}"

            # Thread-safe instance creation
            if class_key not in instances:
                with _lock:
                    # Double-check pattern
                    if class_key not in instances:
                        instances[class_key] = class_(*args, **kwargs)
            
            return instances[class_key]

        # Preserve class attributes for inheritance
        get_instance.__name__ = class_.__name__
        get_instance.__qualname__ = class_.__qualname__
        get_instance.__module__ = class_.__module__
        get_instance.__doc__ = class_.__doc__
        get_instance.__annotations__ = getattr(class_, '__annotations__', {})

        return get_instance

    return wrap
