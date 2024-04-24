import pytest 

from koza.utils.testing import mock_koza


source_name = "{{cookiecutter.__ingest_name}}"
script = "./src/{{cookiecutter.__project_slug}}/transform.py"

@pytest.fixture
def example_row():
    return {
        "example_column_1": "entity_1",
        "example_column_2": "entity_6",
        "example_column_3": "biolink:related_to",
    }

def test_example(example_row):
    