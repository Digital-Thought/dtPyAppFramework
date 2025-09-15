# dtPyAppFramework

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)

**dtPyAppFramework** is a comprehensive Python framework library designed as the foundation for creating robust Python applications. It provides enterprise-grade features including layered configuration management, multi-cloud secrets storage, advanced multi-processing task management, sophisticated logging with nested support for spawned processes, singleton pattern utilities, and application path management.

## 🚀 Key Features

- **🐳 Container Mode:** Full containerization support with `--container` flag for Docker, Kubernetes, and container orchestration
- **⚙️ Layered Configuration:** Multi-tier configuration system with working directory, user, and system-level settings
- **🔐 Multi-Cloud Secrets:** Seamless integration with AWS Secrets Manager, Azure Key Vault, and local encrypted storage
- **📱 AbstractApp Foundation:** Complete application framework with command-line parsing, logging, and lifecycle management
- **🔄 Advanced Multiprocessing:** Process spawning, task coordination, and nested logging for parallel execution
- **📝 Sophisticated Logging:** Cross-process synchronized logging with color coding and automatic rotation
- **🛡️ Security Framework:** Comprehensive validation, encryption, and secure file handling
- **📁 Path Management:** Automatic application directory structure and resource management
- **🔧 Singleton Utilities:** Thread-safe singleton pattern implementation with parameter support

## 📦 Installation

### From PyPI (Future)
```bash
pip install dtPyAppFramework
```

### Development Installation
```bash
# Clone the repository
git clone <repository-url>
cd dtPyAppFramework

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e .
```

## 🏁 Quick Start

### Basic Application
Create a simple application using the AbstractApp foundation:

```python
from dtPyAppFramework.application import AbstractApp
import logging

class MyApplication(AbstractApp):
    def define_args(self, arg_parser):
        """Define custom command-line arguments"""
        arg_parser.add_argument('--task', default='hello', 
                              help='Task to perform')

    def main(self, args):
        """Main application logic"""
        logging.info(f"Running task: {args.task}")
        
        # Access configuration
        app_name = self.settings.get('app.name', 'MyApp')
        logging.info(f"Application: {app_name}")
        
        # Your application logic here
        
# Create and run the application
if __name__ == "__main__":
    app = MyApplication(
        description="My Sample Application",
        version="1.0.0",
        short_name="my-app",
        full_name="My Sample Application",
        console_app=True
    )
    app.run()
```

### Container Mode
For containerized deployments (Docker, Kubernetes):

```python
# Enable container mode with simplified directory structure
app.run()  # Use --container flag or set CONTAINER_MODE=true

# Or detect container environment automatically
if os.path.exists('/.dockerenv'):
    os.environ['CONTAINER_MODE'] = 'True'
```

## 🔧 Core Framework Components

### 🐳 Container Mode
Full support for containerized deployments with simplified directory structure:
- **Simplified Paths**: All directories (`config/`, `data/`, `logs/`, `temp/`) in working directory
- **Single Config Layer**: No multi-tier configuration in container mode
- **Environment Detection**: Automatic detection of Docker/Kubernetes environments
- **Volume Mounting**: Designed for persistent volume mounting

```bash
# Enable container mode
python app.py --container
# or
export CONTAINER_MODE=true && python app.py
```

### ⚙️ Layered Configuration Management
Multi-tier configuration system with automatic merging:
- **Working Directory**: `./config/config.yaml`
- **User Level**: User-specific configurations
- **System Level**: System-wide configurations (standard mode only)

```yaml
# config.yaml example
app:
  name: "MyApp"
  debug: false
secrets:
  azure:
    vault_url: "https://vault.vault.azure.net/"
logging:
  level: "INFO"
  console_colors: true
```

### 🔐 Multi-Cloud Secrets Management
Unified interface for multiple secret storage backends:
- **AWS Secrets Manager**: Full boto3 integration
- **Azure Key Vault**: azure-keyvault-secrets support
- **Local Encrypted Storage**: cryptography-based local secrets
- **Environment Variables**: SEC/ prefix resolution

