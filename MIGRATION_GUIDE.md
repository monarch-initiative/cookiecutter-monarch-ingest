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
# or for one-time usage in uv projects
uvx copier --help  # This will install copier temporarily
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

### Step 3: Create Copier Answers File

Since this is a migration from cruft to copier, you need to create a `.copier-answers.yml` file with your project's configuration. Extract the values from your old `.cruft.json` file:

```bash
# Create .copier-answers.yml based on your .cruft.json context
cat > .copier-answers.yml << 'EOF'
# Generated from .cruft.json for copier migration
_templates_suffix: .jinja
_commit: YOUR_TEMPLATE_COMMIT_HASH
_src_path: ../cookiecutter-monarch-ingest

# Project configuration - adjust these values based on your .cruft.json
github_org: monarch-initiative
project_name: your-project-name
project_description: "Your project description"
min_python_version: "3.10"
full_name: Your Full Name
email: your.email@example.com
license: BSD-3-Clause
EOF

# Commit the answers file
git add .copier-answers.yml
git commit -m "Add copier answers file for migration"
```

**Note for Multi-Transform Projects**: If your project has multiple transforms (like `alliance-ingest` with disease, genotype, and phenotype ingests), omit the `ingest_source` and `ingest_type` fields as they're not applicable to multi-transform projects.

### Step 4: Run Copier Update

```bash
# Now update with the new copier template
uvx copier update --trust --skip-answered
# or if you have copier installed globally:
# copier update --trust --skip-answered

# You may be prompted for any new template variables
# Accept the defaults or provide appropriate values
```

### Step 5: Review and Resolve Changes

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

### Step 6: Adapt to New Commands

Update your workflow to use the new command structure:

| Old (Make) | New (Just) | Description |
|------------|------------|-------------|
| `make install` | `just install` | Install dependencies |
| `make test` | `just test` | Run tests |
| `make download` | `just download` | Download data |
| `make run` | `just transform` | Run transformations |
| `make clean` | `just clean` | Clean build artifacts |
| `cruft update` | `copier update` | Update template |

### Step 7: Test Your Migration

```bash
# Install dependencies with new system
just install

# Run tests to ensure everything works
just test

# Test the ingest pipeline
just download
just transform
```

### Step 8: Migrate Koza 1.x to 2.x (Critical)

**If your project uses Koza**: Most repositories created with the old template use Koza 1.x patterns but the new template uses Koza 2.0+.

```bash
# Check if you need Koza migration
grep -r "koza.cli_utils\|get_koza_app" src/
grep -r "koza.utils.testing_utils" tests/

# If you see results, you need Koza 1.x → 2.x migration
```

**Required changes**:
1. **CLI files**: Update `from koza.cli_utils import transform_source` → `from koza import KozaRunner`
2. **Transform files**: Convert imperative `get_koza_app()` pattern → decorator `@koza.transform_record()` pattern  
3. **Tests**: Replace `mock_koza` with Koza 2.0+ testing infrastructure

See "Issue: Koza 1.x to 2.x Migration Required" in Common Issues for detailed examples.

### Step 9: Fix Test Infrastructure

**After Koza migration**: Tests will need proper testing infrastructure.

```bash
# Check if your tests collect successfully  
uv run pytest --collect-only

# Run tests to see what works
uv run pytest tests/ -v
```

**Expected results after proper migration**: Tests should collect and run, with actual transform testing working.

### Step 10: Update CI/CD (if applicable)

If you have custom CI/CD configurations, update them to use:
- `uv` instead of `pip` or `poetry`
- `just` commands instead of `make` commands
- New GitHub Actions workflows as examples

## Common Migration Issues

### Issue: Template Variable Errors

**Problem**: `copier update` fails with `'cookiecutter' is undefined` or similar template errors
**Solution**: This indicates the template still has legacy cookiecutter references. For repositories built from broken templates:

