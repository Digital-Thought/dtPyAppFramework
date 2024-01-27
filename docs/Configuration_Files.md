# Settings and Configuration

The **`Settings`** class manages application settings. It provides methods to define, get, and set settings. Settings can be read from various sources, including configuration files and environment variables.

## Configuration File Locations

The library searches for the existence of the `config.yaml` file in the following locations:

1. **Root of the Application:**
    - Path: `os.getcwd()`
    - Priority: Lowest

2. **All Users Configuration:**
    - Path: `{CommonApplicationData}/{simple_name}/config.yaml` (e.g., `C:/ProgramData/{simple_name}/config.yaml` on Windows)
    - Priority: Medium

3. **User-Specific Configuration:**
    - Path: `{UserApplicationData}/{simple_name}/config.yaml` (e.g., `C:/Users/{username}/AppData/Roaming/{simple_name}/config.yaml` on Windows)
    - Priority: Highest

## Configuration File Format
The configuration file (`config.yaml`) follows the YAML format. Users can define application-specific settings and configurations in this file.

Example `config.yaml`:

```yaml
settings:
  key1: value1
  key2:
    nested_key: nested_value
```
## Accessing Settings
To access the settings, you can use the Settings class provided by the library. It automatically loads settings from the configuration file and allows you to retrieve values.
Example usage:

```python
from dtPyAppFramework.settings import Settings

# Create a singleton instance of the Settings class
settings = Settings()

# Retrieve settings
value = settings.get('settings.key1', 'default_value')
nested_value = settings.get('settings.key2.nested_key', 'default_nested_value')
```

## Defining Settings Readers
The library defines settings readers, each with a specific priority. These settings readers are responsible for loading settings from different locations. By default, the settings readers have the following priorities:

1. Root of the Application (Priority: 300)
2. All Users Configuration (Priority: 200)
3. User-Specific Configuration (Priority: 100)

You can customize the priority by adding or modifying settings readers.

```python
from dtPyAppFramework.settings import Settings
from dtPyAppFramework.settings.settings_reader import SettingsReader

# Create a singleton instance of the Settings class
settings = Settings()

# Define custom settings readers
settings.settings_readers.append(SettingsReader('/path/to/custom/config', priority=250))

# The settings will now be read from the custom configuration folder with a priority of 250
```

## Setting Values

To set a new value or change the existing value of a setting, you can use the `set` method provided by the `Settings` class.

```python
from dtPyAppFramework.settings import Settings

# Create a singleton instance of the Settings class
settings = Settings()

# Set a new value
settings.set('settings.new_key', 'new_value')

# The new value will be saved to the application keystore
```
Note: Setting a value using the set method will override any existing values in the application keystore.

## Retrieving Persisted Values

The persisted values can be retrieved using the get method as usual. The Settings class automatically checks the application keystore for persisted values before looking into the configuration files.

```python
from dtPyAppFramework.settings import Settings

# Create a singleton instance of the Settings class
settings = Settings()

# Retrieve the persisted value
persisted_value = settings.get('settings.new_key', 'default_value')

```

This ensures that the most recent values set during the application runtime are used, even after a restart.