"""
Transform for {{ cookiecutter.project_name }}.

This module transforms data from the source into Biolink model entities and associations.
"""

import uuid
from typing import Any

import koza
from koza import KozaTransform
from biolink_model.datamodel.pydanticmodel_v2 import Entity, Association


@koza.transform_record()
def transform_record(koza_transform: KozaTransform, row: dict[str, Any]) -> list[Entity | Association]:
    """
    Transform a data row into Biolink entities and associations.

    Args:
        koza_transform: Koza transform context
        row: Dictionary containing row data

    Returns:
        list[Entity | Association]: List of Biolink entities and/or associations

    Note:
        - Always return a list, even for single entities
        - Return empty list [] to skip rows (don't return None)
        - Import specific Biolink classes instead of using *
    """
    # Example: Skip rows without required data
    if not row.get('example_column_1') or not row.get('example_column_2'):
        return []

    # Example entities
    entity_a = Entity(
        id=f"XMPL:00000{row['example_column_1'].split('_')[-1]}",
        name=row["example_column_1"],
        category=["biolink:Entity"],
    )
    entity_b = Entity(
        id=f"XMPL:00000{row['example_column_2'].split('_')[-1]}",
        name=row["example_column_2"],
        category=["biolink:Entity"],
    )

    # Example association
    association = Association(
        id=f"uuid:{uuid.uuid4()}",  # Use uuid4() for association IDs
        subject=row["example_column_1"],
        predicate=row["example_column_3"],
        object=row["example_column_2"],
        subject_category="SUBJ",
        object_category="OBJ",
        category=["biolink:Association"],
        knowledge_level="not_provided",
        agent_type="not_provided",
    )

    return [entity_a, entity_b, association]
