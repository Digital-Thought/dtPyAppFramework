# Concurrent Keystore Access Sample

This sample demonstrates the file locking mechanism introduced in v4.0.1, which allows multiple processes to safely access the same keystore file concurrently.

## Purpose

When multiple containers or processes need to share a keystore file, race conditions can cause data corruption. The file locking mechanism prevents this by:

1. **File Locking**: Using `filelock` library for cross-platform file locking
2. **Atomic Writes**: Writing to a temporary file, then atomically renaming
3. **Lock Timeout**: Configurable via `KEYSTORE_LOCK_TIMEOUT` environment variable

## Sample Structure

```
concurrent_keystore/
├── setup_keystore.py      # Initialises the shared keystore
├── worker.py              # Standalone worker (run multiple instances)
├── run_test.py            # Automated test runner (launches workers)
├── concurrent_access.py   # Legacy: spawned workers from single process
├── stress_test.py         # Legacy: intensive stress test
├── README.md
└── data/                  # Created automatically
    └── concurrent_test.v3keystore
```

## How to Run

### Option 1: Manual Multi-Process Test (Recommended)

This approach runs each worker as a completely separate process with its own PID, simulating multiple containers.

**Step 1: Initialise the keystore**
```bash
cd samples/concurrent_keystore
python setup_keystore.py --password "test_password"
```

**Step 2: Run workers in separate terminals**

Open multiple terminal windows and run:
```bash
# Terminal 1
python worker.py --password "test_password" --worker-id 0 --iterations 20

# Terminal 2
python worker.py --password "test_password" --worker-id 1 --iterations 20

# Terminal 3
python worker.py --password "test_password" --worker-id 2 --iterations 20

# Terminal 4
python worker.py --password "test_password" --worker-id 3 --iterations 20
```

Each worker runs as a completely separate application with its own:
- Process ID (PID)
- Memory space
- dtPyAppFramework instance

### Option 2: Automated Test Runner

The test runner automatically launches multiple worker processes:

```bash
python run_test.py --password "test_password" --workers 4 --iterations 10
```

This will:
1. Initialise the shared keystore
2. Launch 4 worker.py processes (each with unique PID)
3. Wait for all workers to complete
4. Verify results and report statistics

### Option 3: Legacy Tests

The original tests spawn workers as child processes from a single parent:

```bash
# Basic concurrent access test
python concurrent_access.py --password "test_password" --workers 4 --iterations 10

# Stress test
python stress_test.py --password "test_password" --workers 8 --iterations 50
```

## Arguments

### setup_keystore.py
| Argument | Description | Default |
|----------|-------------|---------|
| `--password` | Keystore password (required) | - |
| `--max-workers` | Prepare for N workers | 10 |

### worker.py
| Argument | Description | Default |
|----------|-------------|---------|
| `--password` | Keystore password (required) | - |
| `--worker-id` | Unique worker ID (required) | - |
| `--iterations` | Operations to perform | 10 |
| `--delay` | Max random delay (seconds) | 0.01 |

### run_test.py
| Argument | Description | Default |
|----------|-------------|---------|
| `--password` | Keystore password (required) | - |
| `--workers` | Number of worker processes | 4 |
| `--iterations` | Operations per worker | 10 |
| `--delay` | Max random delay (seconds) | 0.01 |

## Expected Output

### Successful Run

```
CONCURRENT KEYSTORE ACCESS TEST
============================================================
Configuration:
  Workers: 4
  Iterations per worker: 10
  Expected total operations: 40

Launching 4 worker processes...
  Started worker 0 (PID: 12345)
  Started worker 1 (PID: 12346)
  Started worker 2 (PID: 12347)
  Started worker 3 (PID: 12348)

Waiting for workers to complete...
  Worker 0 (PID: 12345) completed successfully
  Worker 1 (PID: 12346) completed successfully
  Worker 2 (PID: 12347) completed successfully
  Worker 3 (PID: 12348) completed successfully

============================================================
RESULTS
============================================================
Test duration: 2.34 seconds
Final shared_counter: 40
Expected (if no races): 40

Worker contributions:
  Worker 0 (PID: 12345): 10 operations
  Worker 1 (PID: 12346): 10 operations
  Worker 2 (PID: 12347): 10 operations
  Worker 3 (PID: 12348): 10 operations

============================================================
TEST PASSED: All workers completed successfully!
  - 4 separate processes accessed the same keystore
  - File locking prevented data corruption

COUNTER INTEGRITY: PASSED
  Final counter (40) matches expected (40)
============================================================
```

## Understanding the Results

### Why Separate Processes Matter

Running workers as separate processes (each with unique PID) is more realistic than spawning threads or child functions because:

1. **True Isolation**: Each process has its own memory space
2. **Real File Locking**: Tests actual file lock acquisition across processes
3. **Container Simulation**: Mimics multiple containers accessing shared storage

### Counter Integrity

The test uses a shared counter that each worker increments. Due to the read-modify-write pattern, the final counter may occasionally be less than expected because:

1. Worker A reads counter = 5
2. Worker B reads counter = 5 (before A writes)
3. Worker A writes counter = 6
4. Worker B writes counter = 6 (overwrites A's value)

This is expected behaviour - the file locking prevents **data corruption**, not application-level race conditions. For atomic increment operations, you would need application-level locking.

### What File Locking Prevents

- **Corrupted JSON**: Without locking, partial writes can corrupt the keystore file
- **Lost Updates**: Without atomic writes, one process can overwrite another's changes mid-write
- **HMAC Validation Failures**: Partial writes would cause HMAC verification to fail

## Real-World Use Case

In a Kubernetes deployment with multiple pods accessing a shared PersistentVolume:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-workers
spec:
  replicas: 5
  template:
    spec:
      containers:
        - name: worker
          image: myapp
          command: ["python", "worker.py", "--password", "$(KEYSTORE_PASSWORD)"]
          volumeMounts:
            - name: shared-keystore
              mountPath: /app/data
          env:
            - name: KEYSTORE_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: myapp-secrets
                  key: keystore-password
            - name: KEYSTORE_LOCK_TIMEOUT
              value: "60"
      volumes:
        - name: shared-keystore
          persistentVolumeClaim:
            claimName: shared-keystore-pvc
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `KEYSTORE_PASSWORD` | Password for keystore encryption | Required |
| `KEYSTORE_LOCK_TIMEOUT` | Lock acquisition timeout (seconds) | 30 |
| `CONTAINER_MODE` | Enable container-mode behaviour | Auto-detected |

## Troubleshooting

### Lock Timeout Errors

If you see lock timeout errors:
- Increase `KEYSTORE_LOCK_TIMEOUT` environment variable
- Reduce the number of concurrent workers
- Check for deadlocked processes

### Performance Issues

File locking adds overhead. For high-throughput scenarios:
- Consider using a dedicated secrets manager (AWS Secrets Manager, Azure Key Vault)
- Use read-through caching in your application
- Batch operations where possible

### Verification Failures

If HMAC verification fails:
- Ensure all processes use the same password
- Check for corrupted keystore files (restore from backup)
- Verify file system supports atomic rename operations
