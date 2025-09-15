"""
Comprehensive tests for AbstractApp application base class.

This test suite ensures that AbstractApp correctly handles application initialization,
argument parsing, process management integration, and provides the proper interface
for concrete application implementations.
"""

import pytest
import os
import sys
import argparse
from unittest.mock import patch, MagicMock, call
from argparse import ArgumentParser

# Add the src directory to Python path for imports  
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from dtPyAppFramework.application import AbstractApp


class ConcreteTestApp(AbstractApp):
    """Concrete implementation of AbstractApp for testing."""
    
    def __init__(self, description="Test Application", version="1.0.0", 
                 short_name="testapp", full_name="Test Application", 
                 console_app=True):
        super().__init__(description, version, short_name, full_name, console_app)
        self.define_args_called = False
        self.main_called = False
        self.exiting_called = False
        self.main_args = None
    
    def define_args(self, arg_parser: ArgumentParser):
        """Implementation of abstract method for testing."""
        self.define_args_called = True
        arg_parser.add_argument('--test', action='store_true', help='Test argument')
    
    def main(self, args):
        """Implementation of abstract method for testing."""
        self.main_called = True
        self.main_args = args
    
    def exiting(self):
        """Implementation of abstract method for testing."""
        self.exiting_called = True


class TestAbstractAppBasic:
    """Test basic AbstractApp functionality and initialization."""
    
    def test_basic_initialization(self):
        """Test basic AbstractApp initialization with required parameters."""
        app = ConcreteTestApp(
            description="Test Application",
            version="1.0.0",
            short_name="testapp", 
            full_name="Test Application",
            console_app=True
        )
        
        # Verify app_spec dictionary
        assert app.app_spec['description'] == "Test Application"
        assert app.app_spec['version'] == "1.0.0"
        assert app.app_spec['short_name'] == "testapp"
        assert app.app_spec['full_name'] == "Test Application"
        
        # Verify console_app and process_manager
        assert app.console_app is True
        assert app.process_manager is None
    
    def test_initialization_defaults(self):
        """Test AbstractApp initialization with default parameters."""
        app = ConcreteTestApp(
            description="Test App",
            version="2.0.0",
            short_name="test",
            full_name="Test App"
        )
        
        # Verify defaults
        assert app.console_app is True  # Default value
        assert app.process_manager is None
    
    def test_initialization_with_console_false(self):
        """Test AbstractApp initialization with console_app=False."""
        app = ConcreteTestApp(
            description="Test App",
            version="1.0.0", 
            short_name="test",
            full_name="Test App",
            console_app=False
        )
        
        assert app.console_app is False
    
    @patch('sys.argv', ['script.py', '--console'])
    def test_console_argument_override(self):
        """Test that --console argument overrides console_app=False."""
        app = ConcreteTestApp(
            description="Test App",
            version="1.0.0",
            short_name="test", 
            full_name="Test App",
            console_app=False
        )
        
        assert app.console_app is True  # Should be overridden by --console
    
    @patch('sys.argv', ['script.py', '-c'])
    def test_console_short_argument_override(self):
        """Test that -c argument overrides console_app=False."""
        app = ConcreteTestApp(
            description="Test App",
            version="1.0.0",
            short_name="test",
            full_name="Test App", 
            console_app=False
        )
        
        assert app.console_app is True  # Should be overridden by -c


class TestAbstractAppProperties:
    """Test AbstractApp property methods."""
    
    def test_version_property(self):
        """Test version property returns correct value."""
        app = ConcreteTestApp(
            description="Test App",
            version="3.2.1",
            short_name="test",
            full_name="Test App"
        )
        
        assert app.version == "3.2.1"
    
    def test_description_property(self):
        """Test description property returns correct value.""" 
        app = ConcreteTestApp(
            description="My Test Application",
            version="1.0.0",
            short_name="test",
            full_name="Test App"
        )
        
        assert app.description == "My Test Application"
    
    def test_short_name_property(self):
        """Test short_name property returns correct value."""
        app = ConcreteTestApp(
            description="Test App",
            version="1.0.0", 
            short_name="myapp",
            full_name="Test App"
        )
        
        assert app.short_name == "myapp"
    
    def test_full_name_property(self):
        """Test full_name property returns correct value."""
        app = ConcreteTestApp(
            description="Test App",
            version="1.0.0",
            short_name="test",
            full_name="My Full Application Name"
        )
        
        assert app.full_name == "My Full Application Name"


