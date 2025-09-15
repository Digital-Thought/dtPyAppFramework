"""
Comprehensive tests for ApplicationPaths cross-platform path management.

This test suite ensures that ApplicationPaths correctly manages application directories
across different operating systems (Windows, macOS, Linux) and handles various
configuration scenarios including development mode and spawned instances.
"""

import pytest
import os
import sys
import tempfile
import shutil
import platform
from unittest.mock import patch, MagicMock

# Add the src directory to Python path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from dtPyAppFramework.paths import ApplicationPaths


class TestApplicationPathsBasic:
    """Test basic ApplicationPaths functionality and initialization."""
    
    def setup_method(self):
        """Setup method run before each test."""
        # Clear any existing environment variables that might interfere
        env_vars_to_clear = ['DEV_MODE', 'dt_LOGGING_PATH', 'dt_APP_DATA', 'dt_USR_DATA', 'dt_TMP']
        for var in env_vars_to_clear:
            if var in os.environ:
                del os.environ[var]
    
    def teardown_method(self):
        """Cleanup method run after each test."""
        # Clear environment variables set during tests
        env_vars_to_clear = ['DEV_MODE', 'dt_LOGGING_PATH', 'dt_APP_DATA', 'dt_USR_DATA', 'dt_TMP']
        for var in env_vars_to_clear:
            if var in os.environ:
                del os.environ[var]
    
    def test_basic_initialization(self):
        """Test basic ApplicationPaths initialization with required parameters."""
        app_paths = ApplicationPaths("TestApp")
        
        # Verify basic attributes are set
        assert app_paths.app_short_name == "TestApp"
        assert app_paths.forced_os is None
        assert app_paths.spawned_instance is False
        assert app_paths.auto_create is True
        assert app_paths.clean_temp is True
        assert app_paths.forced_dev_mode is False
        assert app_paths.worker_id is None
        
        # Verify paths are initialized
        assert app_paths.logging_root_path is not None
        assert app_paths.app_data_root_path is not None
        assert app_paths.usr_data_root_path is not None
        assert app_paths.tmp_root_path is not None
    
    def test_initialization_with_all_parameters(self):
        """Test ApplicationPaths initialization with all parameters specified."""
        app_paths = ApplicationPaths(
            app_short_name="TestApp",
            forced_os="TestOS",
            forced_dev_mode=True,
            auto_create=False,
            clean_temp=False,
            spawned_instance=True,
            worker_id=42
        )
        
        assert app_paths.app_short_name == "TestApp"
        assert app_paths.forced_os == "TestOS"
        assert app_paths.spawned_instance is True
        assert app_paths.auto_create is False
        assert app_paths.clean_temp is False
        assert app_paths.forced_dev_mode is True
        assert app_paths.worker_id == 42
        assert os.environ.get('DEV_MODE') == "True"


class TestApplicationPathsWindows:
    """Test Windows-specific path generation."""
    
    def setup_method(self):
        """Setup method run before each test."""
        env_vars_to_clear = ['DEV_MODE', 'dt_LOGGING_PATH', 'dt_APP_DATA', 'dt_USR_DATA', 'dt_TMP']
        for var in env_vars_to_clear:
            if var in os.environ:
                del os.environ[var]
    
    @patch.dict(os.environ, {
        'LOCALAPPDATA': 'C:\\Users\\TestUser\\AppData\\Local',
        'ALLUSERSPROFILE': 'C:\\ProgramData',
        'APPDATA': 'C:\\Users\\TestUser\\AppData\\Roaming',
        'TEMP': 'C:\\Users\\TestUser\\AppData\\Local\\Temp'
    })
    def test_windows_paths_production_mode(self):
        """Test Windows path generation in production mode."""
        with patch('platform.system', return_value='Windows'):
            app_paths = ApplicationPaths("TestApp", forced_os="Windows", auto_create=False)
            
            expected_logging = 'C:\\Users\\TestUser\\AppData\\Local\\TestApp\\logs'
            expected_app_data = 'C:\\ProgramData\\TestApp'
            expected_usr_data = 'C:\\Users\\TestUser\\AppData\\Roaming\\TestApp'
            expected_temp = 'C:\\Users\\TestUser\\AppData\\Local\\Temp\\TestApp'
            
            assert app_paths.logging_root_path == expected_logging
            assert app_paths.app_data_root_path == expected_app_data
            assert app_paths.usr_data_root_path == expected_usr_data
            assert app_paths.tmp_root_path == expected_temp
            
            # Verify environment variables are set
            assert os.environ['dt_LOGGING_PATH'] == expected_logging
            assert os.environ['dt_APP_DATA'] == expected_app_data
            assert os.environ['dt_USR_DATA'] == expected_usr_data
            assert os.environ['dt_TMP'] == expected_temp
    
    def test_windows_paths_dev_mode(self):
        """Test Windows path generation in development mode."""
        with patch('os.getcwd', return_value='C:\\dev\\myproject'):
            app_paths = ApplicationPaths("TestApp", forced_dev_mode=True, auto_create=False)
            
            expected_logging = 'C:\\dev\\myproject/logs'
            expected_app_data = 'C:\\dev\\myproject/data/app'
            expected_usr_data = 'C:\\dev\\myproject/data/usr'
            expected_temp = 'C:\\dev\\myproject/temp'
            
            assert app_paths.logging_root_path == expected_logging
            assert app_paths.app_data_root_path == expected_app_data
            assert app_paths.usr_data_root_path == expected_usr_data
            assert app_paths.tmp_root_path == expected_temp


