============
Installation
============

This guide covers installing dtPyAppFramework and its dependencies across different platforms and deployment scenarios.

Requirements
============

System Requirements
-------------------

* **Python**: 3.10 or higher
* **Operating Systems**: 
  - Windows 10/11
  - macOS 10.15+ (Catalina or later)  
  - Linux (Ubuntu 20.04+, CentOS 8+, or equivalent)

Python Dependencies
-------------------

dtPyAppFramework automatically installs these core dependencies:

.. code-block:: text

    PyYaml~=6.0.2                     # Configuration file parsing
    colorlog~=6.9.0                   # Console color coding for logs
    psutil~=6.1.0                     # Process monitoring and management
    pybase64~=1.4.0                   # Base64 encoding utilities
    boto3~=1.35.54                    # AWS integration (secrets, services)
    cryptography~=44.0.0              # Local encryption and cryptographic functions
    azure-identity                    # Azure authentication
    azure-keyvault-secrets            # Azure Key Vault integration
    azure-core~=1.32.0               # Azure core services
    InquirerPy                       # Interactive CLI prompts and interfaces
    watchdog~=6.0.0                  # File system monitoring and auto-reload

Platform-Specific Dependencies
-------------------------------

**Windows Only:**
  - ``pywin32`` - Windows-specific functionality and service support

**Development Dependencies (optional):**
  - ``pytest~=8.3.3`` - Testing framework
  - ``pytest-mock`` - Mocking capabilities for tests
  - ``pytest-watch`` - Continuous testing during development

Installation Methods
====================

Standard Installation
---------------------

Install from PyPI using pip:

.. code-block:: bash

    pip install dtPyAppFramework

Development Installation
------------------------

For development work or to get the latest features:

.. code-block:: bash

    # Clone the repository
    git clone https://github.com/your-org/dtPyAppFramework.git
    cd dtPyAppFramework

    # Install in development mode
    pip install -e .

    # Install development dependencies
    pip install -e .[dev]

Virtual Environment Installation
--------------------------------

**Recommended approach** for project isolation:

.. code-block:: bash

    # Create virtual environment
    python -m venv dtpyapp-env

    # Activate virtual environment
    # On Windows:
    dtpyapp-env\Scripts\activate
    # On macOS/Linux:
    source dtpyapp-env/bin/activate

    # Install framework
    pip install dtPyAppFramework

Docker Installation
-------------------

Create a Dockerfile for containerized deployment:

