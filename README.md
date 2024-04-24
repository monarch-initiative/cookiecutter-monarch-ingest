# cookiecutter-monarch-ingest

A Cruft cookiecutter template for modular Koza ingests.

## Getting Started

First, install [cruft](https://cruft.github.io/cruft/):

```bash
pip install cruft
```

Then, create a new project using this template:

```bash
cruft create https://github.com/monarch-initiative/cookiecutter-monarch-ingest.git
```

This will start an interactive session to fill in the project details.

Once the project is created, you can update the project to the latest version of the template by running:

```bash
cruft update
```

For more information, see the [cruft documentation](https://cruft.github.io/cruft/#updating-a-project)

## Setting Up Your Project

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
1. Add any documentation to the `docs` directory.



## Project Structure

Cruft/cookiecutter will create a project with the following structure:

```
{{cookiecutter.project_name}}
├── .github/
│   ├── workflows/
│   │   ├── deploy-docs.yml
│   │   ├── test.yml
|   ├── dependabot.yml
├── docs/
├── src/{{cookiecutter.__project_slug}}
│   ├── __init__.py
│   ├── cli.py
├── ├── download.yaml
│   ├── metadata.yaml
│   ├── transform.py
│   ├── transform.yaml
├── tests/
│   ├── test_example.py
├── pyproject.toml
├── CONTRIBUTING.md
├── LICENSE
├── Makefile
├── mkdocs.yaml
├── pyproject.toml
├── README.md
```
