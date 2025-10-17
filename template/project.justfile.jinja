# Ingest-specific recipes

# Clean up build artifacts
clean:
  rm -f `find . -type f -name '*.py[co]' `
  rm -rf `find . -name __pycache__` \
    .venv .ruff_cache .pytest_cache **/.ipynb_checkpoints

# Clean up generated files
clobber: clean
  rm -rf output/
  rm -rf data/

# Run the full ingest pipeline
run: download transform

# Check ingest configuration files
check-config:
  uv run python -c "import yaml; yaml.safe_load(open('src/{{project_slug}}/download.yaml')); print('download.yaml is valid')"
  uv run python -c "import yaml; yaml.safe_load(open('src/{{project_slug}}/transform.yaml')); print('transform.yaml is valid')"
  uv run python -c "import yaml; yaml.safe_load(open('src/{{project_slug}}/metadata.yaml')); print('metadata.yaml is valid')"