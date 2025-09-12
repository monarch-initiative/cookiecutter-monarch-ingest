# Migration Guide: Cruft → Copier

This guide helps you migrate existing repositories created with the old cookiecutter+cruft template to the new copier-based template.

## Overview

The cookiecutter-monarch-ingest template has been modernized:
- **From**: cookiecutter + cruft
- **To**: copier with enhanced features
- **Benefits**: Better tooling, no templated Python, multi-transform support, AI integration

## Prerequisites

Before starting, ensure you have:
- [copier](https://copier.readthedocs.io/en/stable/installing/) >= 9.4.0 installed
- [uv](https://docs.astral.sh/uv/getting-started/installation/) installed  
- [just](https://just.systems/man/en/) installed (recommended)
- Your existing repository backed up or committed

```bash
pip install copier>=9.4.0
# or
pipx install copier>=9.4.0
```

## Migration Steps

### Step 1: Backup Your Current State

```bash
# Commit any outstanding changes
git add .
git commit -m "Pre-migration backup"

# Create a backup branch (optional but recommended)
git checkout -b backup-before-copier-migration
git checkout main  # or your main branch
```

### Step 2: Remove Cruft Configuration

```bash
# Remove the cruft tracking file
rm .cruft.json

# Commit this change
git add .cruft.json
git commit -m "Remove cruft configuration for copier migration"
```

### Step 3: Run Copier Update

```bash
# Update with the new copier template
copier update --trust --skip-answered

# You'll be prompted for any new template variables
# Accept the defaults or provide appropriate values
```

### Step 4: Review and Resolve Changes

The migration will update several areas:

#### Build System Changes
- **Makefile** → **justfile**: Review the new justfile commands
- **pyproject.toml**: Updated for uv and modern Python packaging
- **Dependencies**: Moved to dependency groups format

#### Configuration Files Added
- `.editorconfig`: Editor configuration
- `.yamllint.yaml`: YAML linting rules  
- `mypy.ini`: Type checking configuration
- `pytest.ini`: Test configuration
- `.pre-commit-config.yaml`: Updated pre-commit hooks

#### GitHub Workflows Updated
- Old workflows → `main.yaml` (test/build/deploy)
- Added `ai.yml` for Dragon AI Agent integration
- Updated to use uv instead of pip/poetry

#### Documentation Updated
- Enhanced README with copier instructions
- Added `CLAUDE.md` for AI assistant integration
- Updated CONTRIBUTING.md for new workflows

### Step 5: Adapt to New Commands

Update your workflow to use the new command structure:

| Old (Make) | New (Just) | Description |
|------------|------------|-------------|
| `make install` | `just install` | Install dependencies |
| `make test` | `just test` | Run tests |
| `make download` | `just download` | Download data |
| `make run` | `just transform` | Run transformations |
| `make clean` | `just clean` | Clean build artifacts |
| `cruft update` | `copier update` | Update template |

### Step 6: Test Your Migration

```bash
# Install dependencies with new system
just install

# Run tests to ensure everything works
just test

# Test the ingest pipeline
just download
just transform
```

### Step 7: Update CI/CD (if applicable)

If you have custom CI/CD configurations, update them to use:
- `uv` instead of `pip` or `poetry`
- `just` commands instead of `make` commands
- New GitHub Actions workflows as examples

## Common Migration Issues

### Issue: Import Errors in Tests

**Problem**: Tests fail due to changed import paths
**Solution**: The new template uses dynamic discovery - tests should work automatically, but check for any hardcoded import paths

### Issue: Custom Makefile Rules

**Problem**: You had custom rules in your Makefile
**Solution**: Add custom rules to `project.justfile` (which is imported by the main justfile)

```bash
# Add to project.justfile
my-custom-command:
    echo "My custom command"
```

### Issue: Outdated Dependencies

**Problem**: Some dependencies are outdated after migration
**Solution**: Update `pyproject.toml` with your specific versions

### Issue: Configuration File Conflicts

**Problem**: Conflicts with existing configuration files
**Solution**: Review and merge configurations manually, keeping your project-specific settings

## Post-Migration Checklist

- [ ] All tests pass (`just test`)
- [ ] Ingest pipeline works (`just download && just transform`)
- [ ] Documentation builds (`just docs-build`)
- [ ] GitHub Actions pass (check Actions tab)
- [ ] Dependencies are correct in `pyproject.toml`
- [ ] Custom configurations preserved
- [ ] Team members updated on new commands

## Key Benefits After Migration

### 🐍 No More Templated Python
- All Python files use standard syntax
- Better IDE support and debugging
- Easier code review and maintenance

### 🚀 Modern Tooling
- **uv**: Fast dependency management
- **justfile**: Better task runner than make
- **copier**: Advanced templating with validation

### 🔄 Multi-Transform Support
- Architecture ready for multiple transforms
- Dynamic discovery of transform modules
- Auto-detection of output files

### 🤖 AI Integration
- Dragon AI Agent for automated assistance
- Enhanced CLAUDE.md instructions
- GitHub Actions AI workflows

### 📦 Improved Packaging
- Modern pyproject.toml configuration
- uv-dynamic-versioning for releases
- Dependency groups instead of extras

## Troubleshooting

### Getting Help

1. **Check the logs**: Look at copier output for specific errors
2. **Review conflicts**: Use `git status` to see what needs attention
3. **Compare with template**: Look at a fresh template generation for reference
4. **Ask for help**: Open an issue in the cookiecutter-monarch-ingest repository

### Rollback Process

If migration fails, you can rollback:

```bash
# Reset to pre-migration state
git reset --hard HEAD~2  # Adjust number based on commits

# Or switch to backup branch
git checkout backup-before-copier-migration
```

### Advanced Migration

For complex repositories with many customizations:

1. **Create a fresh template**: Generate a new project with copier
2. **Manual migration**: Copy your custom code to the new structure
3. **Incremental approach**: Migrate components one at a time

## Future Updates

After migration, keep your template up to date:

```bash
# Update template (instead of cruft update)
copier update

# Check for conflicts and resolve
git status
```

## Support

- **Documentation**: [Copier Documentation](https://copier.readthedocs.io/)
- **Issues**: [cookiecutter-monarch-ingest Issues](https://github.com/monarch-initiative/cookiecutter-monarch-ingest/issues)
- **Template Repository**: [cookiecutter-monarch-ingest](https://github.com/monarch-initiative/cookiecutter-monarch-ingest)

---

**Note**: This is a one-time migration. Once completed, you'll use `copier update` instead of `cruft update` for future template updates.