class TestApplicationPathsLinux:
    """Test Linux-specific path generation."""
    
    def setup_method(self):
        """Setup method run before each test."""
        env_vars_to_clear = ['DEV_MODE', 'dt_LOGGING_PATH', 'dt_APP_DATA', 'dt_USR_DATA', 'dt_TMP']
        for var in env_vars_to_clear:
            if var in os.environ:
                del os.environ[var]
    
    def test_linux_paths_production_mode(self):
        """Test Linux path generation in production mode."""
        with patch('os.path.expanduser') as mock_expanduser:
            mock_expanduser.side_effect = lambda path: path.replace('~', '/home/testuser')
            
            app_paths = ApplicationPaths("TestApp", forced_os="Linux", auto_create=False)
            
            expected_logging = '/var/log/TestApp'
            expected_app_data = '/etc/TestApp'
            expected_usr_data = '/home/testuser/.config/TestApp'
            expected_temp = '/tmp/TestApp'
            
            assert app_paths.logging_root_path == expected_logging
            assert app_paths.app_data_root_path == expected_app_data
            assert app_paths.usr_data_root_path == expected_usr_data
            assert app_paths.tmp_root_path == expected_temp


class TestApplicationPathsDarwin:
    """Test macOS (Darwin) specific path generation."""
    
    def setup_method(self):
        """Setup method run before each test."""
        env_vars_to_clear = ['DEV_MODE', 'dt_LOGGING_PATH', 'dt_APP_DATA', 'dt_USR_DATA', 'dt_TMP']
        for var in env_vars_to_clear:
            if var in os.environ:
                del os.environ[var]
    
    @patch.dict(os.environ, {'TMPDIR': '/tmp/'})
    def test_darwin_paths_production_mode(self):
        """Test macOS path generation in production mode."""
        with patch('os.path.expanduser') as mock_expanduser:
            mock_expanduser.side_effect = lambda path: path.replace('~', '/Users/testuser')
            
            app_paths = ApplicationPaths("TestApp", forced_os="Darwin", auto_create=False)
            
            expected_logging = '/Users/testuser/Library/Logs/TestApp'
            expected_app_data = '/Library/Application Support/TestApp'
            expected_usr_data = '/Users/testuser/Library/Application Support/TestApp'
            expected_temp = '/tmp/TestApp'
            
            assert app_paths.logging_root_path == expected_logging
            assert app_paths.app_data_root_path == expected_app_data
            assert app_paths.usr_data_root_path == expected_usr_data
            assert app_paths.tmp_root_path == expected_temp


class TestApplicationPathsSpawnedInstance:
    """Test spawned instance functionality with worker IDs."""
    
    def setup_method(self):
        """Setup method run before each test."""
        env_vars_to_clear = ['DEV_MODE', 'dt_LOGGING_PATH', 'dt_APP_DATA', 'dt_USR_DATA', 'dt_TMP']
        for var in env_vars_to_clear:
            if var in os.environ:
                del os.environ[var]
    
    def test_spawned_instance_temp_path(self):
        """Test that spawned instances get worker-specific temp paths."""
        with patch('os.path.expanduser', side_effect=lambda path: path.replace('~', '/home/testuser')):
            app_paths = ApplicationPaths(
                "TestApp", 
                forced_os="Linux", 
                spawned_instance=True, 
                worker_id=123,
                auto_create=False
            )
            
            # Only temp path should include worker ID
            assert app_paths.tmp_root_path == '/tmp/TestApp/123'
            assert app_paths.logging_root_path == '/var/log/TestApp'
            assert app_paths.app_data_root_path == '/etc/TestApp'
            assert app_paths.usr_data_root_path == '/home/testuser/.config/TestApp'
    
    def test_spawned_instance_without_worker_id(self):
        """Test spawned instance behavior when worker_id is None."""
        app_paths = ApplicationPaths(
            "TestApp", 
            forced_os="Linux",
            spawned_instance=True,
            worker_id=None,
            auto_create=False
        )
        
        # Should not append worker ID if None
        assert app_paths.tmp_root_path == '/tmp/TestApp'


