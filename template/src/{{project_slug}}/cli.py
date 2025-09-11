"""Command line interface for data ingest."""
import logging
import sys
from pathlib import Path
from typing import Optional, Tuple

from kghub_downloader.download_utils import download_from_yaml
from koza.runner import KozaRunner
from koza.model.formats import OutputFormat
from loguru import logger
import typer

app = typer.Typer()
logging_logger = logging.getLogger(__name__)


def get_project_info() -> Tuple[str, str]:
    """Get project name and description from pyproject.toml or package metadata."""
    try:
        # Try to read from pyproject.toml first
        import tomllib
        project_root = Path(__file__).parent.parent.parent
        pyproject_path = project_root / "pyproject.toml"
        
        if pyproject_path.exists():
            with open(pyproject_path, 'rb') as f:
                config = tomllib.load(f)
                name = config.get('project', {}).get('name', 'data-ingest')
                description = config.get('project', {}).get('description', 'Data ingest project')
                return name, description
    except Exception:
        pass
    
    try:
        # Fallback to package metadata
        import importlib.metadata
        package_name = __package__ or Path(__file__).parent.name
        metadata = importlib.metadata.metadata(package_name)
        name = metadata.get('Name', package_name)
        description = metadata.get('Summary', 'Data ingest project')
        return name, description
    except Exception:
        # Final fallback
        package_name = Path(__file__).parent.name
        return package_name, 'Data ingest project'


def discover_config_files() -> Tuple[Optional[Path], Optional[Path]]:
    """Discover download.yaml and transform.yaml files."""
    package_dir = Path(__file__).parent
    download_config = package_dir / "download.yaml"
    transform_config = package_dir / "transform.yaml"
    
    return (
        download_config if download_config.exists() else None,
        transform_config if transform_config.exists() else None
    )


@app.callback()
def callback(
    version: bool = typer.Option(False, "--version", is_eager=True),
):
    """Data ingest CLI."""
    if version:
        try:
            from importlib.metadata import version as get_version
            package_name = __package__ or Path(__file__).parent.name
            version_str = get_version(package_name)
        except Exception:
            version_str = "unknown"
        
        project_name, _ = get_project_info()
        typer.echo(f"{project_name} version: {version_str}")
        raise typer.Exit()


@app.command()
def download(force: bool = typer.Option(False, help="Force download of data, even if it exists")):
    """Download data for the ingest."""
    project_name, _ = get_project_info()
    typer.echo(f"Downloading data for {project_name}...")
    
    download_config, _ = discover_config_files()
    if not download_config:
        typer.echo("Error: download.yaml not found", err=True)
        raise typer.Exit(1)
    
    from kghub_downloader.model import DownloadOptions
    options = DownloadOptions(ignore_cache=force) if force else None
    download_from_yaml(yaml_file=str(download_config), output_dir=".", download_options=options)


@app.command()
def transform(
    output_dir: str = typer.Option("output", help="Output directory for transformed data"),
    row_limit: int = typer.Option(0, help="Number of rows to process (0 = all)"),
    output_format: OutputFormat = typer.Option(OutputFormat.tsv, help="Output format"),
    show_progress: bool = typer.Option(False, help="Display progress of transform"),
    quiet: bool = typer.Option(False, help="Disable log output"),
    transform_name: Optional[str] = typer.Option(None, help="Specific transform to run (for multi-transform projects)"),
):
    """Run the Koza transform."""
    project_name, _ = get_project_info()
    typer.echo(f"Transforming data for {project_name}...")
    
    _, transform_config = discover_config_files()
    if not transform_config:
        typer.echo("Error: transform.yaml not found", err=True)
        raise typer.Exit(1)
    
    output_path = Path(output_dir)
    if output_path.exists() and not output_path.is_dir():
        raise NotADirectoryError(f"{output_dir} is not a directory")
    elif not output_path.exists():
        output_path.mkdir(parents=True)
    
    if not quiet:
        logger.remove()
        logger.add(lambda msg: typer.echo(msg, nl=False), colorize=True)
    
    # Support for multiple transforms - if transform_name is specified,
    # we could extend this to run specific transforms from a multi-transform config
    config, runner = KozaRunner.from_config_file(
        str(transform_config),
        output_dir=output_dir,
        output_format=output_format,
        row_limit=row_limit,
        show_progress=show_progress,
    )
    
    logger.info(f"Running transform for {config.name} with output to `{output_dir}`")
    runner.run()
    logger.info(f"Finished transform for {config.name}")


@app.command()
def list_transforms():
    """List available transforms (for future multi-transform support)."""
    _, transform_config = discover_config_files()
    if not transform_config:
        typer.echo("Error: transform.yaml not found", err=True)
        raise typer.Exit(1)
    
    # For now, just show the single transform
    # In future, this could parse transform.yaml and show multiple transforms
    import yaml
    with open(transform_config) as f:
        config = yaml.safe_load(f)
    
    transform_name = config.get('name', 'unnamed')
    typer.echo(f"Available transforms:")
    typer.echo(f"  - {transform_name}")


if __name__ == "__main__":
    app()