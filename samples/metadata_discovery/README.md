# Metadata Auto-Discovery Sample

Demonstrates the framework's ability to auto-discover application metadata from text files, removing the need to pass `version`, `short_name`, `full_name`, and `description` as constructor arguments.

## How It Works

When `AbstractApp.__init__()` is called without one or more metadata arguments, the framework looks for corresponding text files in the subclass's top-level package directory:

| File | Provides |
|------|----------|
| `_version.txt` | `version` |
| `_short_name.txt` | `short_name` |
| `_full_name.txt` | `full_name` |
| `_description.txt` | `description` |

This is the same pattern used by dtPyAppFramework itself to store its own library metadata.

## Project Structure

```
metadata_discovery/
    config/
        config.yaml
    metadata_discovery_app/          <-- Python package
        __init__.py
        app.py                       <-- Application class
        _version.txt                 <-- "1.0.0"
        _short_name.txt              <-- "metadata_demo"
        _full_name.txt               <-- "Metadata Discovery Demo Application"
        _description.txt             <-- "Demonstrates auto-discovery..."
```

## Traditional vs Auto-Discovery

**Traditional (explicit arguments):**
```python
MyApp(
    version="1.0.0",
    short_name="my_app",
    full_name="My Application",
    description="Does things",
    console_app=True
).run()
```

**Auto-discovery (no metadata arguments):**
```python
# Metadata loaded from text files in the package directory
MyApp(console_app=True).run()
```

## Running

```bash
cd samples/metadata_discovery

python -m metadata_discovery_app.app
```

## When to Use This Pattern

- **Installable packages**: When your application is structured as a proper Python package
- **CI/CD pipelines**: When version is managed in a text file and read by build tools
- **Consistency**: When you want metadata in one place, used by both the application and `pyproject.toml` / `setup.py`

## Difficulty

Beginner -- demonstrates a simple but powerful convention for managing application metadata.
