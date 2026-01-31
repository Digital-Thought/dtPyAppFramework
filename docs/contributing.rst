============
Contributing
============

Thank you for your interest in contributing to dtPyAppFramework! This guide provides information on how to contribute to the project effectively.

Types of Contributions
======================

We welcome several types of contributions:

**Bug Reports and Feature Requests**
  Report bugs or request new features through GitHub issues

**Code Contributions**
  Submit bug fixes, new features, or improvements via pull requests

**Documentation**
  Improve documentation, add examples, or fix typos

**Testing**
  Add test cases, improve test coverage, or test on different platforms

**Community Support**
  Help other users in discussions, forums, or issue comments

Getting Started
===============

Development Environment Setup
-----------------------------

1. **Fork and Clone the Repository**

.. code-block:: bash

    git clone https://github.com/yourusername/dtPyAppFramework.git
    cd dtPyAppFramework

2. **Create Virtual Environment**

.. code-block:: bash

    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate

3. **Install Development Dependencies**

.. code-block:: bash

    pip install -e .[dev]
    pip install -r requirements.txt

4. **Run Tests**

.. code-block:: bash

    pytest

Development Guidelines
======================

Code Style
----------

We follow PEP 8 with some specific guidelines:

**Python Code Standards:**

- Use 4 spaces for indentation
- Line length limit of 100 characters
- Use type hints where appropriate
- Follow existing code patterns and naming conventions

**Docstring Format:**

Use Google-style docstrings:

.. code-block:: python

    def example_function(param1: str, param2: int = 10) -> bool:
        """Brief description of the function.

        Longer description if needed, explaining the purpose
        and any important details.

        Args:
            param1: Description of first parameter.
            param2: Description of second parameter with default.

        Returns:
            Description of return value.

        Raises:
            ValueError: Description of when this exception is raised.
            
        Example:
            >>> example_function("test", 5)
            True
        """
        pass

**Import Organization:**

.. code-block:: python

    # Standard library imports
    import os
    import sys
    from typing import Dict, List, Optional

    # Third-party imports
    import yaml
    import boto3

    # Local imports
    from dtPyAppFramework.settings import Settings
    from .local_module import LocalClass

Testing Guidelines
------------------

**Test Coverage:**

- Maintain test coverage above 80%
- Write tests for all new features
- Include both positive and negative test cases
- Test error conditions and edge cases

**Test Structure:**

.. code-block:: python

    import pytest
    from unittest.mock import Mock, patch
    
    from dtPyAppFramework.settings import Settings

    class TestSettings:
        def setup_method(self):
            """Setup for each test method."""
            self.settings = Settings()
        
        def test_get_existing_setting(self):
            """Test retrieval of existing configuration setting."""
            # Test implementation
            pass
        
        def test_get_missing_setting_with_default(self):
            """Test retrieval of missing setting returns default."""
            # Test implementation
            pass
        
        @patch('dtPyAppFramework.settings.os.environ')
        def test_environment_variable_resolution(self, mock_environ):
            """Test environment variable resolution in settings."""
            # Test implementation with mocking
            pass

**Running Tests:**

.. code-block:: bash

    # Run all tests
    pytest

    # Run with coverage
    pytest --cov=src/dtPyAppFramework --cov-report=html

    # Run specific test file
    pytest tests/test_settings.py

    # Run with verbose output
    pytest -v

    # Run tests in parallel
    pytest -n auto

Documentation Guidelines
------------------------

**RST Format:**

- Use reStructuredText (.rst) format
- Follow existing documentation structure
- Include code examples for new features
- Update API documentation for code changes

**Documentation Structure:**

.. code-block:: text

    docs/
    ├── index.rst                 # Main documentation index
    ├── guides/                   # User guides
    │   ├── installation.rst
    │   ├── getting-started.rst
    │   └── configuration.rst
    ├── components/               # Component documentation
    │   ├── application.rst
    │   ├── configuration.rst
    │   └── secrets-management.rst
    ├── api/                      # API reference
    │   ├── application.rst
    │   └── settings.rst
    └── examples/                 # Example applications

**Building Documentation:**

.. code-block:: bash

    cd docs
    pip install -r requirements.txt
    make html
    # Open _build/html/index.html in browser

Pull Request Process
====================

1. **Create Feature Branch**

.. code-block:: bash

    git checkout -b feature/your-feature-name
    git checkout -b bugfix/issue-number

2. **Make Changes**

- Follow coding guidelines
- Add tests for new functionality
- Update documentation as needed
- Ensure all tests pass

