import requests
import json


def get_latest_reports():
    url = f"https://api.github.com/repos/{{ cookiecutter.github_org_name }}/{{ cookiecutter.__project_slug }}/releases/latest"
    response = requests.get(url)
    data = json.loads(response.text)

    reports = []
    for asset in data["assets"]:
        if "report" in asset["name"].split("_"):
            file_url = asset["browser_download_url"]
            reports.append(file_url)

    return reports


def download_reports(reports):
    for report in reports:
        response = requests.get(report)
        with open(f"docs/{report.split('/')[-1]}", "wb") as f:
            f.write(response.content)

print(get_latest_reports())
