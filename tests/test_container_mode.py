"""
Tests for container mode functionality.
"""
import os
import sys
import tempfile
import pytest
from unittest.mock import patch

# Add src to path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


class TestContainerMode:
    """Test container mode functionality."""
    
    def setup_method(self, method):
        """Clean up environment before each test."""
        os.environ.pop('CONTAINER_MODE', None)
        os.environ.pop('DEV_MODE', None)
    
    def teardown_method(self, method):
        """Clean up environment after each test."""
        os.environ.pop('CONTAINER_MODE', None)
        os.environ.pop('DEV_MODE', None)

    def test_container_mode_environment_variable(self):
        """Test that CONTAINER_MODE environment variable is detected."""
        os.environ['CONTAINER_MODE'] = 'true'
        
        with patch('dtPyAppFramework.paths.os.getcwd', return_value='/test/workdir'):
            from dtPyAppFramework.paths import ApplicationPaths
            
            # Force new singleton instance
            if hasattr(ApplicationPaths, '__wrapped__'):
                if hasattr(ApplicationPaths.__wrapped__, 'instances'):
                    ApplicationPaths.__wrapped__.instances.clear()
            
            app_paths = ApplicationPaths('test-app')
            
            assert '/test/workdir/logs' in app_paths.logging_root_path
            assert '/test/workdir/data' in app_paths.app_data_root_path
            assert '/test/workdir/data' in app_paths.usr_data_root_path
            assert '/test/workdir/temp' in app_paths.tmp_root_path

    def test_container_mode_paths(self):
        """Test container mode creates correct directory structure."""
        with tempfile.TemporaryDirectory() as temp_dir:
            original_cwd = os.getcwd()
            try:
                os.chdir(temp_dir)
                os.environ['CONTAINER_MODE'] = 'True'
                
                # Import after setting environment
                import importlib
                import dtPyAppFramework.paths
                importlib.reload(dtPyAppFramework.paths)
                from dtPyAppFramework.paths import ApplicationPaths
                
                app_paths = ApplicationPaths('test-container-app')
                
                # Verify all paths are in working directory
                assert temp_dir in app_paths.logging_root_path
                assert temp_dir in app_paths.app_data_root_path
                assert temp_dir in app_paths.usr_data_root_path
                assert temp_dir in app_paths.tmp_root_path
                
                # Verify specific directory names
                assert app_paths.logging_root_path.endswith('logs')
                assert app_paths.app_data_root_path.endswith('data')
                assert app_paths.usr_data_root_path.endswith('data')
                assert app_paths.tmp_root_path.endswith('temp')
                
                # Verify app and user data point to same directory in container mode
                assert app_paths.app_data_root_path == app_paths.usr_data_root_path
                
            finally:
                os.chdir(original_cwd)

    def test_container_mode_settings_single_config(self):
        """Test container mode uses single config directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            original_cwd = os.getcwd()
            try:
                os.chdir(temp_dir)
                os.environ['CONTAINER_MODE'] = 'True'
                
                # Create config directory and file
                config_dir = os.path.join(temp_dir, 'config')
                os.makedirs(config_dir, exist_ok=True)
                config_file = os.path.join(config_dir, 'config.yaml')
                with open(config_file, 'w') as f:
                    f.write('test:\n  value: container_config\n')
                
                # Import after setting up environment
                import importlib
                import dtPyAppFramework.settings
                importlib.reload(dtPyAppFramework.settings)
                from dtPyAppFramework.settings import Settings
                
                settings = Settings()
                settings.init_settings_readers()
                
                # Container mode should have only one settings reader
                assert len(settings.settings_readers) == 1
                
                # Verify it reads from the config directory
                reader = settings.settings_readers[0]
                assert temp_dir in reader.settings_file
                assert 'config' in reader.settings_file
                
            finally:
                os.chdir(original_cwd)

    def test_standard_mode_vs_container_mode(self):
        """Test difference between standard and container modes."""
        with tempfile.TemporaryDirectory() as temp_dir:
            original_cwd = os.getcwd()
            try:
                os.chdir(temp_dir)
                
                # Test standard mode first
                os.environ.pop('CONTAINER_MODE', None)
                import importlib
                import dtPyAppFramework.settings
                importlib.reload(dtPyAppFramework.settings)
                from dtPyAppFramework.settings import Settings
                
                standard_settings = Settings()
                standard_settings.init_settings_readers()
                standard_count = len(standard_settings.settings_readers)
                
                # Test container mode
                os.environ['CONTAINER_MODE'] = 'True'
                importlib.reload(dtPyAppFramework.settings)
                from dtPyAppFramework.settings import Settings as ContainerSettings
                
                container_settings = ContainerSettings()
                container_settings.init_settings_readers()
                container_count = len(container_settings.settings_readers)
                
                # Standard mode should have more settings readers than container mode
                assert standard_count > container_count
                assert container_count == 1
                assert standard_count >= 3  # working dir + app data + user data
                
            finally:
                os.chdir(original_cwd)

    def test_container_mode_raw_settings(self):
        """Test container mode raw settings behavior."""
        with tempfile.TemporaryDirectory() as temp_dir:
            original_cwd = os.getcwd()
            try:
                os.chdir(temp_dir)
                os.environ['CONTAINER_MODE'] = 'True'
                
                # Create config directory to make it writable
                config_dir = os.path.join(temp_dir, 'config')
                os.makedirs(config_dir, exist_ok=True)
                
                import importlib
                import dtPyAppFramework.settings
                importlib.reload(dtPyAppFramework.settings)
                from dtPyAppFramework.settings import Settings
                
                settings = Settings()
                raw_settings = settings.get_raw_settings()
                
                # Should have all expected keys
                assert 'app' in raw_settings
                assert 'all_user' in raw_settings
                assert 'current_user' in raw_settings
                
                # Only 'app' should be writable in container mode
                assert raw_settings['app']['read_only'] == False
                assert raw_settings['all_user']['read_only'] == True
                assert raw_settings['current_user']['read_only'] == True
                
                # Non-app settings should have container mode message
                assert 'Not available in container mode' in raw_settings['all_user']['raw_data']
                assert 'Not available in container mode' in raw_settings['current_user']['raw_data']
                
            finally:
                os.chdir(original_cwd)

    def test_abstract_app_container_argument(self):
        """Test that AbstractApp correctly handles container argument."""
        with patch('sys.argv', ['test_app.py', '--container']):
            with patch('dtPyAppFramework.application.ProcessManager'):
                from dtPyAppFramework.application import AbstractApp
                
                class TestApp(AbstractApp):
                    def define_args(self, arg_parser):
                        pass
                    def main(self, args):
                        pass
                    def exiting(self):
                        pass
                
                app = TestApp("Test", "1.0", "test", "Test App")
                
                # Mock argparser to simulate --container flag
                with patch('argparse.ArgumentParser') as mock_parser:
                    mock_args = type('Args', (), {
                        'container': True,
                        'working_dir': None,
                        'single_folder': False,
                        'service': False,
                        'init': False,
                        'add_secret': False
                    })()
                    
                    mock_parser_instance = mock_parser.return_value
                    mock_parser_instance.parse_known_args.return_value = (mock_args, [])
                    
                    # This should set CONTAINER_MODE environment variable
                    app._AbstractApp__define_args(mock_parser_instance)
                    
                    assert os.environ.get('CONTAINER_MODE') == 'True'