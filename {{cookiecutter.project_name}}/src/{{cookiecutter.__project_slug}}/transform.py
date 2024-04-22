import uuid

from koza.cli_runner import get_koza_app

from biolink_model.datamodel.pydanticmodel_v2 import * # Replace * with any necessary data classes from the Biolink Model

koza_app = get_koza_app("{{cookiecutter.__ingest_name}}")

while (row := koza_app.get_row()) is not None:
    # Code to transform each row of data
    # For more information, see https://koza.monarchinitiative.org/Ingests/transform
    ...
