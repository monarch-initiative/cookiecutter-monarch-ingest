"""
Generate RDF output from transform files.

Auto-discovers transform output files and converts them to RDF format.
Supports multiple transforms by processing all *_nodes.tsv and *_edges.tsv files.
"""

import sys
from pathlib import Path
from typing import List, Tuple

from kgx.cli.cli_utils import transform as kgx_transform
from loguru import logger


def discover_output_files(output_dir: Path = Path("output")) -> List[Tuple[str, List[str]]]:
    """
    Discover transform output files and group them by ingest name.
    
    Returns:
        List of tuples (ingest_name, [list_of_files])
    """
    if not output_dir.exists():
        logger.warning(f"Output directory {output_dir} does not exist")
        return []
    
    # Find all nodes files
    nodes_files = list(output_dir.glob("*_nodes.tsv"))
    discovered = []
    
    for nodes_file in nodes_files:
        # Extract ingest name by removing _nodes suffix
        ingest_name = nodes_file.stem.replace("_nodes", "")
        
        # Collect files for this ingest
        src_files = []
        
        # Add nodes file
        if nodes_file.exists():
            src_files.append(str(nodes_file))
        
        # Look for corresponding edges file
        edges_file = output_dir / f"{ingest_name}_edges.tsv"
        if edges_file.exists():
            src_files.append(str(edges_file))
        
        if src_files:
            discovered.append((ingest_name, src_files))
    
    return discovered


def generate_rdf_for_ingest(ingest_name: str, src_files: List[str], output_dir: Path) -> None:
    """Generate RDF output for a single ingest."""
    output_file = output_dir / f"{ingest_name}.nt.gz"
    
    logger.info(f"Creating RDF output: {output_file}")
    logger.info(f"Source files: {src_files}")
    
    try:
        kgx_transform(
            inputs=src_files,
            input_format="tsv",
            stream=True,
            output=str(output_file),
            output_format="nt",
            output_compression="gz",
        )
        logger.info(f"Successfully created {output_file}")
    except Exception as e:
        logger.error(f"Error generating RDF for {ingest_name}: {e}")


def main():
    """Main entry point for RDF generation."""
    output_dir = Path("output")
    
    if len(sys.argv) > 1:
        output_dir = Path(sys.argv[1])
    
    logger.info(f"Discovering output files in {output_dir}")
    discovered_files = discover_output_files(output_dir)
    
    if not discovered_files:
        logger.warning("No transform output files found")
        return
    
    logger.info(f"Found {len(discovered_files)} transform output(s)")
    
    for ingest_name, src_files in discovered_files:
        generate_rdf_for_ingest(ingest_name, src_files, output_dir)
    
    logger.info("RDF generation complete")


if __name__ == "__main__":
    main()