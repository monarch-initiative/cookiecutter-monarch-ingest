"""
An example test file for the transform script.

It uses pytest fixtures to define the input data and the mock koza transform. 
The test_example function then tests the output of the transform script.

See the Koza documentation for more information on testing transforms:
https://koza.monarchinitiative.org/Usage/testing/
"""

import pytest 

from koza.utils.testing_utils import mock_koza

# Define the ingest name and transform script path
INGEST_NAME = "{{cookiecutter.__project_slug}}"
TRANSFORM_SCRIPT = "./src/{{cookiecutter.__project_slug}}/transform.py"

# Define an example row to test (as a dictionary)
@pytest.fixture
def example_row():
    return {
        "example_column_1": "entity_1",
        "example_column_2": "entity_6",
        "example_column_3": "biolink:related_to",
    }

# Or a list of rows
@pytest.fixture
def example_list_of_rows():
    return [
        {
            "example_column_1": "entity_1",
            "example_column_2": "entity_6",
            "example_column_3": "biolink:related_to",
        },
        {
            "example_column_1": "entity_2",
            "example_column_2": "entity_7",
            "example_column_3": "biolink:related_to",
        },
    ]

# Define the mock koza transform
@pytest.fixture
def mock_transform(mock_koza, example_row):
    return mock_koza(
        INGEST_NAME,
        example_row,
        TRANSFORM_SCRIPT,
    )

# Or for multiple rows
@pytest.fixture
def mock_transform_multiple_rows(mock_koza, example_list_of_rows):
    return mock_koza(
        INGEST_NAME,
        example_list_of_rows,
        TRANSFORM_SCRIPT,
    )

# Test the output of the transform

def test_single_row(mock_transform):
    assert len(mock_transform) == 1
    entity = mock_transform[0]
    assert entity
    assert entity.subject == "entity_1"


def test_multiple_rows(mock_transform_multiple_rows):
    assert len(mock_transform_multiple_rows) == 2
    entity_1 = mock_transform_multiple_rows[0]
    entity_2 = mock_transform_multiple_rows[1]
    assert entity_1.subject == "entity_1"
    assert entity_2.subject == "entity_2"
