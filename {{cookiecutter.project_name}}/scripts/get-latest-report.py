import requests
import json


def get_latest_release_file(user, repo, filename):
    url = f"https://api.github.com/repos/{{ cookiecutter.github_org_name }}/{{ cookiecutter.__project_slug }}/releases/latest"
    response = requests.get(url)
    data = json.loads(response.text)

    for asset in data["assets"]:
        if asset["name"] == "report.md":
            file_url = asset["browser_download_url"]
            return file_url

    return None


# Usage
user = "username"
repo = "repository"
filename = "file.ext"
print(get_latest_release_file(user, repo, filename))