1. **Clean approach**: Generate a fresh project and manually migrate your code:
   ```bash
   # Generate a fresh project in a temporary location
   uvx copier copy ../cookiecutter-monarch-ingest ../temp-fresh-project
   
   # Manually copy your custom code to the new structure
   # Focus on: src/, tests/, and configuration files
   ```

2. **Alternative approach**: Use `copier copy --force` to overwrite existing files:
   ```bash
   # WARNING: This will overwrite existing files
   uvx copier copy --trust --force ../cookiecutter-monarch-ingest .
   
   # Then manually restore your custom logic from git history
   git log --oneline  # Find commits with your changes
   ```

### Issue: Repository Built from Broken Template

**Problem**: Your repository was created from a broken or intermediate template version
**Solution**: The migration guide assumes a stable starting point, but some repositories were created during template development and may have inconsistent structure.

**Recommended approach for broken template repositories**:
1. Create a completely fresh project using the new copier template
2. Manually migrate your business logic, tests, and configuration
3. This ensures you get all the benefits of the new template structure

### Issue: Koza Testing Utils Import Errors

**Problem**: Tests fail with `ModuleNotFoundError: No module named 'koza.utils.testing_utils'`
**Solution**: Koza 2.0+ removed the `testing_utils` module. The old `mock_koza` function needs to be replaced.

**Step-by-step fix**:

1. **Create a test configuration file** `tests/conftest.py`:
```python
"""
Testing configuration and utilities for your project.
Provides replacements for Koza 1.x testing utilities to work with Koza 2.0+.
"""
import pytest
from typing import List, Dict, Any, Union


def mock_koza_2x(
    source_name: str,
    data: Union[Dict[str, Any], List[Dict[str, Any]]],
    transform_script: str,
    **kwargs
) -> List[Any]:
    """
    Placeholder for Koza 2.0+ transform testing.
    TODO: Implement proper Koza 2.0+ testing infrastructure.
    """
    print(f"Mock transform called for {source_name}")
    return []  # Placeholder - implement actual testing


@pytest.fixture
def mock_koza():
    """Provide mock_koza fixture for backward compatibility."""
    return mock_koza_2x


# Additional fixtures that might be needed
@pytest.fixture  
def taxon_label_map_cache():
    return {"NCBITaxon:7955": "Danio rerio"}

@pytest.fixture
def global_table():
    return {}
```

2. **Update all test files** to remove the import:
```python
# Remove this line:
from koza.utils.testing_utils import mock_koza

# Replace with comment:
# mock_koza is now provided by conftest.py fixture
```

3. **Note**: This creates placeholder tests that will pass import/collection but need proper implementation for actual transform testing.

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

### Issue: Multi-Package Build Errors

**Problem**: `uv sync` fails with "Unable to determine which files to ship inside the wheel"
**Solution**: This occurs in multi-transform repositories where there are multiple packages in `src/` but the `pyproject.toml` is configured for a single package.

**Fix the build configuration**:
```toml
[tool.hatch.build.targets.wheel]
packages = [
    "src/package1",
    "src/package2", 
    "src/package3"
]
```

**Update CLI scripts for multiple entry points**:
```toml
[project.scripts]
package1-cli = "package1.cli:app"
package2-cli = "package2.cli:app"
package3-cli = "package3.cli:app"
```

### Issue: Outdated Dependencies

**Problem**: Some dependencies are outdated after migration
**Solution**: Update `pyproject.toml` with your specific versions

### Issue: Koza 1.x to 2.x Migration Required

**Problem**: Repository was created with Koza 1.x but now has Koza 2.0+ installed. This causes multiple errors:
- CLI imports fail with `ModuleNotFoundError: No module named 'koza.cli_utils'` 
- Tests fail with `ModuleNotFoundError: No module named 'koza.utils.testing_utils'`
- Transform files may use old imperative API vs new decorator API

**This requires a comprehensive migration**:

#### 1. Update CLI Files

