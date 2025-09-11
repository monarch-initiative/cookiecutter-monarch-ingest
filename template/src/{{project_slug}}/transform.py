import uuid  # For generating UUIDs for associations
import koza
from biolink_model.datamodel.pydanticmodel_v2 import *  # Replace * with any necessary data classes from the Biolink Model


@koza.transform_record()
def transform_record(koza_transform, row):
    # Code to transform each row of data
    # For more information, see https://koza.monarchinitiative.org/Ingests/transform
    
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
    association = Association(
        id=str(uuid.uuid1()),
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
