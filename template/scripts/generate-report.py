"""
Generate reports from transform output files.

This script auto-discovers output files and generates summary reports.
Supports multiple transforms by processing all *_nodes.tsv and *_edges.tsv files.
"""

import sys
from pathlib import Path
from typing import List, Tuple

import duckdb


def discover_output_files(output_dir: Path = Path("output")) -> List[Tuple[str, Path, Path]]:
    """
    Discover transform output files and group them by ingest name.
    
    Returns:
        List of tuples (ingest_name, nodes_file, edges_file)
    """
    if not output_dir.exists():
        print(f"Output directory {output_dir} does not exist")
        return []
    
    # Find all nodes files
    nodes_files = list(output_dir.glob("*_nodes.tsv"))
    discovered = []
    
    for nodes_file in nodes_files:
        # Extract ingest name by removing _nodes suffix
        ingest_name = nodes_file.stem.replace("_nodes", "")
        
        # Look for corresponding edges file
        edges_file = output_dir / f"{ingest_name}_edges.tsv"
        
        discovered.append((ingest_name, nodes_file, edges_file))
    
    return discovered


def generate_nodes_report(ingest_name: str, nodes_file: Path) -> None:
    """Generate nodes summary report."""
    if not nodes_file.exists():
        print(f"Nodes file {nodes_file} does not exist, skipping")
        return
    
    output_file = nodes_file.parent / f"{ingest_name}_nodes_report.tsv"

    query = f"""  # noqa: S608
    SELECT category, split_part(id, ':', 1) as prefix, count(*)
    FROM '{nodes_file}'
    GROUP BY all
    ORDER BY all
    """
    
    try:
        duckdb.sql(f"copy ({query}) to '{output_file}' (header, delimiter '\\t')")
        print(f"Generated nodes report: {output_file}")
    except Exception as e:
        print(f"Error generating nodes report for {ingest_name}: {e}")


def generate_edges_report(ingest_name: str, edges_file: Path) -> None:
    """Generate edges summary report.""" 
    if not edges_file.exists():
        print(f"Edges file {edges_file} does not exist, skipping")
        return
    
    output_file = edges_file.parent / f"{ingest_name}_edges_report.tsv"

    query = f"""  # noqa: S608
    SELECT category, split_part(subject, ':', 1) as subject_prefix, predicate,
    split_part(object, ':', 1) as object_prefix, count(*)
    FROM '{edges_file}'
    GROUP BY all
    ORDER BY all
    """
    
    try:
        duckdb.sql(f"copy ({query}) to '{output_file}' (header, delimiter '\\t')")
        print(f"Generated edges report: {output_file}")
    except Exception as e:
        print(f"Error generating edges report for {ingest_name}: {e}")


def main():
    """Main entry point for report generation."""
    output_dir = Path("output")
    
    if len(sys.argv) > 1:
        output_dir = Path(sys.argv[1])
    
    print(f"Discovering output files in {output_dir}")
    discovered_files = discover_output_files(output_dir)
    
    if not discovered_files:
        print("No transform output files found")
        return
    
    print(f"Found {len(discovered_files)} transform output(s)")
    
    for ingest_name, nodes_file, edges_file in discovered_files:
        print(f"Processing {ingest_name}...")
        generate_nodes_report(ingest_name, nodes_file)
        generate_edges_report(ingest_name, edges_file)
    
    print("Report generation complete")


if __name__ == "__main__":
    main()