==================
File Paths Reference
==================

This document details all file paths created and used by dtPyAppFramework across different operating systems, and explains how environment variables and modes affect path selection.

Overview
========

dtPyAppFramework manages several directory types:

- **Application Data** (``app_data_root_path``): Shared application data accessible to all users
- **User Data** (``usr_data_root_path``): Per-user application data and secrets
- **Temporary Files** (``tmp_root_path``): Temporary working files
- **Log Files** (``log_root_path``): Application log files
- **Keystore** (``keystore_root_path``): Secret storage location (same as user data)

Path Naming
-----------

Paths are constructed using either:

- **app_short_name**: A sanitised version of the application name (spaces replaced with underscores)
- **app_full_name**: The full application name as provided

Windows Paths
=============

Production Mode (Default)
-------------------------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Path Type
     - Location
   * - Application Data
     - ``C:\ProgramData\{app_short_name}``
   * - User Data
     - ``C:\Users\{username}\AppData\Local\{app_short_name}``
   * - Temporary Files
     - ``C:\Users\{username}\AppData\Local\Temp\{app_short_name}``
   * - Log Files
     - ``C:\Users\{username}\AppData\Local\{app_short_name}\logs``
   * - Keystore
     - ``C:\Users\{username}\AppData\Local\{app_short_name}``

Development Mode (DEV_MODE=TRUE)
--------------------------------

All paths collapse to the current working directory:

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Path Type
     - Location
   * - Application Data
     - ``{cwd}\data``
   * - User Data
     - ``{cwd}\data``
   * - Temporary Files
     - ``{cwd}\tmp``
   * - Log Files
     - ``{cwd}\logs``
   * - Keystore
     - ``{cwd}\data``

macOS Paths
===========

Production Mode (Default)
-------------------------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Path Type
     - Location
   * - Application Data
     - ``/Library/Application Support/{app_short_name}``
   * - User Data
     - ``~/Library/Application Support/{app_short_name}``
   * - Temporary Files
     - ``/tmp/{app_short_name}``
   * - Log Files
     - ``~/Library/Logs/{app_short_name}``
   * - Keystore
     - ``~/Library/Application Support/{app_short_name}``

Development Mode (DEV_MODE=TRUE)
--------------------------------

All paths collapse to the current working directory:

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Path Type
     - Location
   * - Application Data
     - ``{cwd}/data``
   * - User Data
     - ``{cwd}/data``
   * - Temporary Files
     - ``{cwd}/tmp``
   * - Log Files
     - ``{cwd}/logs``
   * - Keystore
     - ``{cwd}/data``

Linux Paths
===========

The framework follows the `XDG Base Directory Specification <https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html>`_ on Linux.

Production Mode - Regular User
------------------------------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Path Type
     - Location
   * - Application Data
     - ``$XDG_DATA_HOME/{app_short_name}`` (default: ``~/.local/share/{app_short_name}``)
   * - User Data
     - ``$XDG_DATA_HOME/{app_short_name}`` (default: ``~/.local/share/{app_short_name}``)
   * - Temporary Files
     - ``/tmp/{app_short_name}``
   * - Log Files
     - ``$XDG_STATE_HOME/{app_short_name}/logs`` (default: ``~/.local/state/{app_short_name}/logs``)
   * - Keystore
     - ``$XDG_DATA_HOME/{app_short_name}`` (default: ``~/.local/share/{app_short_name}``)

Production Mode - Root User
---------------------------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Path Type
     - Location
   * - Application Data
     - ``/etc/{app_short_name}``
   * - User Data
     - ``/etc/{app_short_name}``
   * - Temporary Files
     - ``/tmp/{app_short_name}``
   * - Log Files
     - ``/var/log/{app_short_name}``
   * - Keystore
     - ``/etc/{app_short_name}``

Development Mode (DEV_MODE=TRUE)
--------------------------------

All paths collapse to the current working directory:

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Path Type
     - Location
   * - Application Data
     - ``{cwd}/data``
   * - User Data
     - ``{cwd}/data``
   * - Temporary Files
     - ``{cwd}/tmp``
   * - Log Files
     - ``{cwd}/logs``
   * - Keystore
     - ``{cwd}/data``

Container Mode
==============

Container mode (``CONTAINER_MODE=TRUE``) is designed for Docker and other containerised environments where multiple container instances may share a mounted volume.

Container Mode Paths
--------------------

When ``CONTAINER_MODE=TRUE``:

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Path Type
     - Location
   * - Application Data
     - ``/app/data`` (or ``$CONTAINER_DATA_PATH``)
   * - User Data
     - ``/app/data`` (or ``$CONTAINER_DATA_PATH``)
   * - Temporary Files
     - ``/app/data/tmp/{container_id}``
   * - Log Files
     - ``/app/data/logs/{container_id}``
   * - Keystore
     - ``/app/data`` (or ``$CONTAINER_DATA_PATH``)

The ``{container_id}`` is derived from:

