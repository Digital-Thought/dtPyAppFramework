"""
Metadata Auto-Discovery Example

This example demonstrates the framework's ability to auto-discover application
metadata from text files instead of requiring explicit constructor arguments.

When you create an application that inherits from AbstractApp, you can omit
the version, short_name, full_name, and description constructor arguments.
The framework will automatically look for corresponding text files in your
application's top-level package directory:

    your_app_package/
        __init__.py
        app.py              <-- your application class
        _version.txt         --> version
        _short_name.txt      --> short_name
        _full_name.txt       --> full_name
        _description.txt     --> description

This pattern mirrors how the dtPyAppFramework library itself stores its own
metadata and is the recommended approach for applications that are structured
as installable Python packages.

Key Features Demonstrated:
    - Zero-argument metadata: no version/name/description in the constructor
    - Text file discovery from the subclass's package directory
    - Verification that AppContext receives the discovered metadata
    - Comparison with the explicit-argument approach
"""
import sys
import os

sys.path.append(os.path.abspath('../../src'))

from dtPyAppFramework.application import AbstractApp
from dtPyAppFramework.app_context import AppContext

import logging


class MetadataDiscoveryApp(AbstractApp):
    """
    An application that relies entirely on auto-discovered metadata.

    Notice: the constructor below passes NO metadata arguments.
    The framework reads them from _version.txt, _short_name.txt,
    _full_name.txt, and _description.txt in this package directory.
    """

    def define_args(self, arg_parser):
        """Define custom command-line arguments."""
        pass

    def main(self, args):
        """
        Main application logic.

        Demonstrates that metadata was successfully auto-discovered
        from text files rather than being provided as constructor arguments.
        """
        print('=== Metadata Auto-Discovery Demo ===\n')

        # -- Show the discovered metadata from the AbstractApp --
        print('Metadata discovered by AbstractApp:')
        print(f'  version:     {self.version}')
        print(f'  short_name:  {self.app_spec["short_name"]}')
        print(f'  full_name:   {self.app_spec["full_name"]}')
        print(f'  description: {self.description}')

        # -- Show that AppContext also received the same metadata --
        ctx = AppContext()
        print('\nSame metadata via AppContext:')
        print(f'  ctx.version:     {ctx.version}')
        print(f'  ctx.short_name:  {ctx.short_name}')
        print(f'  ctx.full_name:   {ctx.full_name}')
        print(f'  ctx.description: {ctx.description}')

        # -- Explain the file locations --
        package_dir = os.path.dirname(os.path.abspath(__file__))
        print(f'\nMetadata files loaded from: {package_dir}')
        for filename in ['_version.txt', '_short_name.txt', '_full_name.txt', '_description.txt']:
            filepath = os.path.join(package_dir, filename)
            exists = os.path.isfile(filepath)
            if exists:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                print(f'  {filename}: "{content}"')
            else:
                print(f'  {filename}: NOT FOUND')

        print('\nNo metadata arguments were passed to the constructor!')
        print('All values were discovered automatically from text files.')

    def exiting(self):
        """Cleanup on shutdown."""
        logging.info('Metadata discovery demo exiting.')


if __name__ == '__main__':
    os.environ['DEV_MODE'] = "True"

    # Note: NO version, short_name, full_name, or description arguments!
    # The framework discovers them from text files in this package directory.
    MetadataDiscoveryApp(
        console_app=True
    ).run()
