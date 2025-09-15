#!/usr/bin/env python3
"""
Container Mode Sample Application

This sample demonstrates how to use dtPyAppFramework in container environments
(Docker, Kubernetes, etc.) with simplified directory structure.

Prerequisites:
- Install dependencies from main project: pip install -r ../../requirements.txt
- The main requirements.txt includes all needed dependencies:
  PyYAML, psutil, cryptography, colorlog, boto3, azure-identity, etc.

Key Features Demonstrated:
- Container mode with --container flag
- Simplified directory structure in working directory
- Single configuration layer
- Secrets management in containers
- Resource management
- Logging in container environments
"""

import sys
import os
import time
import json

# Add framework to path (adjust path as needed for your setup)
sys.path.append(os.path.abspath('../../src'))

from dtPyAppFramework.application import AbstractApp
from dtPyAppFramework.settings import Settings
from dtPyAppFramework.resources import ResourceManager
from dtPyAppFramework.paths import ApplicationPaths
import logging


class ContainerApp(AbstractApp):
    """Sample application demonstrating container mode functionality."""

    def define_args(self, arg_parser):
        """Define custom command-line arguments for the application."""
        arg_parser.add_argument(
            '--demo-mode', 
            action='store_true', 
            help='Run in demonstration mode with extra output'
        )
        arg_parser.add_argument(
            '--task', 
            choices=['config', 'secrets', 'resources', 'all'], 
            default='all',
            help='Which functionality to demonstrate'
        )

    def main(self, args):
        """Main application logic."""
        logging.info("=== Container Mode Sample Application ===")
        
        # Show container mode status
        container_mode = os.environ.get('CONTAINER_MODE', 'False')
        logging.info(f"Container Mode: {container_mode}")
        
        if args.demo_mode:
            self._show_directory_structure()
        
        # Run requested demonstrations
        if args.task in ['config', 'all']:
            self._demonstrate_configuration()
        
        if args.task in ['secrets', 'all']:
            self._demonstrate_secrets()
        
        if args.task in ['resources', 'all']:
            self._demonstrate_resources()
        
        if args.demo_mode:
            self._show_final_status()

        v = Settings().get('test_vale', 'not_set')
        print(v)
        Settings().set('test_vale', 'I have set this value')

    def _show_directory_structure(self):
        """Display the current directory structure."""
        logging.info("=== Directory Structure ===")
        
        # Get application paths - use existing singleton instance
        from dtPyAppFramework.process import ProcessManager
        app_paths = ApplicationPaths()
        
        paths_info = {
            'Working Directory': os.getcwd(),
            'Logging Path': app_paths.logging_root_path,
            'App Data Path': app_paths.app_data_root_path,
            'User Data Path': app_paths.usr_data_root_path,
            'Temp Path': app_paths.tmp_root_path,
        }
        
        for name, path in paths_info.items():
            logging.info(f"  {name}: {path}")
        
        # Show actual directory contents
        logging.info("\nDirectory Contents:")
        for root, dirs, files in os.walk('.'):
            level = root.replace('.', '').count(os.sep)
            indent = ' ' * 2 * level
            logging.info(f"{indent}{os.path.basename(root)}/")
            subindent = ' ' * 2 * (level + 1)
            for file in files[:5]:  # Limit to first 5 files
                logging.info(f"{subindent}{file}")
            if len(files) > 5:
                logging.info(f"{subindent}... and {len(files) - 5} more files")

    def _demonstrate_configuration(self):
        """Demonstrate configuration management in container mode."""
        logging.info("=== Configuration Management ===")
        
        settings = Settings()
        
        # Show number of config readers (should be 1 in container mode)
        logging.info(f"Number of configuration layers: {len(settings.settings_readers)}")
        
        # Show configuration paths
        for i, reader in enumerate(settings.settings_readers):
            logging.info(f"  Config Reader {i+1}: {reader.settings_file}")
        
        # Try to read some configuration values
        app_name = settings.get('app.name', 'Container Sample App')
        debug_mode = settings.get('app.debug', False)
        database_host = settings.get('database.host', 'localhost')
        
        logging.info(f"App Name: {app_name}")
        logging.info(f"Debug Mode: {debug_mode}")
        logging.info(f"Database Host: {database_host}")
        
        # Set a runtime configuration value
        settings['runtime.start_time'] = time.time()
        settings['runtime.container_mode'] = os.environ.get('CONTAINER_MODE', 'False')
        
        logging.info("Runtime configuration values set successfully")

    def _demonstrate_secrets(self):
        """Demonstrate secrets management in container mode."""
        logging.info("=== Secrets Management ===")
        
        settings = Settings()
        
        try:
            # Show available secret stores
            if hasattr(settings, 'secret_manager') and settings.secret_manager:
                stores_info = settings.secret_manager.get_local_stores_index()
                logging.info(f"Available secret stores: {stores_info}")
                
                # Set a sample secret
                settings.secret_manager.set_secret('sample_key', 'sample_secret_value')
                logging.info("Sample secret stored successfully")
                
                # Retrieve the secret
                retrieved_secret = settings.secret_manager.get_secret('sample_key')
                logging.info(f"Retrieved secret: {'*' * len(str(retrieved_secret)) if retrieved_secret else 'None'}")
                
                # Try to read environment-based secrets
                api_key = settings.get('SEC/api_key', 'default-api-key')
                logging.info(f"API Key (from secrets): {'*' * len(api_key) if api_key else 'None'}")
            else:
                logging.warning("Secret manager not available")
                
        except Exception as e:
            error_msg = str(e) if str(e) else f"{type(e).__name__}: {repr(e)}"
            logging.error(f"Error in secrets demonstration: {error_msg}")
            import traceback
            logging.debug(f"Full traceback: {traceback.format_exc()}")

    def _demonstrate_resources(self):
        """Demonstrate resource management in container mode."""
        logging.info("=== Resource Management ===")
        
        try:
            # Create a sample resource file
            resource_content = {
                'version': '1.0',
                'container_mode': os.environ.get('CONTAINER_MODE', 'False'),
                'timestamp': time.time(),
                'sample_data': [1, 2, 3, 4, 5]
            }
            
            # Get resource manager
            resource_manager = ResourceManager()
            
            # Store resource
            resource_name = 'sample_resource.json'
            resource_manager.save_resource(resource_name, json.dumps(resource_content, indent=2))
            logging.info(f"Sample resource '{resource_name}' saved successfully")
            
            # Load resource
            loaded_resource = resource_manager.load_resource(resource_name)
            if loaded_resource:
                loaded_data = json.loads(loaded_resource)
                logging.info(f"Resource loaded - version: {loaded_data.get('version')}")
                logging.info(f"Resource timestamp: {loaded_data.get('timestamp')}")
            else:
                logging.warning("Failed to load resource")
                
        except Exception as e:
            logging.error(f"Error in resource demonstration: {e}")

    def _show_final_status(self):
        """Show final application status."""
        logging.info("=== Final Status ===")
        
        # Show memory usage if available
        try:
            import psutil
            process = psutil.Process()
            memory_info = process.memory_info()
            logging.info(f"Memory Usage: {memory_info.rss / 1024 / 1024:.2f} MB")
        except ImportError:
            logging.info("Memory information not available (psutil not installed)")
        
        # Show uptime - handle potential multiprocessing issues gracefully
        try:
            settings = Settings()
            start_time = settings.get('runtime.start_time')
            if start_time:
                uptime = time.time() - start_time
                logging.info(f"Application uptime: {uptime:.2f} seconds")
            else:
                logging.info("Start time not available")
        except Exception as e:
            logging.warning(f"Could not retrieve start time (secrets manager may be unavailable): {e}")
        
        logging.info("Container mode demonstration completed successfully!")

    def exiting(self):
        """Cleanup when application exits."""
        logging.info("=== Application Cleanup ===")
        logging.info("Performing cleanup operations...")
        
        # Add any cleanup logic here
        # In container mode, this might include:
        # - Flushing logs
        # - Closing database connections
        # - Saving final state
        
        logging.info("Cleanup completed. Goodbye!")


def main():
    """Main entry point for the application."""
    
    # You can set container mode in several ways:
    
    # Method 1: Environment variable (recommended for containers)
    # os.environ['CONTAINER_MODE'] = 'True'
    
    # Method 2: Command line argument (will be processed automatically)
    # Run with: python container_app.py --container
    os.environ['CONTAINER_MODE'] = 'True'
    # Method 3: Hybrid approach - check for container environment
    if os.path.exists('/.dockerenv') or os.environ.get('KUBERNETES_SERVICE_HOST'):
        # Automatically enable container mode if running in Docker/Kubernetes
        os.environ['CONTAINER_MODE'] = 'True'
        print("Auto-detected container environment - enabling container mode")
    
    # Create and run the application
    app = ContainerApp(
        description="Container Mode Sample Application",
        version="1.0.0",
        short_name="container-sample",
        full_name="dtPyAppFramework Container Mode Sample",
        console_app=True  # Set to False for service mode
    )
    
    app.run()


if __name__ == "__main__":
    main()