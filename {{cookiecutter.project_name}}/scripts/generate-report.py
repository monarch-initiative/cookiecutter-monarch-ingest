from pathlib import Path

import duckdb

nodes_file = "output/{{ cookiecutter.__ingest_name }}_nodes.tsv"
edges_file = "output/{{ cookiecutter.__ingest_name }}_edges.tsv"


# Nodes
if Path(nodes_file).exists():
    query = f"""
    SELECT category, split_part(id, ':', 1) as prefix, count(*)
    FROM '{nodes_file}'
    GROUP BY all
    ORDER BY all
    """
    duckdb.sql(f"copy ({query}) to 'output/{{ cookiecutter.__ingest_name }}_nodes_report.tsv' (header, delimiter '\t')")

# Edges
if Path(edges_file).exists():
    query = f"""
    SELECT category, split_part(subject, ':', 1) as subject_prefix, predicate,
    split_part(object, ':', 1) as object_prefix, count(*)
    FROM '{edges_file}'
    GROUP BY all
    ORDER BY all
    """
    duckdb.sql(f"copy ({query}) to 'output/{{ cookiecutter.__ingest_name }}_edges_report.tsv' (header, delimiter '\t')")
