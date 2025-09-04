"""Command line interface for {{cookiecutter.project_name}}."""
import logging

from pathlib import Path

from kghub_downloader.download_utils import download_from_yaml

from koza.runner import KozaRunner
from koza.model.formats import OutputFormat
from loguru import logger
import typer

app = typer.Typer()
logging_logger = logging.getLogger(__name__)


@app.callback()
def callback(version: bool = typer.Option(False, "--version", is_eager=True),
):
    """{{cookiecutter.project_name}} CLI."""
    if version:
        from {{cookiecutter.__project_slug}} import __version__
        typer.echo(f"{{cookiecutter.project_name}} version: {__version__}")
        raise typer.Exit()


@app.command()
def download(force: bool = typer.Option(False, help="Force download of data, even if it exists")):
    """Download data for {{cookiecutter.project_name}}."""
    typer.echo("Downloading data for {{cookiecutter.project_name}}...")
    download_config = Path(__file__).parent / "download.yaml"

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
):
    """Run the Koza transform for {{cookiecutter.project_name}}."""
    typer.echo("Transforming data for {{cookiecutter.project_name}}...")
    transform_config = Path(__file__).parent / "transform.yaml"
    
    output_path = Path(output_dir)
    if output_path.exists() and not output_path.is_dir():
        raise NotADirectoryError(f"{output_dir} is not a directory")
    elif not output_path.exists():
        output_path.mkdir(parents=True)
    
    if not quiet:
        logger.remove()
        logger.add(lambda msg: typer.echo(msg, nl=False), colorize=True)
    
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
    

if __name__ == "__main__":
    app()
