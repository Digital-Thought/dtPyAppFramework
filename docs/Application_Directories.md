# Application Directories

The `dtPyAppFramework` automatically prepares a set of application directories or paths upon initialisation. These directories serve different purposes and are designed to enhance the organisation and functionality of the application.

## User Data Root Path

The User Data Root Path is determined based on the operating environment:

- **Windows:**
  - **Path:** `%APPDATA%/{app_short_name}`
  - **Purpose:** Storing user-specific application data.

- **Darwin (MacOS):**
  - **Path:** `~/Library/Application Support/{app_short_name}`
  - **Purpose:** Storing user-specific application data.

- **Linux:**
  - **Path:** `~/.config/{app_short_name}`
  - **Purpose:** Storing user-specific application data.

- **Development Mode:**
  - **Path:** `{os.getcwd()}/data/usr`
  - **Purpose:** Storing user-specific application data.
  - **Note:** This mode is activated when the `DEV_MODE` environment variable is set.

## App Data Root Path

The App Data Root Path is determined based on the operating environment:

- **Development Mode:**
  - **Path:** `{os.getcwd()}/data/app`
  - **Purpose:** Storing application data accessible to all users.
  - **Note:** This mode is activated when the `DEV_MODE` environment variable is set.

- **Windows:**
  - **Path:** `%ALLUSERSPROFILE%/{app_short_name}`
  - **Purpose:** Storing application data accessible to all users.

- **Darwin (MacOS):**
  - **Path:** `/Library/Application Support/{app_short_name}`
  - **Purpose:** Storing application data accessible to all users.

- **Linux:**
  - **Path:** `/etc/{app_short_name}`
  - **Purpose:** Storing application data accessible to all users.

## Log Path

The Log Path is determined based on the operating environment:

- **Windows:**
  - **Path:** `%LOCALAPPDATA%/{app_short_name}/logs`
  - **Purpose:** Storing log files associated with the application.

- **Darwin (MacOS):**
  - **Path:** `~/Library/Logs/{app_short_name}`
  - **Purpose:** Storing log files associated with the application.

- **Linux:**
  - **Path:** `/var/log/{app_short_name}`
  - **Purpose:** Storing log files associated with the application.

- **Development Mode:**
  - **Path:** `{os.getcwd()}/logs`
  - **Purpose:** Storing log files associated with the application.
  - **Note:** This mode is activated when the `DEV_MODE` environment variable is set.

## TEMP Path

The TEMP Path is determined based on the operating environment:

- **Windows:**
  - **Path:** `%TEMP%/{app_short_name}`
  - **Purpose:** Intended for temporary file storage within the application.

- **Darwin (MacOS):**
  - **Path:** `{os.environ.get("TMPDIR")}{app_short_name}`
  - **Purpose:** Intended for temporary file storage within the application.

- **Linux:**
  - **Path:** `/tmp/{app_short_name}`
  - **Purpose:** Intended for temporary file storage within the application.

- **Development Mode:**
  - **Path:** `{os.getcwd()}/temp`
  - **Purpose:** Intended for temporary file storage within the application.
  - **Note:** This mode is activated when the `DEV_MODE` environment variable is set.


## Accessing Application Paths
The Application Paths can be conveniently accessed using the Singleton **`ApplicationPaths`** class from anywhere within the application. The **`ApplicationPaths`** class provides methods to retrieve the paths for different purposes:

```python
from dtPyAppFramework.paths import ApplicationPaths

# Access the Singleton ApplicationPaths instance
app_paths = ApplicationPaths()

# Retrieve the paths
user_data_path = app_paths.usr_data_root_path
app_data_path = app_paths.app_data_root_path
log_path = app_paths.logging_root_path
temp_path = app_paths.tmp_root_path

# Example usage
print(f"User Data Path: {user_data_path}")
print(f"App Data Path: {app_data_path}")
print(f"Log Path: {log_path}")
print(f"Temp Path: {temp_path}")

```