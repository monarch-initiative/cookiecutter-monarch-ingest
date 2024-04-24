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

## Project Structure

The project structure is as follows:

```
{{cookiecutter.project_name}}
├── .github/
│   ├── workflows/
│   │   ├── deploy-docs.yml
│   │   ├── test.yml
|   ├── dependabot.yml
├── data/example_data.tsv
├── docs/
├── src/{{cookiecutter.__project_slug}}
│   ├── __init__.py
│   ├── cli.py
│   ├── metadata.yaml
│   ├── transform.py
│   ├── transform.yaml
├── pyproject.toml
├── CONTRIBUTING.md
├── LICENSE
├── pyproject.toml
├── README.md
```