1. ``HOSTNAME`` environment variable (if set)
2. First 12 characters of ``/proc/self/cgroup`` container ID
3. Falls back to ``unknown`` if neither is available

Environment Variables
=====================

Mode Selection
--------------

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Variable
     - Values
     - Effect
   * - ``DEV_MODE``
     - ``TRUE``
     - Enables development mode; all paths relative to current working directory
   * - ``CONTAINER_MODE``
     - ``TRUE``
     - Enables container mode; paths designed for containerised environments

Container Configuration
-----------------------

.. list-table::
   :header-rows: 1
   :widths: 25 25 50

   * - Variable
     - Default
     - Effect
   * - ``CONTAINER_DATA_PATH``
     - ``/app/data``
     - Base path for all container data
   * - ``HOSTNAME``
     - (auto-detected)
     - Used to create container-specific subdirectories for logs and temp files

Keystore Configuration
----------------------

.. list-table::
   :header-rows: 1
   :widths: 25 25 50

   * - Variable
     - Default
     - Effect
   * - ``ALL_USER_KS``
     - ``FALSE``
     - When ``TRUE``, creates the all-users keystore (``App_Local_Store``) in addition to the per-user keystore
   * - ``KEYSTORE_PASSWORD``
     - (none)
     - Password for keystore encryption; in container mode, used directly without system fingerprint

XDG Variables (Linux Only)
--------------------------

.. list-table::
   :header-rows: 1
   :widths: 25 35 40

   * - Variable
     - Default
     - Affects
   * - ``XDG_DATA_HOME``
     - ``~/.local/share``
     - Application data and user data paths
   * - ``XDG_STATE_HOME``
     - ``~/.local/state``
     - Log file paths

Keystore Locations
==================

The framework creates two types of keystores:

User Local Store
----------------

**Always created.** Stores per-user secrets.

- **Location**: Same as ``usr_data_root_path``
- **File**: ``keystore.enc``

App Local Store (All-Users)
---------------------------

**Only created when** ``ALL_USER_KS=TRUE``.

Stores secrets accessible to all users of the application. Requires write access to the application data directory.

- **Location**: Same as ``app_data_root_path``
- **File**: ``keystore.enc``

Graceful Failure Handling
=========================

As of version 4.2.0, the framework handles directory creation failures gracefully:

- If a directory cannot be created (e.g., due to permissions), a warning is logged
- The application continues with reduced functionality
- Use ``ApplicationPaths().is_path_available('path_name')`` to check availability

Available path names for checking:

- ``app_data``
- ``usr_data``
- ``tmp``
- ``logging``

Example::

    from dtPyAppFramework.paths import ApplicationPaths

    paths = ApplicationPaths()

    if paths.is_path_available('logging'):
        # Log file operations are safe
        pass
    else:
        # Log directory unavailable, use alternative
        pass

Path Aliases
============

When referencing paths in configuration files, the following aliases are available:

.. list-table::
   :header-rows: 1
   :widths: 15 85

   * - Alias
     - Expands To
   * - ``<APP>``
     - ``app_data_root_path``
   * - ``<USR>``
     - ``usr_data_root_path``
   * - ``<TMP>``
     - ``tmp_root_path``

Example configuration::

    [database]
    path = <USR>/database.db

    [cache]
    path = <TMP>/cache

Quick Reference Summary
=======================

Windows
-------

::

    Production:
      App Data:  C:\ProgramData\{app}
      User Data: C:\Users\{user}\AppData\Local\{app}
      Temp:      C:\Users\{user}\AppData\Local\Temp\{app}
      Logs:      C:\Users\{user}\AppData\Local\{app}\logs

    DEV_MODE=TRUE:
      All paths: {cwd}\data, {cwd}\tmp, {cwd}\logs

macOS
-----

::

    Production:
      App Data:  /Library/Application Support/{app}
      User Data: ~/Library/Application Support/{app}
      Temp:      /tmp/{app}
      Logs:      ~/Library/Logs/{app}

    DEV_MODE=TRUE:
      All paths: {cwd}/data, {cwd}/tmp, {cwd}/logs

Linux (Regular User)
--------------------

::

    Production:
      App Data:  ~/.local/share/{app}
      User Data: ~/.local/share/{app}
      Temp:      /tmp/{app}
      Logs:      ~/.local/state/{app}/logs

    DEV_MODE=TRUE:
      All paths: {cwd}/data, {cwd}/tmp, {cwd}/logs

Linux (Root)
------------

::

    Production:
      App Data:  /etc/{app}
      User Data: /etc/{app}
      Temp:      /tmp/{app}
      Logs:      /var/log/{app}

Container Mode
--------------

::

    CONTAINER_MODE=TRUE:
      App Data:  /app/data (or $CONTAINER_DATA_PATH)
      User Data: /app/data (or $CONTAINER_DATA_PATH)
      Temp:      /app/data/tmp/{container_id}
      Logs:      /app/data/logs/{container_id}