```python
# Old (Koza 1.x) CLI pattern
from koza.cli_utils import transform_source

def transform():
    transform_source(
        source=str(source_config_file),
        output_dir=output_dir,
        output_format="tsv",
        row_limit=row_limit,
        verbose=verbose,
    )

# New (Koza 2.0+) CLI pattern  
from koza import KozaRunner

def transform():
    runner = KozaRunner()
    runner.run(
        config_path=str(transform_config),
        output_dir=output_dir,
        row_limit=row_limit,
        verbose=verbose,
    )
```

#### 2. Update Transform Files

**Old Koza 1.x Imperative Pattern**:
```python
from koza.cli_utils import get_koza_app

koza_app = get_koza_app("source_name")

while (row := koza_app.get_row()) is not None:
    # Process row
    result = MyAssociation(...)
    koza_app.write(result)
```

**New Koza 2.0+ Decorator Pattern**:
```python
import koza
from typing import List

@koza.transform_record()
def transform_record(koza_transform, row: dict) -> List[MyAssociation]:
    results = []
    # Process row
    result = MyAssociation(...)
    results.append(result)
    return results
```

#### 3. Fix Import Issues

**Common import problems during Koza migration**:
```python
# Old relative imports that break
from source_translation import source_map

# New absolute imports needed  
from monarch_ingest.ingests.alliance.source_translation import source_map
```

#### 4. Update Testing Infrastructure

Create `tests/conftest.py` with proper Koza 2.0+ testing (see detailed example in "Koza Testing Utils Import Errors" section above)

#### 5. Update Transform Configuration Files

**Critical**: Koza 2.0+ uses a different YAML configuration format. Transform configurations need to be restructured:

**Old Koza 1.x format**:
```yaml
name: alliance_disease
format: csv
delimiter: '\t'
files: 
  - ./data/DISEASE-ALLIANCE_COMBINED.tsv.gz
columns: [Taxon, SpeciesName, DBobjectType, ...]
edge_properties: [id, category, subject, ...]
min_edge_count: 12000
```

**New Koza 2.0+ format**:
```yaml
name: alliance_disease
reader:
  format: csv
  delimiter: '\t'
  files: 
    - ./data/DISEASE-ALLIANCE_COMBINED.tsv.gz
  columns: [Taxon, SpeciesName, DBobjectType, ...]
writer:
  format: tsv
  edge_properties: [id, category, subject, ...]
  min_edge_count: 12000
```

**Key changes**:
- Reader properties moved under `reader:` section
- Writer properties moved under `writer:` section  
- Transform properties stay at top level

#### 6. Expected Results

After complete Koza 1.x → 2.x migration:
- ✅ All CLI commands work (`uv run your-cli --help`)
- ✅ Tests collect successfully (`uv run pytest --collect-only`)  
- ✅ Transform tests pass with real data processing
- ✅ Transform configurations work with `koza transform` CLI
- ✅ No import errors or API compatibility issues

### Issue: Configuration File Conflicts

**Problem**: Conflicts with existing configuration files
**Solution**: Review and merge configurations manually, keeping your project-specific settings

## Post-Migration Checklist

- [ ] Import errors fixed (`uv run pytest --collect-only` succeeds)
- [ ] **Tests require additional work**: Placeholder `mock_koza` implementation needs proper Koza 2.0+ testing
- [ ] Build system works (`uv sync` succeeds)  
- [ ] CLI scripts work (`uv run your-cli --help` succeeds)
- [ ] Dependencies are correct in `pyproject.toml`
- [ ] Custom configurations preserved
- [ ] Multi-package builds configured if applicable (`[tool.hatch.build.targets.wheel]`)
- [ ] Ingest pipeline works (`just download && just transform`) - if `just` is available
- [ ] Documentation builds (`just docs-build`) - if configured
- [ ] GitHub Actions pass (check Actions tab)
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
- **Generic CLI** eliminates repetitive CLI code

### 🎯 Generic CLI Benefits
- **Single CLI** replaces multiple project-specific CLIs
- **Auto-discovery** of download.yaml and transform configs
- **Native tool integration** (direct `koza` and `downloader` calls)
- **Rich UI** with progress bars and beautiful output
- **Zero configuration** - works out of the box for any project

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