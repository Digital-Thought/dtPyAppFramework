# Container Mode Sample

This sample demonstrates how to use dtPyAppFramework in container environments (Docker, Kubernetes, etc.) with the simplified directory structure provided by container mode.

## 🎯 What This Sample Demonstrates

- **Container Mode Activation**: Using `--container` flag and `CONTAINER_MODE` environment variable
- **Simplified Directory Structure**: Single config directory, unified data directory
- **Configuration Management**: Single-layer configuration vs multi-layer standard mode
- **Secrets Management**: Container-safe secret handling
- **Resource Management**: File resources in container environments
- **Logging**: Container-friendly logging setup
- **Auto-Detection**: Automatic container environment detection

## 📁 Directory Ste

### Standard Mode (Default)
```
~/myapp/
├── config/config.yaml           # Working directory config
├── ~/.config/myapp/config.yaml  # User config  
├── /etc/myapp/config.yaml       # System config
├── /var/log/myapp/              # System logs
├── ~/.local/share/myapp/        # User data
└── /tmp/myapp/                  # Temp files
```

### Container Mode (`--container`)
```
/working_directory/
├── config/                      # Single config directory
│   └── config.yaml             # Only configuration file
├── data/                       # Unified data directory
│   ├── keystore/              # Secret storage
│   └── resources/             # Application resources
├── logs/                      # All log files
└── temp/                      # Temporary files
```

## 🚀 Running the Sample

### Prerequisites

The sample uses the main project dependencies from `../../requirements.txt`. To install:

```bash
# From the project root directory
pip install -r requirements.txt

# Or install in development mode
pip install -e .
```

### Method 1: Command Line Flag
```bash
python container_app.py --container
```

### Method 2: Environment Variable
```bash
export CONTAINER_MODE=true
python container_app.py
```

### Method 3: Auto-Detection (Docker/Kubernetes)
The sample automatically detects container environments and enables container mode:
```bash
# Will auto-enable container mode in Docker/Kubernetes
python container_app.py
```

### Optional Arguments
```bash
# Run with extra diagnostic output
python container_app.py --container --demo-mode

# Demonstrate specific functionality
python container_app.py --container --task config
python container_app.py --container --task secrets  
python container_app.py --container --task resources
```

## 🐳 Docker Example

### 1. Use Provided Dockerfile

The sample includes a complete Dockerfile that handles all dependencies:

```bash
# Build from project root to include framework source
docker build -t dtpyapp-container-sample -f samples/container_mode/Dockerfile .
```

The Dockerfile automatically:
- Installs all dependencies from the main `requirements.txt`
- Copies the framework source code
- Sets up the container environment
- Configures proper security (non-root user)
```

### 2. Build and Run
```bash
# Build the container
docker build -t dtpyapp-container-sample .

# Run the container
docker run --rm dtpyapp-container-sample

# Run with custom environment
docker run --rm -e DB_HOST=postgres -e API_KEY=secret123 dtpyapp-container-sample

# Run with volume mounts for persistence
docker run --rm -v $(pwd)/data:/app/data -v $(pwd)/logs:/app/logs dtpyapp-container-sample
```

## ☸️ Kubernetes Example

### Deployment YAML
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: dtpyapp-container-sample
spec:
  replicas: 1
  selector:
    matchLabels:
      app: dtpyapp-container-sample
  template:
    metadata:
      labels:
        app: dtpyapp-container-sample
    spec:
      containers:
      - name: app
        image: dtpyapp-container-sample:latest
        env:
        - name: CONTAINER_MODE
          value: "true"
        - name: DB_HOST
          value: "postgres-service"
        volumeMounts:
        - name: config-volume
          mountPath: /app/config
        - name: data-volume
          mountPath: /app/data
      volumes:
      - name: config-volume
        configMap:
          name: app-config
      - name: data-volume
        persistentVolumeClaim:
          claimName: app-data-pvc
```

### ConfigMap for Configuration
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  config.yaml: |
    app:
      name: "Kubernetes Container Sample"
      debug: false
    database:
      host: "ENV/DB_HOST"
      port: 5432
```

## 🔧 Configuration Examples

### Environment Variables
Container mode supports environment variable resolution in config files:

```yaml
# config/config.yaml
database:
  host: "ENV/DB_HOST"          # Resolves to $DB_HOST
  password: "SEC/db_password"   # Resolves from secrets manager
  
app:
  data_path: "<APP>/data"      # Resolves to application data path
```

### Secret Management

#### Basic Usage
```python
# In your application code
settings = Settings()

# Set secrets (stored in ./data/keystore/)
settings.secret_manager.set_secret('api_key', 'your-secret-key')

