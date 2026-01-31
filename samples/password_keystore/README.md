# Password Keystore Sample

This sample demonstrates the `--password` argument feature introduced in v4.0.3, which allows you to set the `KEYSTORE_PASSWORD` environment variable from the command line.

## Purpose

When running in `CONTAINER_MODE`, dtPyAppFramework uses the `KEYSTORE_PASSWORD` directly (without system fingerprint mixing) to encrypt/decrypt the keystore. This means the same keystore file can be accessed from different locations (e.g., different containers) as long as the same password is provided.

## Sample Structure

```
password_keystore/
├── create_keystore.py   # Step 1: Create a keystore with a password
├── access_keystore.py   # Step 2: Access the keystore from a different location
├── location_a/          # Created automatically - simulates first container
│   └── data/
│       └── keystore/
│           └── create_keystore.v3keystore
└── location_b/          # Created automatically - simulates second container
    └── data/
        └── keystore/
            └── access_keystore.v3keystore (copied from location_a)
```

## How to Run

### Step 1: Create a Keystore

```bash
cd samples/password_keystore
python create_keystore.py --password "my_secure_password_123"
```

This will:
- Create a keystore in `./location_a/data/keystore/`
- Store a test secret called `test_secret`
- Store a timestamp to prove keystore identity

### Step 2: Access from a Different Location

```bash
python access_keystore.py --password "my_secure_password_123"
```

This will:
- Automatically copy the keystore from `location_a` to `location_b`
- Access the keystore using the provided password
- Retrieve and display the test secret

### Expected Output

If successful, you should see:
```
SECRET RETRIEVED SUCCESSFULLY
============================================================

Secret name: test_secret
Secret value: Hello from password_keystore sample!

Keystore creation timestamp: 2025-12-18T...

This proves the same keystore is being accessed!
```

## Key Points Demonstrated

1. **--password Argument**: The password is passed via command line, not environment variable
2. **Container Mode**: Both scripts enable `CONTAINER_MODE` to use direct password access
3. **Portable Keystores**: The same keystore file works across different locations
4. **Password Consistency**: The EXACT same password must be used for both create and access

## Real-World Use Case

In a Kubernetes/Docker environment, you might:
1. Create a keystore during deployment initialisation
2. Store the keystore in a shared volume
3. Multiple worker containers access the same keystore using the password from a Kubernetes Secret

Example Docker Compose:
```yaml
services:
  worker:
    image: myapp
    command: python app.py --password "${KEYSTORE_PASSWORD}"
    volumes:
      - shared_keystore:/app/data/keystore
    deploy:
      replicas: 3
```

## Troubleshooting

### "Secret not found" error
- Ensure you ran `create_keystore.py` first
- Check that the passwords match exactly (case-sensitive)

### "Failed to access keystore" error
- The password is incorrect
- The keystore file wasn't copied properly

### Keystore not created
- Ensure you have write permissions
- Check that `--password` was provided (not required, but recommended for portability)