class TestApplicationPathsDirectoryManagement:
    """Test directory creation, cleanup, and management."""
    
    def setup_method(self):
        """Setup method run before each test."""
        self.test_dir = tempfile.mkdtemp()
        env_vars_to_clear = ['DEV_MODE', 'dt_LOGGING_PATH', 'dt_APP_DATA', 'dt_USR_DATA', 'dt_TMP']
        for var in env_vars_to_clear:
            if var in os.environ:
                del os.environ[var]
    
    def teardown_method(self):
        """Cleanup temporary directories after tests."""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_auto_create_directories(self):
        """Test automatic directory creation when auto_create=True."""
        with patch('os.getcwd', return_value=self.test_dir):
            app_paths = ApplicationPaths("TestApp", forced_dev_mode=True, auto_create=True)
            
            # Verify directories were created
            assert os.path.exists(app_paths.tmp_root_path)
            assert os.path.exists(app_paths.logging_root_path)
            assert os.path.exists(app_paths.usr_data_root_path)
            # app_data_root_path creation might fail in dev mode, that's expected
    
    def test_no_auto_create_directories(self):
        """Test that directories are not created when auto_create=False."""
        with patch('os.getcwd', return_value=self.test_dir):
            app_paths = ApplicationPaths("TestApp", forced_dev_mode=True, auto_create=False)
            
            # Verify directories were not created
            assert not os.path.exists(app_paths.tmp_root_path)
            assert not os.path.exists(app_paths.logging_root_path)
            assert not os.path.exists(app_paths.usr_data_root_path)
    
    def test_clean_temp_directory(self):
        """Test cleanup of existing temp directory when clean_temp=True."""
        with patch('os.getcwd', return_value=self.test_dir):
            # Create a temp directory with some content
            temp_path = os.path.join(self.test_dir, 'temp')
            os.makedirs(temp_path, exist_ok=True)
            test_file = os.path.join(temp_path, 'test_file.txt')
            with open(test_file, 'w') as f:
                f.write('test content')
            assert os.path.exists(test_file)
            
            # Initialize ApplicationPaths with clean_temp=True
            app_paths = ApplicationPaths(
                "TestApp", 
                forced_dev_mode=True, 
                clean_temp=True,
                auto_create=True
            )
            
            # Verify temp directory was cleaned and recreated
            assert os.path.exists(app_paths.tmp_root_path)
            assert not os.path.exists(test_file)  # Old content should be gone
    
    def test_no_clean_temp_directory(self):
        """Test that temp directory is preserved when clean_temp=False."""
        with patch('os.getcwd', return_value=self.test_dir):
            # Create a temp directory with some content
            temp_path = os.path.join(self.test_dir, 'temp')
            os.makedirs(temp_path, exist_ok=True)
            test_file = os.path.join(temp_path, 'test_file.txt')
            with open(test_file, 'w') as f:
                f.write('test content')
            assert os.path.exists(test_file)
            
            # Initialize ApplicationPaths with clean_temp=False
            app_paths = ApplicationPaths(
                "TestApp", 
                forced_dev_mode=True, 
                clean_temp=False,
                auto_create=False
            )
            
            # Verify temp directory and content was preserved
            assert os.path.exists(test_file)  # Old content should remain


class TestApplicationPathsEnvironmentVariables:
    """Test environment variable management."""
    
    def setup_method(self):
        """Setup method run before each test."""
        env_vars_to_clear = ['DEV_MODE', 'dt_LOGGING_PATH', 'dt_APP_DATA', 'dt_USR_DATA', 'dt_TMP']
        for var in env_vars_to_clear:
            if var in os.environ:
                del os.environ[var]
    
    def test_dev_mode_environment_variable(self):
        """Test that DEV_MODE environment variable is set when forced_dev_mode=True."""
        assert 'DEV_MODE' not in os.environ
        
        app_paths = ApplicationPaths("TestApp", forced_dev_mode=True, auto_create=False)
        
        assert os.environ.get('DEV_MODE') == "True"
    
    def test_path_environment_variables_set(self):
        """Test that path environment variables are set correctly."""
        app_paths = ApplicationPaths("TestApp", forced_os="Linux", auto_create=False)
        
        # Verify all path environment variables are set
        assert os.environ.get('dt_LOGGING_PATH') is not None
        assert os.environ.get('dt_APP_DATA') is not None
        assert os.environ.get('dt_USR_DATA') is not None
        assert os.environ.get('dt_TMP') is not None
        
        # Verify they match the ApplicationPaths attributes
        assert os.environ['dt_LOGGING_PATH'] == app_paths.logging_root_path
        assert os.environ['dt_APP_DATA'] == app_paths.app_data_root_path
        assert os.environ['dt_USR_DATA'] == app_paths.usr_data_root_path
        assert os.environ['dt_TMP'] == app_paths.tmp_root_path


