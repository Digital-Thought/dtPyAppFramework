# Command Line Arguments

The **dtPyAppFramework** provides flexible command line argument handling to cater to the specific needs of your application. This is achieved by implementing the `define_args` method within your custom application class, which inherits from the `AbstractApp` class.

## Customising Command Line Arguments

When you create an instance of your application class, you can define custom command line arguments by overriding the `define_args` method. This method is responsible for defining the command line arguments specific to your application.

Here's a basic example:

```python
from dtPyAppFramework.application import AbstractApp, argparse

class MyCustomApp(AbstractApp):
    def __init__(self):
        super().__init__(description="My Custom App", version="1.0", short_name="custom_app",
                         full_name="Custom Application", console_app=True)

    def define_args(self, arg_parser: argparse.ArgumentParser):
        """
        Define command-line arguments for the application.

        Args:
            arg_parser (argparse.ArgumentParser): The ArgumentParser object for defining command-line arguments.
        """
        # Add your custom command line arguments here
        arg_parser.add_argument('--custom_arg', action='store', type=str, required=False,
                                help="Description of your custom argument.")
```

In the example above, the define_args method is overridden, and a custom command line argument --custom_arg is defined. You can add as many custom arguments as needed for your application.

## Handling Command Line Arguments
The main method in your application class receives the parsed command line arguments. You can access the values of these arguments as attributes of the args object.

Here's an example:

```python
from dtPyAppFramework.application import AbstractApp

class MyCustomApp(AbstractApp):
    def __init__(self):
        super().__init__(description="My Custom App", version="1.0", short_name="custom_app",
                         full_name="Custom Application", console_app=True)

    def define_args(self, arg_parser):
        arg_parser.add_argument('--custom_arg', action='store', type=str, required=False,
                                help="Description of your custom argument.")

    def main(self, args):
        # Access the value of the custom argument
        custom_arg_value = args.custom_arg
        print(f"Value of custom argument: {custom_arg_value}")

```

In this example, the main method retrieves the value of the --custom_arg command line argument using args.custom_arg.

Now, when you run your application, you can provide the custom argument from the command line:

```bash
python my_custom_app.py --custom_arg value
```

This provides a flexible way to tailor the command line interface of your application to suit its specific functionality.