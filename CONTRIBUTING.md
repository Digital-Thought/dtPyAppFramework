# Contributing to dtPyAppFramework

Welcome, and thank you for your interest in contributing to dtPyAppFramework! This document provides guidelines and information to help you get started.

dtPyAppFramework is a comprehensive Python framework library designed as the foundation for creating robust Python applications. Whether you are fixing a bug, adding a feature, improving documentation, or reporting an issue, your contribution is valued.

Full documentation is available at [https://dtpyappframework.readthedocs.io](https://dtpyappframework.readthedocs.io).

## Code of Conduct

All contributors are expected to adhere to our [Code of Conduct](CODE_OF_CONDUCT.md). Please read it before participating. We are committed to providing a welcoming and inclusive environment for everyone.

## Development Environment Setup

1. **Fork the repository** on GitHub: [Digital-Thought/dtPyAppFramework](https://github.com/Digital-Thought/dtPyAppFramework)

2. **Clone your fork locally:**
   ```bash
   git clone https://github.com/<your-username>/dtPyAppFramework.git
   cd dtPyAppFramework
   ```

3. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   # Linux/macOS
   source venv/bin/activate
   # Windows
   venv\Scripts\activate
   ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

5. **Create a working branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Code Style

- **PEP 8** compliance is required for all Python code.
- **Type hints** are mandatory for all function signatures, including return types.
- **Australian English** must be used in all comments, docstrings, and documentation (e.g. behaviour, organisation, colour, analyse, initialise, centre, defence, licence).
- **Google-style docstrings** are required for all public modules, classes, and functions.

Example:

```python
def analyse_configuration(config_path: str, strict: bool = False) -> dict:
    """Analyse the given configuration file and return parsed settings.

    Reads the configuration file at the specified path, validates its
    structure, and returns the normalised settings dictionary.

    Args:
        config_path: The absolute path to the configuration file.
        strict: If True, raise errors on unrecognised keys.

    Returns:
        A dictionary containing the parsed and validated configuration.

    Raises:
        FileNotFoundError: If the configuration file does not exist.
        ValueError: If the configuration contains invalid values.
    """
    ...
```

## Testing Requirements

All contributions must include appropriate tests.

- **Framework:** [pytest](https://docs.pytest.org/)
- **Minimum coverage:** 80% for all new and modified code.
- **Security-critical functions** (anything in `security/`, secrets handling, encryption, authentication) require **100% test coverage**.
- **Run the test suite:**
  ```bash
  pytest tests/ -v --cov=src
  ```
- Tests must pass on all supported platforms before a pull request will be reviewed.
- Use `pytest-mock` for mocking external services (cloud providers, file system operations, etc.).

## Commit Message Format

All commit messages must follow this format:

```
[TYPE] Brief description of the change
```

**Types:**

| Type         | Usage                                      |
|--------------|--------------------------------------------|
| `FEAT`       | A new feature                              |
| `FIX`        | A bug fix                                  |
| `DOCS`       | Documentation changes only                 |
| `STYLE`      | Code style changes (formatting, no logic)  |
| `REFACTOR`   | Code restructuring without behaviour change|
| `TEST`       | Adding or updating tests                   |
| `SECURITY`   | Security-related changes                   |
| `RELEASE`    | Release preparation and version bumps      |

**Examples:**

```
[FEAT] Add Azure Managed Identity support to secrets manager
[FIX] Resolve race condition in process pool shutdown
[DOCS] Update configuration examples for layered settings
[SECURITY] Upgrade cryptography dependency to address CVE
```

## Branch Strategy

| Branch               | Purpose                                         |
|----------------------|-------------------------------------------------|
| `main`               | Production-ready releases only                  |
| `develop`            | Integration branch for upcoming release         |
| `feature/[name]`     | New features (branch from `develop`)            |
| `fix/[name]`         | Bug fixes (branch from `develop`)               |
| `security/[name]`    | Security fixes (branch from `main` or `develop`)|

- All feature and fix branches should be created from `develop`.
- Security branches may be created from `main` for critical patches.
- Keep branches focused on a single change or closely related set of changes.

## Pull Request Process

1. **Create your branch** from `develop` following the naming conventions above.
2. **Make your changes**, ensuring all code style and testing requirements are met.
3. **Push to your fork** and open a pull request against `develop` on the upstream repository.
4. **Fill in the PR template** completely, including a description of the change, testing performed, and any related issues.
5. **Ensure all CI checks pass**, including tests and linting.
6. **At least one approval** from a maintainer is required before merging.
7. Maintainers may request changes; please address review feedback promptly.

## Reporting Bugs

If you encounter a bug, please report it using the **Bug Report** issue template on GitHub:

[Open a Bug Report](https://github.com/Digital-Thought/dtPyAppFramework/issues/new/choose)

When reporting a bug, please include:

- A clear and descriptive title.
- Steps to reproduce the behaviour.
- Expected behaviour versus actual behaviour.
- Python version, operating system, and dtPyAppFramework version.
- Relevant log output or error messages.

## Feature Requests

We welcome ideas for new features. Please use the **Feature Request** issue template on GitHub:

[Open a Feature Request](https://github.com/Digital-Thought/dtPyAppFramework/issues/new/choose)

Include:

- A clear description of the proposed feature.
- The problem it solves or the use case it addresses.
- Any alternative approaches you have considered.

## Security Issues

**Do NOT create public GitHub issues for security vulnerabilities.**

If you discover a security issue, please report it responsibly:

- **Email:** [dev@digital-thought.org](mailto:dev@digital-thought.org)
- Include a detailed description of the vulnerability and steps to reproduce it.
- See [SECURITY.md](SECURITY.md) for our full security policy and disclosure process.

We will acknowledge receipt within 48 hours and work with you to address the issue before any public disclosure.

## Documentation

- All documentation is written in **RST format** for integration with Sphinx and ReadTheDocs.
- Documentation source files are located in the `docs/` directory.
- Use Australian English throughout all documentation.
- When adding new framework features, include corresponding documentation updates.
- Preview documentation locally by building with Sphinx:
  ```bash
  cd docs
  make html
  ```
- Full published documentation: [https://dtpyappframework.readthedocs.io](https://dtpyappframework.readthedocs.io)

## Licence

By contributing to dtPyAppFramework, you agree that your contributions will be licenced under the [MIT Licence](LICENCE).

---

Thank you for helping improve dtPyAppFramework. If you have any questions, feel free to open a discussion on the [GitHub repository](https://github.com/Digital-Thought/dtPyAppFramework).