class TestAbstractAppArgumentParsing:
    """Test argument parsing and definition functionality."""
    
    def test_define_args_called(self):
        """Test that define_args is called during argument parsing."""
        app = ConcreteTestApp()
        
        # Create a mock argument parser
        arg_parser = MagicMock()
        
        # Call the private method that should call define_args
        app._AbstractApp__define_args(arg_parser)
        
        # Verify define_args was called on our concrete implementation
        assert app.define_args_called is True
    
    def test_common_arguments_added(self):
        """Test that common framework arguments are added."""
        app = ConcreteTestApp()
        
        # Use a real ArgumentParser to test actual argument addition
        arg_parser = ArgumentParser()
        
        # Mock parse_known_args to return empty opts
        with patch.object(arg_parser, 'parse_known_args') as mock_parse:
            mock_opts = MagicMock()
            mock_opts.working_dir = None
            mock_opts.single_folder = False
            mock_opts.service = False
            mock_opts.init = False
            mock_opts.add_secret = False
            mock_parse.return_value = (mock_opts, [])
            
            app._AbstractApp__define_args(arg_parser)
        
        # Verify common arguments were added (check by trying to parse them)
        with patch('os.chdir'):
            args = arg_parser.parse_args(['--init', '--add_secret', '--run', '--service', '--console', '--single_folder'])
            assert args.init is True
            assert args.add_secret is True  
            assert args.run is True
            assert args.service is True
            assert args.console is True
            assert args.single_folder is True
    
    def test_working_directory_change(self):
        """Test working directory change when --working_dir is provided."""
        app = ConcreteTestApp()
        arg_parser = ArgumentParser()
        
        with patch.object(arg_parser, 'parse_known_args') as mock_parse:
            mock_opts = MagicMock()
            mock_opts.working_dir = '/tmp/test'
            mock_opts.single_folder = False
            mock_opts.service = False  
            mock_opts.init = False
            mock_opts.add_secret = False
            mock_parse.return_value = (mock_opts, [])
            
            with patch('os.chdir') as mock_chdir:
                app._AbstractApp__define_args(arg_parser)
                mock_chdir.assert_called_once_with('/tmp/test')
    
    def test_dev_mode_environment_variable(self):
        """Test DEV_MODE environment variable set when --single_folder is used."""
        app = ConcreteTestApp()
        arg_parser = ArgumentParser()
        
        # Clear any existing DEV_MODE
        if 'DEV_MODE' in os.environ:
            del os.environ['DEV_MODE']
        
        with patch.object(arg_parser, 'parse_known_args') as mock_parse:
            mock_opts = MagicMock() 
            mock_opts.working_dir = None
            mock_opts.single_folder = True
            mock_opts.service = False
            mock_opts.init = False
            mock_opts.add_secret = False
            mock_parse.return_value = (mock_opts, [])
            
            app._AbstractApp__define_args(arg_parser)
            
            assert os.environ.get('DEV_MODE') == "True"
        
        # Cleanup
        if 'DEV_MODE' in os.environ:
            del os.environ['DEV_MODE']
    
    def test_service_specific_arguments(self):
        """Test that service-specific arguments are added when --service is used."""
        app = ConcreteTestApp()
        arg_parser = ArgumentParser()
        
        with patch.object(arg_parser, 'parse_known_args') as mock_parse:
            mock_opts = MagicMock()
            mock_opts.working_dir = None
            mock_opts.single_folder = False
            mock_opts.service = True
            mock_opts.init = False
            mock_opts.add_secret = False
            mock_parse.return_value = (mock_opts, [])
            
            with patch.object(arg_parser, 'add_argument') as mock_add_arg:
                app._AbstractApp__define_args(arg_parser)
                
                # Verify --install was added for service mode
                install_call = call('--install', action='store_true')
                assert install_call in mock_add_arg.call_args_list
    
    def test_init_specific_arguments(self):
        """Test that init-specific arguments are added when --init is used.""" 
        app = ConcreteTestApp()
        arg_parser = ArgumentParser()
        
        with patch.object(arg_parser, 'parse_known_args') as mock_parse:
            mock_opts = MagicMock()
            mock_opts.working_dir = None
            mock_opts.single_folder = False
            mock_opts.service = False
            mock_opts.init = True
            mock_opts.add_secret = False
            mock_parse.return_value = (mock_opts, [])
            
            with patch.object(arg_parser, 'add_argument') as mock_add_arg:
                app._AbstractApp__define_args(arg_parser)
                
                # Verify --password was added for init mode
                password_call = call('--password', action='store', type=str, required=False,
                                   help="Secrets Store password")
                assert password_call in mock_add_arg.call_args_list
    
    def test_add_secret_specific_arguments(self):
        """Test that add_secret-specific arguments are added when --add_secret is used."""
        app = ConcreteTestApp()
        arg_parser = ArgumentParser()
        
        with patch.object(arg_parser, 'parse_known_args') as mock_parse:
            mock_opts = MagicMock()
            mock_opts.working_dir = None
            mock_opts.single_folder = False
            mock_opts.service = False
            mock_opts.init = False
            mock_opts.add_secret = True
            mock_parse.return_value = (mock_opts, [])
            
            with patch.object(arg_parser, 'add_argument') as mock_add_arg:
                with patch.object(arg_parser, 'add_mutually_exclusive_group') as mock_group:
                    mock_exclusive_group = MagicMock()
                    mock_group.return_value = mock_exclusive_group
                    
                    app._AbstractApp__define_args(arg_parser)
                    
                    # Verify --name argument was added
                    name_call = call('--name', action='store', type=str, required=False, help="Secret Name")
                    assert name_call in mock_add_arg.call_args_list
                    
                    # Verify --store_as argument was added
                    store_as_call = call('--store_as', action='store', type=str, default='raw',
                                       choices=['raw', 'base64'], help="Store file as either base64 or raw")
                    assert store_as_call in mock_add_arg.call_args_list
                    
                    # Verify mutually exclusive group was created
                    mock_group.assert_called_once_with(required=False)
                    
                    # Verify --value and --file were added to exclusive group
                    value_call = call('--value', action='store', type=str, help="Secret Value")
                    file_call = call('--file', action='store', type=str, help="File to add to secret")
                    assert value_call in mock_exclusive_group.add_argument.call_args_list
                    assert file_call in mock_exclusive_group.add_argument.call_args_list


