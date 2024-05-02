import requests
import json


def main():
    url = (
        "https://api.github.com/repos/{{ cookiecutter.github_org_name }}/{{ cookiecutter.__repo_name }}/releases/latest"
    )

    # Get the latest release from the GitHub API
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(
            f"\n\tFailed to get latest release from {url}\n\tStatus Code: {response.status_code} - {response.text}"
        )
    data = json.loads(response.text)

    # Get the download URLs for the reports
    reports = {}
    for asset in data["assets"]:
        report_name = asset["name"]
        if "report" in asset["name"].split("_"):
            file_url = asset["browser_download_url"]
            reports[report_name] = file_url

    if not reports:
        raise Exception("No reports found in the latest release")

    # Download the reports
    for fn, url in reports:
        response = requests.get(url)
        output_fn = "_".join(fn.split("_")[:-1])
        with open(f"docs/{output_fn}", "wb") as f:
            f.write(response.content)


print(main())
