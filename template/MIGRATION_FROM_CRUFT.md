# 🚀 Welcome to the New Copier-Based Template!

Your project has been successfully migrated from the old cookiecutter+cruft template to the new copier-based template.

## What Changed?

### ✨ Template System
- **Cookiecutter + Cruft** → **Copier** with advanced features
- Better conflict resolution and update mechanisms
- Validators and computed values for configuration

### 🐍 Python Files 
- **No more templated Python** - all `.py` files use standard Python syntax
- **Better IDE support** - no more template variables breaking syntax highlighting
- **Dynamic discovery** - project metadata discovered at runtime

### 🛠️ Build System
- **Makefile** → **Justfile** for better task automation
- **pip/poetry** → **uv** for fast dependency management
- **pyproject.toml** updated for modern Python packaging

### 📦 New Commands

| Old Command | New Command | Description |
|-------------|-------------|-------------|
| `make install` | `just install` | Install dependencies |
| `make test` | `just test` | Run tests |
| `make download` | `just download` | Download data |
| `make run` | `just transform` | Run transform |
| `cruft update` | `copier update` | Update template |

## Next Steps

1. **Install new tools** (if not already installed):
   ```bash
   pip install uv
   pip install just
   ```

2. **Try the new commands**:
   ```bash
   just install
   just test
   just download
   just transform
   ```

3. **Update your documentation** to reference new commands

4. **Update CI/CD** if you have custom configurations

## Getting Help

- **Migration issues?** Check the [Migration Guide](https://github.com/monarch-initiative/cookiecutter-monarch-ingest/blob/main/MIGRATION_GUIDE.md)
- **New features?** See the [README](https://github.com/monarch-initiative/cookiecutter-monarch-ingest#readme)
- **Problems?** Open an [issue](https://github.com/monarch-initiative/cookiecutter-monarch-ingest/issues)

## Future Updates

Use the new update command:
```bash
copier update
```

This will keep your project synchronized with the latest template improvements.

---

**You can delete this file after reviewing** - it's just here to help with the migration!