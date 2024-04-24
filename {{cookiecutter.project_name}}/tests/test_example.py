import pytest 

from koza.utils.testing import mock_koza


SOURCE_NAME = "{{cookiecutter.__ingest_name}}"
TRANSFORM_SCRIPT = "./src/{{cookiecutter.__project_slug}}/transform.py"

@pytest.fixture
def example_row():
    return {
        "example_column_1": "entity_1",
        "example_column_2": "entity_6",
        "example_column_3": "biolink:related_to",
    }

@pytest.fixture
def mock_transform():
    return mock_koza(
        SOURCE_NAME,
        iter([example_row]),
        TRANSFORM_SCRIPT,
    )

def test_example(mock_transform):
    assert len(mock_transform) == 1
    entity = mock_transform[0]
    assert entity
    assert entity.example_column_1 == "entity_1"