.. code-block:: dockerfile

    FROM python:3.12-slim

    # Set working directory
    WORKDIR /app

    # Install system dependencies
    RUN apt-get update && apt-get install -y \
        gcc \
        && rm -rf /var/lib/apt/lists/*

    # Copy requirements and install Python dependencies
    COPY requirements.txt .
    RUN pip install --no-cache-dir -r requirements.txt

    # Install dtPyAppFramework
    RUN pip install dtPyAppFramework

    # Copy application code
    COPY . .

    # Create non-root user
    RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
    USER appuser

    # Command to run the application
    CMD ["python", "your_app.py"]

Platform-Specific Setup
=======================

Windows Setup
-------------

**Prerequisites:**
1. Install Python 3.10+ from `python.org <https://www.python.org/downloads/>`_
2. Ensure pip is available and updated

**Installation:**

.. code-block:: cmd

    # Update pip
    python -m pip install --upgrade pip

    # Install framework
    pip install dtPyAppFramework

**Windows Service Support:**

.. code-block:: cmd

    # Install additional Windows dependencies
    pip install pywin32

    # Register COM objects (run as Administrator)
    python Scripts/pywin32_postinstall.py -install

macOS Setup
-----------

**Prerequisites:**
1. Install Python 3.10+ via Homebrew (recommended) or python.org

.. code-block:: bash

    # Using Homebrew
    brew install python@3.10

**Installation:**

.. code-block:: bash

    # Update pip
    python3.10 -m pip install --upgrade pip

    # Install framework
    pip3.10 install dtPyAppFramework

Linux Setup
-----------

**Ubuntu/Debian:**

.. code-block:: bash

    # Update package manager
    sudo apt update

    # Install Python and dependencies
    sudo apt install python3.10 python3.10-pip python3.10-venv python3.10-dev

    # Install framework
    pip3.10 install dtPyAppFramework

**CentOS/RHEL/Fedora:**

.. code-block:: bash

    # Install Python and dependencies
    sudo dnf install python3.10 python3.10-pip python3.10-devel

    # Install framework
    pip3.10 install dtPyAppFramework

**Alpine Linux (for minimal Docker images):**

.. code-block:: bash

    # Install dependencies
    apk add --no-cache python3 py3-pip gcc musl-dev python3-dev

    # Install framework
    pip install dtPyAppFramework

Cloud Platform Setup
====================

AWS Environment
---------------

**EC2 Instance Setup:**

.. code-block:: bash

    # Amazon Linux 2
    sudo yum update -y
    sudo yum install python3.10 python3.10-pip -y

    # Install framework
    pip3.10 install dtPyAppFramework

    # Configure AWS credentials (if not using IAM roles)
    aws configure

**Lambda Function Setup:**

Create a ``requirements.txt`` file:

.. code-block:: text

    dtPyAppFramework
    
Package your Lambda function:

.. code-block:: bash

    # Create deployment package
    pip install -r requirements.txt -t .
    zip -r lambda-deployment.zip .

Azure Environment
-----------------

**Azure VM Setup:**

.. code-block:: bash

    # Ubuntu on Azure
    sudo apt update
    sudo apt install python3.10 python3.10-pip -y

    # Install framework
    pip3.10 install dtPyAppFramework

    # Install Azure CLI (optional)
    curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

**Azure Functions Setup:**

Create ``requirements.txt``:

.. code-block:: text

    dtPyAppFramework
    azure-functions

Deploy using Azure Functions Core Tools:

.. code-block:: bash

    func azure functionapp publish your-function-app

Google Cloud Platform
---------------------

**Compute Engine Setup:**

.. code-block:: bash

    # Install Python
    sudo apt update
    sudo apt install python3.10 python3.10-pip -y

    # Install framework
    pip3.10 install dtPyAppFramework

    # Install Google Cloud SDK (optional)
    curl https://sdk.cloud.google.com | bash

Verification
============

Verify Installation
-------------------

Create a simple test script to verify the installation:

.. code-block:: python

    # test_installation.py
    try:
        from dtPyAppFramework.application import AbstractApp
        from dtPyAppFramework.settings import Settings
        from dtPyAppFramework.paths import ApplicationPaths
        from dtPyAppFramework.logging import initialise_logging
        
        print("✓ Core modules imported successfully")
        
        # Test basic functionality
        paths = ApplicationPaths(app_short_name="test")
        settings = Settings()
        
        print("✓ Basic components initialized successfully")
        print("✓ dtPyAppFramework installation verified!")
        
    except ImportError as e:
        print(f"✗ Import error: {e}")
        print("Installation may be incomplete")
    except Exception as e:
        print(f"✗ Unexpected error: {e}")

Run the verification:

.. code-block:: bash

    python test_installation.py

Check Framework Version
-----------------------

.. code-block:: python

    from dtPyAppFramework import version
    print(f"dtPyAppFramework version: {version()}")

Development Environment Setup
=============================

IDE Configuration
-----------------

**Visual Studio Code:**

Create ``.vscode/settings.json``:

.. code-block:: json

    {
        "python.defaultInterpreterPath": "./dtpyapp-env/bin/python",
        "python.linting.enabled": true,
        "python.linting.pylintEnabled": true,
        "python.formatting.provider": "black"
    }

**PyCharm:**
1. File → Settings → Project → Python Interpreter
2. Add interpreter → Existing environment
3. Select your virtual environment's Python executable

Testing Setup
--------------

Install testing dependencies:

.. code-block:: bash

    pip install pytest pytest-mock pytest-watch

Create ``pytest.ini``:

.. code-block:: ini

    [tool:pytest]
    testpaths = tests
    python_files = test_*.py
    python_classes = Test*
    python_functions = test_*
    addopts = -v --tb=short

Run tests:

.. code-block:: bash

    # Run all tests
    pytest

    # Run with coverage
    pytest --cov=dtPyAppFramework

    # Continuous testing
    pytest-watch

Troubleshooting
===============

Common Issues
-------------

**Python Version Error:**

.. code-block:: bash

    ERROR: Python 3.10 or higher is required

Solution: Install Python 3.10+:

.. code-block:: bash

    # Check current version
    python --version
    
    # Install correct version (platform-specific)
    # See platform-specific setup sections above

**Permission Errors on Windows:**

.. code-block:: bash

    ERROR: Could not install packages due to an EnvironmentError: [WinError 5]

Solution: Run command prompt as Administrator or use `--user` flag:

.. code-block:: bash

    pip install --user dtPyAppFramework

**pywin32 Installation Issues:**

.. code-block:: bash

    # Manual pywin32 setup
    pip install pywin32
    python Scripts/pywin32_postinstall.py -install

**Azure Dependencies Issues:**

.. code-block:: bash

    # Update Azure components
    pip install --upgrade azure-identity azure-keyvault-secrets azure-core

**AWS Dependencies Issues:**

.. code-block:: bash

    # Update boto3
    pip install --upgrade boto3 botocore

**Cryptography Installation Issues:**

On some systems, you may need to install system dependencies:

.. code-block:: bash

    # Ubuntu/Debian
    sudo apt install build-essential libffi-dev python3-dev

    # CentOS/RHEL
    sudo yum install gcc openssl-devel libffi-devel python3-devel

    # macOS (with Homebrew)
    brew install libffi

**Import Errors:**

If you encounter import errors, verify your Python path:

.. code-block:: python

    import sys
    print(sys.path)
    
    # Verify framework location
    import dtPyAppFramework
    print(dtPyAppFramework.__file__)

Upgrading
=========

Standard Upgrade
----------------

.. code-block:: bash

    pip install --upgrade dtPyAppFramework

Force Reinstallation
--------------------

.. code-block:: bash

    pip install --force-reinstall dtPyAppFramework

Development Upgrade
-------------------

.. code-block:: bash

    # Pull latest changes
    git pull origin main
    
    # Reinstall in development mode
    pip install -e .

Migration Between Versions
--------------------------

Check the changelog for breaking changes and migration guides:

.. code-block:: bash

    # Check current version
    python -c "from dtPyAppFramework import version; print(version())"

Uninstallation
==============

Complete Removal
-----------------

.. code-block:: bash

    # Uninstall framework
    pip uninstall dtPyAppFramework

    # Remove configuration directories (optional)
    # Linux (regular user):
    rm -rf ~/.local/state/your-app-name
    rm -rf ~/.config/your-app-name
    rm -rf ~/.local/share/your-app-name

    # Linux (root/service):
    # sudo rm -rf /var/log/your-app-name
    # sudo rm -rf /var/lib/your-app-name
    # sudo rm -rf /etc/your-app-name

    # macOS:

    # Windows:
    # Remove %APPDATA%\your-app-name and %LOCALAPPDATA%\your-app-name

Clean Virtual Environment
--------------------------

.. code-block:: bash

    # Deactivate environment
    deactivate

    # Remove environment directory
    rm -rf dtpyapp-env

The installation process is designed to be straightforward across all supported platforms. If you encounter any issues not covered in this guide, please check the project's issue tracker or contact support.