# cookiecutter-monarch-ingest

A Cruft cookiecutter template for modular Koza ingests.

This template is designed to help you create a new Koza ingest project. It includes a basic project structure, a Makefile with common tasks, and GitHub Actions workflows for testing and deploying documentation.

> Note: This template assumes you the project will be a GitHub repository (as opposed to GitLab or another CVS platform.  
> If you are using a different platform, you may need to adjust the GitHub Actions workflows accordingly, along with any instances of `https://github.com/...` urls.)

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

Once the project is created, you can keep it up to date by occasionally running the following command in the project directory:

```bash
cruft update
```

For more information, see the [cruft documentation](https://cruft.github.io/cruft/#updating-a-project)

## Setting Up a New Project

Upon creating a new project from the `cookiecutter-monarch-ingest` template, you can install and test the project:

```bash
cd {{cookiecutter.project_name}}
make install
make test
```

There are a few additional steps to complete before the project is ready for use.

#### GitHub Repository

1. Create a new repository on GitHub.
1. Enable GitHub Actions to read and write to the repository (required to deploy the project to GitHub Pages).
   - in GitHub, go to Settings -> Action -> General -> Workflow permissions and choose read and write permissions
1. Initialize the local repository and push the code to GitHub. For example:

   ```bash
   cd {{cookiecutter.project_name}}
   git init
   git remote add origin https://github.com/<username>/<repository>.git
   git add -A && git commit -m "Initial commit"
   git push -u origin main
   ```

#### Transform Code and Configuration

1. Edit the `download.yaml`, `transform.py`, `transform.yaml`, and `metadata.yaml` files to suit your needs.
   - For more information, see the [Koza documentation](https://koza.monarchinitiative.org) and [kghub-downloader](https://github.com/monarch-initiative/kghub-downloader).
1. Add any additional dependencies to the `pyproject.toml` file.
1. Adjust the contents of the `tests` directory to test the functionality of your transform.

#### Documentation

1. Update this `README.md` file with any additional information about the project.
1. Add any appropriate documentation to the `docs` directory.

> **Note:** After the GitHub Actions for deploying documentation runs, the documentation will be automatically deployed to GitHub Pages.  
> However, you will need to go to the repository settings and set the GitHub Pages source to the `gh-pages` branch, using the `/docs` directory.

## Project Structure

Cruft/cookiecutter will create a project with the following structure:

```
{{cookiecutter.project_name}}
├── .github/
│   ├── workflows/
│   │   ├── create-release.yaml
│   │   ├── deploy-docs.yaml
│   │   ├── test.yaml
│   │   ├── update-docs.yaml
|   ├── dependabot.yaml
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

### GitHub Actions

- `test.yaml`: Run the pytest suite.
- `create-release.yaml`: Create a new release once a week, or manually.
- `deploy-docs.yaml`: Deploy the documentation to GitHub Pages (on pushes to main).
- `update-docs.yaml`: After a release, update the documentation with node/edge reports.