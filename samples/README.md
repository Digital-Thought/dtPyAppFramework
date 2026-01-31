# dtPyAppFramework Samples

Welcome to the dtPyAppFramework samples directory! This collection of examples demonstrates various features and use cases of the framework to help you get started quickly.

## Available Samples

### [Simple App](./simple_app/)
**Basic application demonstrating core framework features**

- **Purpose**: Introduction to dtPyAppFramework fundamentals and development mode
- **Key Features**: Basic application structure, settings management, development mode
- **Technologies**: Core framework features, configuration, logging
- **Difficulty**: Beginner
- **Files**:
  - [`dev_app.py`](./simple_app/dev_app.py) - Simple one-shot application
  - [`daemon_app.py`](./simple_app/daemon_app.py) - Long-running daemon application

**When to use**: Learning the framework, prototyping, development and testing

---

### [AppContext](./app_context/) (v4.0.4+)
**Demonstrates the AppContext unified facade for framework components**

- **Purpose**: Show how AppContext provides a single access point for metadata, paths, settings, secrets, and resources
- **Key Features**: `AppContext` singleton, metadata access, path resolution, settings and secrets convenience methods
- **Technologies**: Core framework features
- **Difficulty**: Beginner
- **Files**:
  - [`app_context_app.py`](./app_context/app_context_app.py) - Main application demonstrating all AppContext features
  - [`config/config.yaml`](./app_context/config/config.yaml) - Sample configuration

**When to use**: When you want a clean, unified interface to access framework components without importing multiple singletons

---

### [Metadata Auto-Discovery](./metadata_discovery/) (v4.0.4+)
**Demonstrates auto-discovery of application metadata from text files**

- **Purpose**: Show how AbstractApp can load version, name, and description from text files instead of constructor arguments
- **Key Features**: Metadata text files (`_version.txt`, `_short_name.txt`, `_full_name.txt`, `_description.txt`), zero-argument construction
- **Technologies**: Core framework features, Python packaging conventions
- **Difficulty**: Beginner
- **Files**:
  - [`metadata_discovery_app/app.py`](./metadata_discovery/metadata_discovery_app/app.py) - Application with auto-discovered metadata
  - [`metadata_discovery_app/_version.txt`](./metadata_discovery/metadata_discovery_app/_version.txt) - Version file
  - [`metadata_discovery_app/_short_name.txt`](./metadata_discovery/metadata_discovery_app/_short_name.txt) - Short name file
  - [`metadata_discovery_app/_full_name.txt`](./metadata_discovery/metadata_discovery_app/_full_name.txt) - Full name file
  - [`metadata_discovery_app/_description.txt`](./metadata_discovery/metadata_discovery_app/_description.txt) - Description file

**When to use**: Structuring applications as installable Python packages, managing metadata in text files for CI/CD integration

---

### [Container Mode](./container_mode/)
**Demonstrates containerised application deployment with simplified directory structure**

- **Purpose**: Show how to run dtPyAppFramework applications in Docker, Kubernetes, and other container environments
- **Key Features**: Container mode (`--container`), simplified directory structure, single configuration layer
- **Technologies**: Docker, Kubernetes, container orchestration
- **Difficulty**: Intermediate
- **Files**:
  - [`container_app.py`](./container_mode/container_app.py) - Main application demonstrating container features
  - [`config/config.yaml`](./container_mode/config/config.yaml) - Sample configuration
  - [`Dockerfile`](./container_mode/Dockerfile) - Docker container example
  - [`k8s-deployment.yaml`](./container_mode/k8s-deployment.yaml) - Kubernetes deployment

**When to use**: Deploying applications in containerised environments, microservices architecture, cloud-native applications

---

### [Multiprocessing](./multiprocessing/)
**Demonstrates advanced multiprocessing capabilities and task management**

- **Purpose**: Show how to use the framework's multiprocessing features for parallel task execution
- **Key Features**: Process spawning, task coordination, nested logging, worker management
- **Technologies**: Python multiprocessing, process pools, task queues
- **Difficulty**: Advanced
- **Files**:
  - [`multiprocessing_app.py`](./multiprocessing/multiprocessing_app.py) - Multiprocessing demonstration

**When to use**: CPU-intensive tasks, parallel processing, background job processing

---

### [Password Keystore](./password_keystore/) (v4.0.3+)
**Demonstrates portable keystores using the --password argument**

- **Purpose**: Show how the same keystore can be accessed from different locations using a password
- **Key Features**: `--password` CLI argument, container mode, portable keystores
- **Technologies**: Password-based keystore encryption, container deployments
- **Difficulty**: Intermediate
- **Files**:
  - [`create_keystore.py`](./password_keystore/create_keystore.py) - Create a keystore with a password
  - [`access_keystore.py`](./password_keystore/access_keystore.py) - Access keystore from different location

**When to use**: Sharing keystores between containers, portable keystore deployments

---

### [Concurrent Keystore](./concurrent_keystore/) (v4.0.1+)
**Demonstrates concurrent multi-process access to a shared keystore**

- **Purpose**: Verify that file locking prevents race conditions when multiple processes access the same keystore
- **Key Features**: File locking, atomic writes, multi-process safety, stress testing
- **Technologies**: `filelock` library, multiprocessing, concurrent access patterns
- **Difficulty**: Advanced
- **Files**:
  - [`concurrent_access.py`](./concurrent_keystore/concurrent_access.py) - Basic concurrent access test
  - [`stress_test.py`](./concurrent_keystore/stress_test.py) - Intensive stress test

**When to use**: Validating keystore safety in multi-container/multi-process deployments

## Getting Started

### Prerequisites

