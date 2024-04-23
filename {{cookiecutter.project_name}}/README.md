# {{cookiecutter.project_name}}

{{cookiecutter.project_description}}

## Requirements

- Python >= {{cookiecutter.min_python_version}}
- [Poetry](https://python-poetry.org/docs/#installation)

## Installation

```bash
cd {{cookiecutter.project_name}}
poetry install
```

## Usage

To run the Koza transform for {{cookiecutter.project_name}}:

```bash
poetry run {{cookiecutter.__project_slug}} transform
```

To see available options:

```bash
poetry run {{cookiecutter.__project_slug}} transform --help
```