3. **Commit Changes**

Use conventional commit format:

.. code-block:: bash

    git commit -m "feat: add new multiprocessing feature"
    git commit -m "fix: resolve configuration loading issue"
    git commit -m "docs: update installation guide"

**Commit Message Format:**

- ``feat``: New feature
- ``fix``: Bug fix
- ``docs``: Documentation changes
- ``test``: Adding or updating tests
- ``refactor``: Code refactoring
- ``style``: Formatting, missing semicolons, etc.
- ``chore``: Maintenance tasks

4. **Push and Create Pull Request**

.. code-block:: bash

    git push origin feature/your-feature-name

**Pull Request Description:**

Include:

- Clear description of changes
- Link to related issues
- Testing instructions
- Breaking changes (if any)
- Screenshots (for UI changes)

**Example PR Description:**

.. code-block:: text

    ## Description
    Add support for Azure Key Vault integration in secrets management system.

    ## Related Issues
    Fixes #123
    Related to #456

    ## Changes
    - Add AzureSecretsStore class
    - Implement Azure authentication
    - Add configuration options for Azure Key Vault
    - Update documentation

    ## Testing
    - [ ] Unit tests pass
    - [ ] Integration tests with Azure Key Vault
    - [ ] Documentation builds correctly

    ## Breaking Changes
    None

    ## Additional Notes
    Requires azure-keyvault-secrets dependency.

Code Review Process
===================

All contributions go through code review:

**Reviewer Guidelines:**

- Check code quality and style
- Verify test coverage
- Ensure documentation is updated
- Test functionality when possible
- Provide constructive feedback

**Contributor Guidelines:**

- Respond to feedback promptly
- Make requested changes
- Ask questions if feedback is unclear
- Be open to suggestions and improvements

**Review Criteria:**

- Code follows project standards
- Tests cover new functionality
- Documentation is clear and complete
- Changes are backward compatible (unless breaking change is justified)
- Performance impact is acceptable

Issue Reporting
===============

Good Bug Reports
----------------

Include the following information:

**Environment Information:**
- Operating system and version
- Python version
- dtPyAppFramework version
- Relevant dependency versions

**Problem Description:**
- Clear description of the issue
- Expected behavior vs actual behavior
- Steps to reproduce
- Minimal code example
- Error messages and stack traces

**Example Bug Report:**

.. code-block:: text

    ## Bug Report

    ### Environment
    - OS: Windows 11
    - Python: 3.10.0
    - dtPyAppFramework: 3.1.0
    - PyYAML: 6.0.2

    ### Description
    Configuration files with unicode characters fail to load.

    ### Expected Behavior
    Configuration should load successfully with unicode characters.

    ### Actual Behavior
    UnicodeDecodeError when loading config.yaml with unicode characters.

    ### Steps to Reproduce
    1. Create config.yaml with unicode characters: "name: José"
    2. Run application with Settings().get('name')
    3. Error occurs

    ### Error Message
    ```
    UnicodeDecodeError: 'ascii' codec can't decode byte 0xc3 in position 6: ordinal not in range(128)
    ```

Feature Requests
----------------

**Good Feature Requests Include:**

- Clear use case description
- Proposed API or interface
- Examples of usage
- Consideration of alternatives
- Implementation ideas (if any)

Security Issues
===============

**Responsible Disclosure:**

For security vulnerabilities:

1. **DO NOT** create public issues
2. Email security@dtpyappframework.org
3. Include detailed description
4. Allow reasonable response time
5. Coordinate public disclosure

**Security Review:**

Security-sensitive changes require additional review:

- Authentication and authorization
- Cryptographic operations
- Input validation
- File system operations
- Network communications

Community Guidelines
====================

**Code of Conduct:**

- Be respectful and inclusive
- Welcome newcomers and help them learn
- Focus on constructive feedback
- Assume positive intent
- Follow project guidelines

**Communication:**

- Use clear, professional language
- Provide context and examples
- Ask questions when unclear
- Thank contributors for their time

**Recognition:**

Contributors are recognized through:

- Contributor list in documentation
- Release notes acknowledgments
- GitHub contributor statistics
- Community showcases

Getting Help
============

If you need help contributing:

**Documentation:**
- Read existing documentation thoroughly
- Check examples and API reference

**Discussion:**
- GitHub Discussions for general questions
- Issues for specific bugs or features

**Direct Contact:**
- Project maintainer emails for urgent matters
- Community channels for general support

**Mentoring:**
New contributors can request mentoring for their first contribution.

Thank you for contributing to dtPyAppFramework!