1. **Install dtPyAppFramework and dependencies**:
   ```bash
   # From the project root directory
   pip install -r requirements.txt

   # Or install in development mode (recommended)
   pip install -e .
   ```

   The main `requirements.txt` includes all core dependencies:
   - PyYAML~=6.0.2 (configuration)
   - psutil~=6.1.0 (process management)
   - cryptography~=44.0.0 (secrets encryption)
   - And other framework dependencies...

### Running Samples

Each sample can be run independently from its directory:

```bash
# Navigate to a sample directory
cd samples/container_mode

# Run the sample
python container_app.py --help

# Run with specific features
python container_app.py --container --demo-mode
```

### Sample Structure

Each sample follows this structure:
```
sample_name/
├── README.md           # Detailed documentation
├── main_app.py         # Primary application file
├── config/             # Configuration files (if applicable)
├── docker/             # Docker-related files (if applicable)
├── k8s/               # Kubernetes files (if applicable)
└── requirements.txt    # Sample-specific dependencies (if any)
```

## Learning Path

### 1. **Start Here: Simple App**
Learn the basics of dtPyAppFramework:
- Application structure with `AbstractApp`
- Configuration management
- Settings and secrets
- Development mode

### 2. **Unified Access: AppContext**
Learn the unified facade pattern:
- Access metadata, paths, settings, and secrets from a single object
- Simplify imports across your application
- Understand the `AppContext` singleton lifecycle

### 3. **Package Metadata: Metadata Auto-Discovery**
Learn file-based metadata management:
- Store version, name, and description in text files
- Eliminate constructor boilerplate
- Align with Python packaging conventions and CI/CD pipelines

### 4. **Production Ready: Container Mode**
Understand production deployment:
- Container mode setup
- Simplified directory structure
- Docker and Kubernetes deployment
- Environment-specific configuration

### 5. **Advanced Features: Multiprocessing**
Explore powerful capabilities:
- Parallel processing
- Task coordination
- Advanced logging
- Process management

### 6. **Container Secrets: Password Keystore**
Learn portable keystore patterns:
- `--password` CLI argument
- Shared keystores across containers
- Container mode encryption

### 7. **Enterprise Ready: Concurrent Keystore**
Understand multi-process safety:
- File locking mechanisms
- Concurrent access patterns
- Stress testing strategies

## Framework Features by Sample

| Feature | Simple App | AppContext | Metadata Discovery | Container Mode | Multiprocessing | Password Keystore | Concurrent Keystore |
|---------|------------|-----------|-------------------|----------------|-----------------|-------------------|---------------------|
| **Basic Application Structure** | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| **Configuration Management** | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| **Secrets Management** | Yes | Yes | -- | Yes | Yes | Yes | Yes |
| **Logging System** | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| **AppContext Facade** | -- | Yes | Yes | -- | -- | -- | -- |
| **Metadata Auto-Discovery** | -- | -- | Yes | -- | -- | -- | -- |
| **Container Mode** | -- | -- | -- | Yes | -- | Yes | Yes |
| **Docker/Kubernetes** | -- | Yes | -- | Yes | -- | Yes | Yes |
| **Multiprocessing** | -- | -- | -- | -- | Yes | -- | Yes |
| **Task Management** | -- | -- | -- | -- | Yes | -- | -- |
| **Development Mode** | Yes | Yes | Yes | Yes | Yes | -- | -- |
| **Resource Management** | Basic | Yes | -- | Yes | Yes | -- | -- |
| **--password Argument** | -- | -- | -- | -- | -- | Yes | Yes |
| **File Locking** | -- | -- | -- | -- | -- | -- | Yes |

## Containerisation Guide

### Docker Quick Start
```bash
# From any sample directory with a Dockerfile
docker build -t sample-app .
docker run --rm sample-app
```

### Kubernetes Quick Start
```bash
# From any sample with k8s files
kubectl apply -f k8s-deployment.yaml
kubectl logs -f deployment/sample-app
```

## Development Tips

### Running in Development Mode
```bash
# Enable development mode for any sample
export DEV_MODE=true
python sample_app.py
```

### Container Mode Testing
```bash
# Test container mode locally
python sample_app.py --container --demo-mode

# Compare with standard mode
python sample_app.py --demo-mode
```

### Debugging
```bash
# Enable debug logging
python sample_app.py --console
```

## Documentation

- **[Framework Documentation](../docs/)** - Complete framework documentation
- **[Getting Started Guide](../docs/guides/getting-started.rst)** - Framework introduction
- **[Configuration Guide](../docs/components/configuration.rst)** - Configuration management
- **[Application Framework](../docs/components/application.rst)** - Container mode and application details
- **[API Reference](../docs/api/)** - Detailed API documentation

## Contributing Samples

We welcome contributions of new samples! To add a sample:

1. **Create a new directory** under `samples/`
2. **Follow the sample structure** shown above
3. **Include comprehensive README.md** with:
   - Purpose and key features
   - Prerequisites and setup
   - Usage examples
   - Troubleshooting guide
4. **Test thoroughly** in multiple environments
5. **Update this README.md** to include your sample

### Sample Guidelines

- **Self-contained**: Each sample should run independently
- **Well-documented**: Clear README with examples
- **Production-ready**: Show best practices
- **Cross-platform**: Work on Windows, macOS, and Linux
- **Container-friendly**: Support container deployment when applicable

## Support

- **Issues**: [GitHub Issues](https://github.com/Digital-Thought/dtPyAppFramework/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Digital-Thought/dtPyAppFramework/discussions)
- **Documentation**: [Framework Docs](../docs/)

## Licence

All samples are part of dtPyAppFramework and follow the same licence terms as the main project.
