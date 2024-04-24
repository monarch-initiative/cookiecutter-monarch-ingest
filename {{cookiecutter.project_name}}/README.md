# {{cookiecutter.project_name}}

{{cookiecutter.project_description}}

## Requirements

- Python >= {{cookiecutter.min_python_version}}
- [Poetry](https://python-poetry.org/docs/#installation)

## Starting a new project

Upon creating a new project from the `cookiecutter-monarch-ingest` template, you can install and test the project:

```bash
cd {{cookiecutter.project_name}}
make install
make test
```

To finish setting up this project:

1. Edit the `download.yaml`, `transform.py`, `transform.yaml`, and `metadata.yaml` files to suit your needs.
   - For more information, see the [Koza documentation](https://koza.monarchinitiative.org) and [kghub-downloader](https://github.com/monarch-initiative/kghub-downloader).
1. Add any additional dependencies to the `pyproject.toml` file.
1. Adjust the contents of the `tests` directory to test the functionality of your transform.
1. Update this `README.md` file with any additional information about the project.
1. Add any appropriate documentation to the `docs` directory.

Once you have completed these steps, you can remove this section from the `README.md` file.

## Installation

```bash
cd {{cookiecutter.project_name}}
make install
# or
poetry install
```

> **Note** that the `make install` command is just a convenience wrapper around `poetry install`.

Once installed, you can check that everything is working as expected:

```bash
# Run the pytest suite
make test
# Download the data and run the Koza transform
make download
make run
```

## Usage

This project is set up with a Makefile for common tasks.  
To see available options:

```bash
make help
```

### Download and Transform

Download the data for the {{cookiecutter.__project_slug}} transform:

```bash
poetry run {{cookiecutter.__project_slug}} download
```

To run the Koza transform for {{cookiecutter.project_name}}:

```bash
poetry run {{cookiecutter.__project_slug}} transform
```

To see available options:

```bash
poetry run {{cookiecutter.__project_slug}} download --help
# or
poetry run {{cookiecutter.__project_slug}} transform --help
```

---

> This project was generated using [monarch-initiative/cookiecutter-monarch-ingest](https://github.com/monarch-initiative/cookiecutter-monarch-ingest).  
> Keep this project up to date using cruft by occasionally running in the project directory:
>
> ```bash
> cruft update
> ```
>
> For more information, see the [cruft documentation](https://cruft.github.io/cruft/#updating-a-project)