class TestAbstractAppExitFunctionality:
    """Test exit and cleanup functionality."""
    
    def test_exit_calls_exiting(self):
        """Test that exit() calls the exiting() method."""
        app = ConcreteTestApp()
        
        with patch('dtPyAppFramework.settings.Settings') as mock_settings_class:
            mock_settings_instance = MagicMock()
            mock_settings_class.return_value = mock_settings_instance
            
            app.exit()
            
            # Verify exiting was called
            assert app.exiting_called is True
            
            # Verify Settings().close() was called
            mock_settings_instance.close.assert_called_once()
    
    def test_exit_handles_settings_cleanup(self):
        """Test that exit properly handles Settings cleanup."""
        app = ConcreteTestApp()
        
        with patch('dtPyAppFramework.settings.Settings') as mock_settings_class:
            mock_settings_instance = MagicMock()
            mock_settings_class.return_value = mock_settings_instance
            
            app.exit()
            
            # Verify Settings was instantiated and close was called
            mock_settings_class.assert_called_once()
            mock_settings_instance.close.assert_called_once()


class TestAbstractAppRunFunctionality:
    """Test main run functionality and integration."""
    
    @patch('dtPyAppFramework.application.ProcessManager')
    def test_run_creates_process_manager(self, mock_process_manager_class):
        """Test that run() creates and initializes ProcessManager."""
        app = ConcreteTestApp()
        
        mock_process_manager = MagicMock()
        mock_process_manager_class.return_value = mock_process_manager
        
        app.run()
        
        # Verify ProcessManager was created with correct parameters
        mock_process_manager_class.assert_called_once_with(
            description=app.description,
            version=app.version,
            short_name=app.short_name,
            full_name=app.full_name,
            console_app=app.console_app,
            main_procedure=app.main,
            exit_procedure=app.exit
        )
        
        # Verify ProcessManager was assigned and initialized
        assert app.process_manager is mock_process_manager
        mock_process_manager.initialise_application.assert_called_once()
    
    @patch('argparse.ArgumentParser')
    @patch('dtPyAppFramework.application.ProcessManager')
    def test_run_creates_argument_parser(self, mock_process_manager_class, mock_arg_parser_class):
        """Test that run() creates ArgumentParser with correct parameters."""
        app = ConcreteTestApp()
        
        mock_arg_parser = MagicMock()
        mock_arg_parser_class.return_value = mock_arg_parser
        
        mock_process_manager = MagicMock()
        mock_process_manager_class.return_value = mock_process_manager
        
        app.run()
        
        # Verify ArgumentParser was created with correct parameters
        mock_arg_parser_class.assert_called_once_with(
            prog=app.short_name,
            description=app.description
        )
        
        # Verify ProcessManager was initialized with the argument parser
        mock_process_manager.initialise_application.assert_called_once_with(mock_arg_parser)
    
    @patch('dtPyAppFramework.application.ProcessManager')  
    def test_run_integration_workflow(self, mock_process_manager_class):
        """Test complete run workflow integration."""
        app = ConcreteTestApp()
        
        mock_process_manager = MagicMock()
        mock_process_manager_class.return_value = mock_process_manager
        
        # Mock the argument parser creation and define_args call
        with patch('argparse.ArgumentParser') as mock_arg_parser_class:
            mock_arg_parser = MagicMock()
            mock_arg_parser_class.return_value = mock_arg_parser
            
            # Setup parse_known_args mock
            mock_opts = MagicMock()
            mock_opts.working_dir = None
            mock_opts.single_folder = False
            mock_opts.service = False
            mock_opts.init = False
            mock_opts.add_secret = False
            mock_arg_parser.parse_known_args.return_value = (mock_opts, [])
            
            app.run()
        
        # Verify complete workflow
        assert app.process_manager is mock_process_manager
        assert app.define_args_called is True
        mock_process_manager.initialise_application.assert_called_once()