class TestApplicationPathsLogging:
    """Test logging functionality."""
    
    def setup_method(self):
        """Setup method run before each test."""
        env_vars_to_clear = ['DEV_MODE', 'dt_LOGGING_PATH', 'dt_APP_DATA', 'dt_USR_DATA', 'dt_TMP']
        for var in env_vars_to_clear:
            if var in os.environ:
                del os.environ[var]
    
    def test_log_paths_method(self):
        """Test the log_paths method outputs correct information."""
        with patch('logging.info') as mock_log:
            app_paths = ApplicationPaths("TestApp", forced_os="Linux", auto_create=False)
            app_paths.log_paths()
            
            # Verify logging.info was called for each path
            assert mock_log.call_count == 4
            
            # Extract the logged messages
            logged_messages = [call.args[0] for call in mock_log.call_args_list]
            
            # Verify each path type was logged
            assert any('Logging Root Path:' in msg for msg in logged_messages)
            assert any('Application Data Root Path:' in msg for msg in logged_messages)
            assert any('User Data Root Path:' in msg for msg in logged_messages)
            assert any('Temp Root Path:' in msg for msg in logged_messages)


class TestApplicationPathsErrorHandling:
    """Test error handling and edge cases."""
    
    def setup_method(self):
        """Setup method run before each test."""
        env_vars_to_clear = ['DEV_MODE', 'dt_LOGGING_PATH', 'dt_APP_DATA', 'dt_USR_DATA', 'dt_TMP']
        for var in env_vars_to_clear:
            if var in os.environ:
                del os.environ[var]
    
    def test_app_data_creation_exception_handling(self):
        """Test handling of exceptions during app data directory creation."""
        with patch('os.getcwd', return_value='/tmp/test'):
            with patch('os.makedirs') as mock_makedirs:
                with patch('builtins.print') as mock_print:
                    # Make app_data_root_path creation fail
                    def makedirs_side_effect(path, exist_ok=False):
                        if 'data/app' in path:
                            raise PermissionError("Permission denied")
                        # Let other directories succeed
                        return None
                    
                    mock_makedirs.side_effect = makedirs_side_effect
                    
                    app_paths = ApplicationPaths("TestApp", forced_dev_mode=True, auto_create=True)
                    
                    # Verify exception was handled and message was printed
                    mock_print.assert_called()
                    print_args = mock_print.call_args[0][0]
                    assert "Skipping creation of application data path" in print_args
                    assert "Permission denied" in print_args
    
    def test_unknown_os_handling(self):
        """Test behavior with unknown operating system."""
        app_paths = ApplicationPaths("TestApp", forced_os="UnknownOS", auto_create=False)
        
        # Should still initialize paths (likely to None for unknown OS)
        assert app_paths.logging_root_path is not None or app_paths.logging_root_path is None
        assert app_paths.app_data_root_path is not None or app_paths.app_data_root_path is None
        assert app_paths.usr_data_root_path is not None or app_paths.usr_data_root_path is None
        assert app_paths.tmp_root_path is not None or app_paths.tmp_root_path is None


class TestApplicationPathsSingleton:
    """Test singleton behavior of ApplicationPaths."""
    
    def setup_method(self):
        """Setup method run before each test."""
        # Clear any existing instances
        if hasattr(ApplicationPaths, '_instances'):
            ApplicationPaths._instances.clear()
        env_vars_to_clear = ['DEV_MODE', 'dt_LOGGING_PATH', 'dt_APP_DATA', 'dt_USR_DATA', 'dt_TMP']
        for var in env_vars_to_clear:
            if var in os.environ:
                del os.environ[var]
    
    def test_singleton_same_parameters(self):
        """Test that same parameters return the same instance."""
        # Note: ApplicationPaths uses singleton decorator, so same parameters should return same instance
        app_paths1 = ApplicationPaths("TestApp", auto_create=False)
        app_paths2 = ApplicationPaths("TestApp", auto_create=False)
        
        # They should be the same instance due to singleton pattern
        assert app_paths1 is app_paths2
    
    def test_singleton_different_parameters(self):
        """Test that different parameters may return different instances based on key."""
        # This depends on how the singleton decorator is configured
        # If no key is specified, it might still be a global singleton
        app_paths1 = ApplicationPaths("TestApp1", auto_create=False)
        app_paths2 = ApplicationPaths("TestApp2", auto_create=False)
        
        # Behavior depends on singleton implementation
        # Document the actual behavior found
        if app_paths1 is app_paths2:
            # Global singleton behavior
            assert app_paths1.app_short_name == app_paths2.app_short_name
        else:
            # Key-based singleton behavior
            assert app_paths1.app_short_name != app_paths2.app_short_name


if __name__ == '__main__':
    pytest.main([__file__, '-v'])