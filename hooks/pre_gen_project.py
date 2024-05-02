"""Code to run before generating the project."""

import re
import sys

REPO_NAME_REGEX = re.compile(r"^[a-zA-Z0-9_-]+$")
MODULE_REGEX = re.compile(r"^[_a-zA-Z][_a-zA-Z0-9]+$")

repo_name = "{{ cookiecutter.__repo_name }}"
module_name = "{{ cookiecutter.__project_slug }}"

# Assert repo name is dash-separated
if not REPO_NAME_REGEX.match(repo_name):
    print(
        f"""ERROR: {repo_name} is not a valid GitHub repository name.
Try again with a valid project name using only '-', '_', '.', or spaces as separators.
"""
    )
    sys.exit(1)

# Check if the module name is a valid Python module name
if not MODULE_REGEX.match(module_name):
    if "-" in module_name:
        invalid_char = "-"
    elif " " in module_name:
        invalid_char = "<space>"
    else:
        print(
            f"ERROR: {module_name} is not a valid Python module name. Try again with a valid project name."
        )
        sys.exit(1)
    print(
        f'WARNING: {module_name} is not a valid Python module name. Try using "_" instead of "{invalid_char}" for module name.'
    )