class TestAbstractAppAbstractMethods:
    """Test abstract method enforcement."""
    
    def test_abstract_methods_must_be_implemented(self):
        """Test that abstract methods must be implemented in subclasses."""
        # This test verifies that the abstract methods are defined
        # The actual enforcement is done by Python's ABC mechanism
        
        # Verify that define_args is abstract
        with pytest.raises(TypeError):
            AbstractApp(
                description="Test",
                version="1.0.0", 
                short_name="test",
                full_name="Test"
            )
    
    def test_concrete_implementation_works(self):
        """Test that concrete implementation with all methods works."""
        # This should not raise any errors
        app = ConcreteTestApp()
        
        # Verify all abstract methods are implemented
        assert hasattr(app, 'define_args')
        assert hasattr(app, 'main')
        assert hasattr(app, 'exiting')
        
        # Verify they are callable
        assert callable(app.define_args)
        assert callable(app.main)
        assert callable(app.exiting)


class TestAbstractAppErrorHandling:
    """Test error handling and edge cases."""
    
    def test_main_method_receives_args(self):
        """Test that main method receives parsed arguments."""
        app = ConcreteTestApp()
        
        # Create test args
        test_args = MagicMock()
        test_args.test = True
        
        # Call main directly
        app.main(test_args)
        
        # Verify main was called and received args
        assert app.main_called is True
        assert app.main_args is test_args
        assert app.main_args.test is True
    
    def test_define_args_modifies_parser(self):
        """Test that define_args properly modifies the argument parser."""
        app = ConcreteTestApp()
        
        # Use real ArgumentParser
        arg_parser = ArgumentParser()
        
        # Call define_args
        app.define_args(arg_parser)
        
        # Verify our test argument was added
        try:
            args = arg_parser.parse_args(['--test'])
            assert args.test is True
        except SystemExit:
            pytest.fail("ArgumentParser failed to parse --test argument")
        
        # Verify it was actually called
        assert app.define_args_called is True
    
    def test_exiting_method_called(self):
        """Test that exiting method is properly called."""
        app = ConcreteTestApp()
        
        # Call exiting directly
        app.exiting()
        
        # Verify it was called
        assert app.exiting_called is True


class TestAbstractAppInheritance:
    """Test inheritance and polymorphism behavior."""
    
    def test_multiple_concrete_implementations(self):
        """Test that multiple concrete implementations can coexist."""
        class AnotherTestApp(AbstractApp):
            def define_args(self, arg_parser):
                arg_parser.add_argument('--another', action='store_true')
            
            def main(self, args):
                self.main_executed = True
            
            def exiting(self):
                self.exit_executed = True
        
        # Create instances of both
        app1 = ConcreteTestApp()
        app2 = AnotherTestApp(
            description="Another App",
            version="2.0.0",
            short_name="another", 
            full_name="Another App"
        )
        
        # Verify they are different
        assert app1.short_name != app2.short_name
        assert app1.version != app2.version
        
        # Verify they have different behaviors
        parser1 = ArgumentParser()
        parser2 = ArgumentParser()
        
        app1.define_args(parser1)
        app2.define_args(parser2)
        
        # Test that different arguments were added
        args1 = parser1.parse_args(['--test'])
        args2 = parser2.parse_args(['--another'])
        
        assert hasattr(args1, 'test')
        assert hasattr(args2, 'another')
    
    def test_super_initialization(self):
        """Test that super().__init__() is properly called."""
        class ChildApp(ConcreteTestApp):
            def __init__(self):
                super().__init__(
                    description="Child App",
                    version="3.0.0",
                    short_name="child",
                    full_name="Child Application"
                )
                self.child_initialized = True
        
        app = ChildApp()
        
        # Verify parent initialization occurred
        assert app.app_spec['description'] == "Child App"
        assert app.app_spec['version'] == "3.0.0"
        assert app.app_spec['short_name'] == "child"
        assert app.app_spec['full_name'] == "Child Application"
        
        # Verify child initialization occurred
        assert app.child_initialized is True
        
        # Verify all methods are still available
        assert app.define_args_called is False  # Not called yet
        app.define_args(ArgumentParser())
        assert app.define_args_called is True


if __name__ == '__main__':
    pytest.main([__file__, '-v'])