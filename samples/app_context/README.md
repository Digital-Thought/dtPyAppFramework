# AppContext Sample

Demonstrates the `AppContext` singleton, a unified facade providing convenient access to all framework components from a single object.

## What is AppContext?

Instead of importing and using individual singletons (`Settings`, `ApplicationPaths`, `ResourceManager`, etc.), `AppContext` wraps them all behind a clean interface:

```python
from dtPyAppFramework.app_context import AppContext

ctx = AppContext()

# Metadata
print(ctx.version)
print(ctx.full_name)

# Paths
print(ctx.logging_path)
print(ctx.app_data_path)

# Settings
value = ctx.get_setting('app.timeout', 30)
ctx.set_setting('app.name', 'MyApp')

# Secrets
ctx.set_secret('api_key', 'sk-12345')
secret = ctx.get_secret('api_key')
ctx.delete_secret('api_key')

# Config files
for path in ctx.config_file_paths:
    print(path)
```

## Features Demonstrated

| Feature | Method / Property |
|---------|-------------------|
| Version | `ctx.version` |
| Full name | `ctx.full_name` |
| Short name | `ctx.short_name` |
| Description | `ctx.description` |
| Logging path | `ctx.logging_path` |
| App data path | `ctx.app_data_path` |
| User data path | `ctx.usr_data_path` |
| Temp path | `ctx.tmp_path` |
| Config file list | `ctx.config_file_paths` |
| Get setting | `ctx.get_setting(key, default)` |
| Set setting | `ctx.set_setting(key, value)` |
| Get secret | `ctx.get_secret(key, default)` |
| Set secret | `ctx.set_secret(key, value)` |
| Delete secret | `ctx.delete_secret(key)` |
| Resource lookup | `ctx.get_resource_path(name)` |

## Running

```bash
cd samples/app_context

# Run all demonstrations
python app_context_app.py

# Run a specific section
python app_context_app.py --task metadata
python app_context_app.py --task paths
python app_context_app.py --task settings
python app_context_app.py --task secrets
```

## Key Points

- `AppContext` is a **singleton** -- calling `AppContext()` always returns the same instance
- It is **automatically initialised** by the framework during application startup
- It delegates to the existing framework singletons (`Settings`, `ApplicationPaths`, `ResourceManager`) -- no duplication
- Useful when you need quick access to multiple framework components without multiple imports

## Difficulty

Beginner -- start here if you want to understand the framework's unified access pattern.
