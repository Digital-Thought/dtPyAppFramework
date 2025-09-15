# dtPyAppFramework Samples

Welcome to the dtPyAppFramework samples directory! This collection of examples demonstrates various features and use cases of the framework to help you get started quickly.

## 📋 Available Samples

### 🐳 [Container Mode](./container_mode/)
**Demonstrates containerized application deployment with simplified directory structure**

- **Purpose**: Show how to run dtPyAppFramework applications in Docker, Kubernetes, and other container environments
- **Key Features**: Container mode (`--container`), simplified directory structure, single configuration layer
- **Technologies**: Docker, Kubernetes, container orchestration
- **Difficulty**: Intermediate
- **Files**: 
  - [`container_app.py`](./container_mode/container_app.py) - Main application demonstrating container features
  - [`config/config.yaml`](./container_mode/config/config.yaml) - Sample configuration
  - [`Dockerfile`](./container_mode/Dockerfile) - Docker container example
  - [`k8s-deployment.yaml`](./container_mode/k8s-deployment.yaml) - Kubernetes deployment

**When to use**: Deploying applications in containerized environments, microservices architecture, cloud-native applications

---

### 🔄 [Multiprocessing](./multiprocessing/)
**Demonstrates advanced multiprocessing capabilities and task management**

- **Purpose**: Show how to use the framework's multiprocessing features for parallel task execution
- **Key Features**: Process spawning, task coordination, nested logging, worker management
- **Technologies**: Python multiprocessing, process pools, task queues
- **Difficulty**: Advanced
- **Files**: 
  - [`multiprocessing_app.py`](./multiprocessing/multiprocessing_app.py) - Multiprocessing demonstration

**When to use**: CPU-intensive tasks, parallel processing, background job processing

---

### 📱 [Simple App](./simple_app/)
**Basic application demonstrating core framework features**

- **Purpose**: Introduction to dtPyAppFramework fundamentals and development mode
- **Key Features**: Basic application structure, settings management, development mode
- **Technologies**: Core framework features, configuration, logging
- **Difficulty**: Beginner
- **Files**: 
  - [`dev_app.py`](./simple_app/dev_app.py) - Simple development application

**When to use**: Learning the framework, prototyping, development and testing

## 🚀 Getting Started

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

## 🎯 Learning Path

### 1. **Start Here: Simple App**
Learn the basics of dtPyAppFramework:
- Application structure with `AbstractApp`
- Configuration management
- Settings and secrets
- Development mode

### 2. **Production Ready: Container Mode**
Understand production deployment:
- Container mode setup
- Simplified directory structure
- Docker and Kubernetes deployment
- Environment-specific configuration

### 3. **Advanced Features: Multiprocessing**
Explore powerful capabilities:
- Parallel processing
- Task coordination
- Advanced logging
- Process management

## 🛠️ Framework Features by Sample

| Feature | Simple App | Container Mode | Multiprocessing |
|---------|------------|----------------|-----------------|
| **Basic Application Structure** | ✅ | ✅ | ✅ |
| **Configuration Management** | ✅ | ✅ | ✅ |
| **Secrets Management** | ✅ | ✅ | ✅ |
| **Logging System** | ✅ | ✅ | ✅ |
| **Container Mode** | ❌ | ✅ | ❌ |
| **Docker/Kubernetes** | ❌ | ✅ | ❌ |
| **Multiprocessing** | ❌ | ❌ | ✅ |
| **Task Management** | ❌ | ❌ | ✅ |
| **Development Mode** | ✅ | ✅ | ✅ |
| **Resource Management** | Basic | ✅ | ✅ |

## 🐳 Containerization Guide

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

## 🔧 Development Tips

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

## 📚 Documentation

- **[Framework Documentation](../docs/)** - Complete framework documentation
- **[Getting Started Guide](../docs/guides/getting-started.rst)** - Framework introduction
- **[Configuration Guide](../docs/components/configuration.rst)** - Configuration management
- **[Application Framework](../docs/components/application.rst)** - Container mode and application details
- **[API Reference](../docs/api/)** - Detailed API documentation

## 🤝 Contributing Samples

We welcome contributions of new samples! To add a sample:

1. **Create a new directory** under `samples/`
2. **Follow the sample structure** shown above
3. **Include comprehensive README.md** with:
   - Purpose and key features
   - Prerequisites and setup
   - Usage examples
   - Troubleshooting guide
4. **Test thoroughly** in multiple environments
5. **Update this INDEX.md** to include your sample

### Sample Guidelines

- **Self-contained**: Each sample should run independently
- **Well-documented**: Clear README with examples
- **Production-ready**: Show best practices
- **Cross-platform**: Work on Windows, macOS, and Linux
- **Container-friendly**: Support container deployment when applicable

## ❓ Support

- **Issues**: [GitHub Issues](https://github.com/your-org/dtPyAppFramework/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-org/dtPyAppFramework/discussions)
- **Documentation**: [Framework Docs](../docs/)

## 📄 License

All samples are part of dtPyAppFramework and follow the same license terms as the main project.