```python
# Usage example
settings = Settings()
api_key = settings.get('SEC/api_key', 'default-key')
settings.secret_manager.set_secret('db_password', 'secret123')
```

### 📝 Advanced Logging System
Sophisticated logging with cross-process support:
- **Nested Logging**: Each spawned process gets its own namespace
- **Color Coding**: Console output with colorlog integration
- **Log Rotation**: Automatic file rotation and management
- **Cross-Process Sync**: Synchronized logging between parent/child processes

### 🔄 Multiprocessing Framework
Advanced process management and task coordination:
- **Process Spawning**: Managed subprocess creation with psutil
- **Task Coordination**: Process pool management and task distribution
- **Resource Monitoring**: Memory and CPU usage tracking
- **Cleanup Handling**: Automatic process cleanup and resource management

### 🛡️ Security Features
Comprehensive security framework:
- **File Validation**: Secure file operations and path validation
- **Encryption**: Local secret encryption with cryptography
- **Access Control**: Platform-specific permission handling
- **Error Handling**: Secure error reporting without information leakage

## 📚 Samples and Examples

Comprehensive samples are available in the `./samples/` directory:

- **[Container Mode](./samples/container_mode/)** - Complete Docker/Kubernetes example with deployment files
- **[Simple App](./samples/simple_app/)** - Basic application structure and development mode
- **[Multiprocessing](./samples/multiprocessing/)** - Advanced parallel processing examples

Each sample includes detailed README documentation with setup instructions, usage examples, and best practices.

## 🏗️ Project Structure

```
dtPyAppFramework/
├── src/
│   └── dtPyAppFramework/           # Main framework source
│       ├── application.py          # AbstractApp base class
│       ├── paths/                  # Application path management
│       ├── settings/               # Configuration and secrets
│       ├── security/               # Security framework
│       ├── logging/                # Advanced logging system
│       ├── decorators/             # Singleton and utilities
│       ├── process/                # Multiprocessing framework
│       └── resources/              # Resource management
├── samples/                        # Usage examples
├── tests/                          # Comprehensive test suite
├── docs/                           # Documentation (RST format)
└── requirements.txt                # Core dependencies
```

## 🔧 Development

### Running Tests
```bash
# Run full test suite
pytest

# Run with coverage
pytest --cov=src/dtPyAppFramework

# Watch mode for development
pytest-watch
```

### Core Dependencies
```
PyYAML~=6.0.2                     # Configuration parsing
colorlog~=6.9.0                   # Console color coding
psutil~=6.1.0                     # Process management
cryptography~=44.0.0              # Local encryption
boto3~=1.35.54                    # AWS integration
azure-identity                    # Azure authentication
azure-keyvault-secrets            # Azure Key Vault
pytest~=8.3.3                     # Testing framework
InquirerPy                        # Interactive CLI prompts
```

## 📖 Documentation

- **[Getting Started](./docs/guides/getting-started.rst)** - Framework introduction and basic usage
- **[Application Framework](./docs/components/application.rst)** - Container mode and application lifecycle
- **[Configuration Management](./docs/components/configuration.rst)** - Settings and layered config
- **[Secrets Management](./docs/components/secrets-management.rst)** - Multi-cloud secret handling
- **[API Reference](./docs/api/)** - Complete API documentation

## 🤝 Contributing

We welcome contributions! Please see our contributing guidelines for:

- Code style and standards (Python 3.12+)
- Testing requirements (pytest with full coverage)
- Documentation standards (RST format)
- Sample creation guidelines

## 📄 License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).

## 📧 Support

For questions, bug reports, or feature requests:
- **Issues**: [GitHub Issues](https://github.com/your-org/dtPyAppFramework/issues)
- **Email**: [dev@digital-thought.org](mailto:dev@digital-thought.org)