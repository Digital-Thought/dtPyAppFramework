# dtPyAppFramework

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)

Welcome to `dtPyAppFramework` – A Python library for common features in application development.

## Introduction

`dtPyAppFramework` is a Python library that provides essential features commonly required in application development.<br>
It aims to streamline the development process by offering solutions for:

- Logging
- Configuration file management
- Secure secrets storage and retrieval
- Command line argument parsing
- Temporary storage directory management
- Accessing common resource paths
- Support for MultiProcessing

## Installation

You can install `dtPyAppFramework` using `pip`:

```bash
pip install dtPyAppFramework
```

## Getting Started
To get started with `dtPyAppFramework`, follow these basic usage examples:
```python
from dtPyAppFramework.app import AbstractApp
from dtPyAppFramework import settings

import logging

class SimpleApp(AbstractApp):

    def define_args(self, arg_parser):
        return

    def main(self, args):
        logging.info("Running your code")
        ## Place you own code here that you wish to run

SimpleApp(description="Simple App", version="1.0", short_name="simple_app",
          full_name="Simple Application", console_app=True).run()
```

The above example will output the following to the console:

![Output](docs/simple_app_output.jpg)

## Features
Now lets take some time to go over the various features that makes `dtPyAppFramework` such a power library to base your 
Python projects of.

### Logging
`dtPyAppFramework` offers flexible logging capabilities, allowing you to configure and manage logs easily. <br>
In addition it offers some pretty cool logging capabilities straight out of the door which requires no setup from you.

[More about logging](docs/Logging.md)

### Configuration Files
Easily read and manage configuration settings from configurations files.<br>
Configuration files can be set for a specific user or for any user of the application.

[More about configuration files](docs/Configuration_Files.md)

### Secrets Management
Securely store and retrieve sensitive information with encryption and best practices.<br>
You can store secrets for a specific user or make secrets available to all users of the application.<br>
In addition, you can use the AWS Secrets Management seamlessly within the application alongside the in-built secrets store.

[More about secrets management](docs/Secrets_Management.md)

### Command Line Arguments
Effortlessly parse and manage command line arguments with support for defining options and accessing them in your code.

[More about command line arguments](docs/Command_Line_Arguments.md)

### Temporary Storage
Create and manage temporary storage directories, including handling cleanup.

[More about temporary storage](docs/Temporary_Storage.md)

### Resource Paths
Access common resource paths like user storage directories.

[More about resource paths](docs/Resource_Paths.md)

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).

## Contact

If you have any questions, bug reports, or feature requests, feel free to [contact us](mailto:matthew@digital-thought.org).