# Get secrets with fallback
api_key = settings.get('SEC/api_key', 'default-key')
```

#### Keystore Persistence in Containers
For persistent keystores across container restarts, set a consistent password:

```bash
# Environment variable approach (recommended)
export KEYSTORE_PASSWORD=your-secure-password
# OR
export SECRETS_STORE_PASSWORD=your-secure-password

python container_app.py --container
```

This ensures the keystore uses the same encryption key across container restarts, preventing HMAC verification failures.

### Resource Files
```python
# Store resources in ./data/resources/
resource_manager = ResourceManager()
resource_manager.save_resource('template.json', json_data)

# Load resources
template = resource_manager.load_resource('template.json')
```

## 🧪 Testing the Sample

### Test Standard vs Container Mode
```bash
# Test standard mode
python container_app.py --demo-mode --task all

# Test container mode  
python container_app.py --container --demo-mode --task all

# Compare the output to see the differences
```

### Verify Directory Structure
```bash
# Run with container mode
python container_app.py --container --demo-mode

# Check created directories
ls -la  # Should see: config/, data/, logs/, temp/

# Check config layers
python container_app.py --container --task config
# Should show only 1 configuration layer
```

## 📝 Key Differences: Standard vs Container Mode

| Feature | Standard Mode | Container Mode |
|---------|---------------|----------------|
| **Config Layers** | 3 layers (working dir, user, system) | 1 layer (working dir only) |
| **Data Directory** | Separate user/system data dirs | Single `./data/` directory |
| **Log Location** | System log directories | `./logs/` directory |
| **Temp Files** | System temp directories | `./temp/` directory |
| **Secrets Storage** | User-specific keystore | `./data/keystore/` |
| **Resources** | User/system resource dirs | `./data/resources/` |

## 🔍 Troubleshooting

### Issue: Container mode not detected
**Solution**: Ensure you're using one of these methods:
- Command line: `--container` or `-c`  
- Environment: `CONTAINER_MODE=true`
- Auto-detect: Running in Docker/Kubernetes

### Issue: Permission denied errors
**Solution**: Ensure the container has write permissions to the working directory:
```dockerfile
RUN chmod -R 755 /app
USER appuser  # Run as non-root user
```

### Issue: Configuration not loading
**Solution**: Verify the config file exists:
```bash
# Check if config file exists
ls -la config/config.yaml

# Verify YAML syntax
python -c "import yaml; yaml.safe_load(open('config/config.yaml'))"
```

### Issue: Secrets not persisting between container restarts
**Problem**: Container system fingerprint changes between restarts, causing keystore HMAC failures.

**Solutions**:

**Option 1 (Recommended)**: Use consistent keystore password via environment variable:
```bash
# Set a consistent password for keystore encryption
docker run --rm -e KEYSTORE_PASSWORD=your-secure-password -v $(pwd)/data:/app/data dtpyapp-container-sample

# Or use SECRETS_STORE_PASSWORD (legacy support)
docker run --rm -e SECRETS_STORE_PASSWORD=your-secure-password -v $(pwd)/data:/app/data dtpyapp-container-sample
```

**For Kubernetes**:
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: keystore-password
type: Opaque
stringData:
  password: "your-secure-password"
---
spec:
  containers:
  - name: app
    env:
    - name: KEYSTORE_PASSWORD
      valueFrom:
        secretKeyRef:
          name: keystore-password
          key: password
    volumeMounts:
    - name: data-volume
      mountPath: /app/data
```

**Option 2**: Mount persistent volume AND ensure consistent hostname:
```bash
# Use consistent hostname to stabilize system fingerprint
docker run --rm --hostname myapp-container -v $(pwd)/data:/app/data dtpyapp-container-sample
```

**Important**: Always mount the `/app/data` directory as a volume for any secrets persistence:
```yaml
volumeMounts:
- name: data-volume
  mountPath: /app/data
```

## 📚 Related Documentation

- [Application Framework](../../docs/components/application.rst) - Container mode implementation details
- [Configuration Management](../../docs/components/configuration.rst) - Settings and layered configuration
- [Secrets Management](../../docs/components/secrets-management.rst) - Multi-cloud secret handling
- [Paths and Resources](../../docs/components/paths-resources.rst) - Directory structure and container mode paths
- [Getting Started Guide](../../docs/guides/getting-started.rst) - Framework introduction with container examples

## 🤝 Contributing

To improve this sample:

1. Fork the repository
2. Make your changes to the container_mode sample
3. Test with both Docker and Kubernetes
4. Update this README if needed
5. Submit a pull request

## 📄 License

This sample is part of dtPyAppFramework and follows the same license terms.