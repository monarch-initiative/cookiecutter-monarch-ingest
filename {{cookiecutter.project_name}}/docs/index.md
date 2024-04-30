# {{cookiecutter.project_name}}

{{cookiecutter.project_description}}

## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)

## Requirements

- Python >= {{cookiecutter.min_python_version}}
- [Poetry](https://python-poetry.org/docs/#installation)

## Installation

```bash
cd {{cookiecutter.project_name}}
make install
# or
poetry install
```

> **Note** that the `make install` command is a convenience wrapper around `poetry install`.

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

To download the data for the {{cookiecutter.__project_slug}} transform:

```bash
poetry run ingest download
```

To run the Koza transform for {{cookiecutter.project_name}}:

```bash
poetry run ingest transform
```

To see available options:

```bash
poetry run ingest download --help
# or
poetry run ingest transform --help
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
