"""
Download the latest reports from GitHub releases.

Auto-discovers the GitHub repository from project configuration.
"""

import json
import sys
from pathlib import Path

import requests


def get_project_repo_info():
    """Get GitHub repository information from pyproject.toml."""
    try:
        import tomllib
        project_root = Path(__file__).parent.parent
        pyproject_path = project_root / "pyproject.toml"
        
        if pyproject_path.exists():
            with open(pyproject_path, 'rb') as f:
                config = tomllib.load(f)
                
            # Look for repository URL in various places
            project_config = config.get('project', {})
            
            # Check project.urls.repository
            urls = project_config.get('urls', {})
            repo_url = urls.get('repository') or urls.get('Repository')
            
            if repo_url and 'github.com' in repo_url:
                # Extract org/repo from URL like https://github.com/org/repo
                parts = repo_url.rstrip('/').split('/')
                if len(parts) >= 2:
                    return parts[-2], parts[-1]
    except Exception:
        pass
    
    # Fallback: try to guess from directory structure
    project_root = Path(__file__).parent.parent
    project_name = project_root.name
    return "monarch-initiative", project_name


def main():
    """Download latest reports from GitHub releases."""
    if len(sys.argv) > 2:
        github_org = sys.argv[1]
        repo_name = sys.argv[2]
    else:
        github_org, repo_name = get_project_repo_info()
    
    url = f"https://api.github.com/repos/{github_org}/{repo_name}/releases/latest"
    print(f"Fetching latest release from: {url}")
    
    # Get the latest release from the GitHub API
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(
            f"\n\tFailed to get latest release from {url}\n\tStatus: {response.status_code} - {response.text}"
        )
    data = json.loads(response.text)

    # Get the download URLs for the reports
    reports = {}
    for asset in data["assets"]:
        report_name = asset["name"]
        if "report.tsv" in asset["name"].split("_"):
            file_url = asset["browser_download_url"]
            reports[report_name] = file_url

    if not reports:
        raise Exception("No reports found in the latest release")

    # Create docs directory if it doesn't exist
    docs_dir = Path("docs")
    docs_dir.mkdir(exist_ok=True)

    # Download the reports
    for fn, url in reports.items():
        print(f"Downloading {fn}...")
        response = requests.get(url)
        output_fn = "_".join(fn.split("_")[-2:])
        output_path = docs_dir / output_fn
        with open(output_path, "wb") as f:
            f.write(response.content)
        print(f"Saved to {output_path}")


if __name__ == "__main__":
    main()