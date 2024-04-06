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
├── src/{{cookiecutter.project_slug}}
│   ├── __init__.py
│   ├── transform.py
│   ├── transform.yaml
│   ├── metadata.yaml
├── pyproject.toml
├── README.md
├── LICENSE
```