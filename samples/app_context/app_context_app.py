"""
AppContext Example - Unified Facade for Framework Components

This example demonstrates the AppContext singleton, which provides a single
convenient access point for all framework components: application metadata,
paths, configuration, settings, secrets, and resources.

Instead of importing and calling individual singletons (Settings, ApplicationPaths,
ResourceManager, etc.), AppContext wraps them all behind a clean interface.

Key Features Demonstrated:
    - Application metadata access (version, names, description)
    - Path resolution (logging, data, temp directories)
    - Configuration file discovery
    - Settings get/set via AppContext
    - Secrets get/set/delete via AppContext
    - Resource path lookup
"""
import sys
import os

sys.path.append(os.path.abspath('../../src'))

from dtPyAppFramework.application import AbstractApp
from dtPyAppFramework.app_context import AppContext

import logging


class AppContextApp(AbstractApp):
    """
    Demonstrates AppContext as a unified facade for framework components.

    AppContext is a singleton that is automatically initialised by the
    framework during application startup. You simply call AppContext()
    to retrieve the pre-initialised instance.
    """

    def define_args(self, arg_parser):
        """Define custom command-line arguments."""
        arg_parser.add_argument(
            '--task',
            type=str,
            default='all',
            choices=['metadata', 'paths', 'config', 'settings', 'secrets', 'all'],
            help='Which AppContext feature to demonstrate (default: all)'
        )

    def main(self, args):
        """
        Main application logic demonstrating all AppContext features.
        """
        # Obtain the AppContext singleton - already initialised by the framework
        ctx = AppContext()

        task = getattr(args, 'task', 'all')

        if task in ('metadata', 'all'):
            self._demo_metadata(ctx)

        if task in ('paths', 'all'):
            self._demo_paths(ctx)

        if task in ('config', 'all'):
            self._demo_config(ctx)

        if task in ('settings', 'all'):
            self._demo_settings(ctx)

        if task in ('secrets', 'all'):
            self._demo_secrets(ctx)

        print('\nAppContext demonstration complete!')

    def _demo_metadata(self, ctx):
        """Demonstrate metadata access via AppContext."""
        print('\n--- Application Metadata ---')
        print(f'  Version:     {ctx.version}')
        print(f'  Full Name:   {ctx.full_name}')
        print(f'  Short Name:  {ctx.short_name}')
        print(f'  Description: {ctx.description}')

    def _demo_paths(self, ctx):
        """Demonstrate path access via AppContext."""
        print('\n--- Application Paths ---')
        print(f'  Logging Path:  {ctx.logging_path}')
        print(f'  App Data Path: {ctx.app_data_path}')
        print(f'  User Data Path:{ctx.usr_data_path}')
        print(f'  Temp Path:     {ctx.tmp_path}')

    def _demo_config(self, ctx):
        """Demonstrate config file path discovery via AppContext."""
        print('\n--- Configuration Files ---')
        for i, path in enumerate(ctx.config_file_paths, 1):
            print(f'  [{i}] {path}')

    def _demo_settings(self, ctx):
        """Demonstrate settings get/set via AppContext."""
        print('\n--- Settings ---')

        # Read a setting from config.yaml
        app_name = ctx.get_setting('app.name', 'not set')
        timeout = ctx.get_setting('app.timeout', 30)
        print(f'  app.name:    {app_name}')
        print(f'  app.timeout: {timeout}')

        # Write and read back a setting
        ctx.set_setting('demo.timestamp', 'hello from AppContext')
        readback = ctx.get_setting('demo.timestamp')
        print(f'  demo.timestamp (set then read): {readback}')

    def _demo_secrets(self, ctx):
        """Demonstrate secrets get/set/delete via AppContext."""
        print('\n--- Secrets ---')

        # Store a secret
        ctx.set_secret('demo_api_key', 'sk-example-12345')
        print('  Stored secret: demo_api_key')

        # Retrieve it
        value = ctx.get_secret('demo_api_key')
        print(f'  Retrieved:     {value}')

        # Delete it
        ctx.delete_secret('demo_api_key')
        after_delete = ctx.get_secret('demo_api_key', 'not found')
        print(f'  After delete:  {after_delete}')

    def exiting(self):
        """Cleanup on shutdown."""
        logging.info('AppContext demo exiting.')


if __name__ == '__main__':
    os.environ['DEV_MODE'] = "True"
    AppContextApp(
        description="AppContext Unified Facade Demo",
        version="1.0",
        short_name="app_context_demo",
        full_name="AppContext Demo Application",
        console_app=True
    ).run()
