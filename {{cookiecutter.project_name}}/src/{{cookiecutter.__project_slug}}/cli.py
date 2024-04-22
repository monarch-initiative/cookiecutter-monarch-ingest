"""Command line interface for {{cookiecutter.project_name}}."""
import logging

import click
from koza.cli_runner import transform_source

logger = logging.getLogger(__name__)


@click.command()
@click.option("-o", "--output-dir", default="output", help="Output directory for transformed data")
@click.option("-r", "--row-limit", default=None, help="Number of rows to process")
@click.option("-v", "--verbose", default=False, help="Whether to be verbose")
def main(
    output_dir: str,
    row_limit: int,
    verbose: int
):
    """Run the Koza transform for {{cookiecutter.project_name}}"""
    transform_source(
        source='transform.py',
        output_dir=output_dir,
        output_format="tsv",
        row_limit=row_limit,
        verbose=verbose,
    )


if __name__ == "__main__":
    main()
