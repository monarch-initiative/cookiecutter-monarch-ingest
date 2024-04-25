import pytest 

from koza.utils.testing_utils import mock_koza

# Define the source name and transform script path
INGEST_NAME = "{{cookiecutter.__project_slug}}"
TRANSFORM_SCRIPT = "./src/{{cookiecutter.__project_slug}}/transform.py"

# Define an example row to test
@pytest.fixture
def example_row():
    return {
        "example_column_1": "entity_1",
        "example_column_2": "entity_6",
        "example_column_3": "biolink:related_to",
    }

# Define the mock koza transform
@pytest.fixture
def mock_transform(mock_koza, example_row):
    return mock_koza(
        INGEST_NAME,
        iter([example_row]),
        TRANSFORM_SCRIPT,
    )

# Define the test
def test_example(mock_transform):
    assert len(mock_transform) == 1
    entity = mock_transform[0]
    assert entity
    assert entity.subject == "entity_1"