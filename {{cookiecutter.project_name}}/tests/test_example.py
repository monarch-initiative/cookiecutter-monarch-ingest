"""
An example test file for the transform script.

It uses pytest fixtures to define the input data and the KozaRunner.
The test functions then test the output of the transform script.

See the Koza documentation for more information on testing transforms:
https://koza.monarchinitiative.org/Usage/testing/
"""

import pytest
from biolink_model.datamodel.pydanticmodel_v2 import Association, Entity
from koza.io.writer.writer import KozaWriter
from koza.runner import KozaRunner, KozaTransformHooks
from {{cookiecutter.__project_slug}}.transform import transform_record


class MockWriter(KozaWriter):
    def __init__(self):
        self.items = []

    def write(self, entities):
        self.items += entities

    def finalize(self):
        pass


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


# Define the koza transform using new API
@pytest.fixture
def mock_transform(example_row):
    # Returns [entity_a, entity_b, association] for a single row
    writer = MockWriter()
    
    runner = KozaRunner(
        data=iter([example_row]),
        writer=writer,
        hooks=KozaTransformHooks(transform_record=[transform_record])
    )
    runner.run()
    return writer.items


# Or for multiple rows
@pytest.fixture
def mock_transform_multiple_rows(example_list_of_rows):
    # Returns concatenated list of [entity_a, entity_b, association]
    # for each row in example_list_of_rows
    writer = MockWriter()
    
    runner = KozaRunner(
        data=iter(example_list_of_rows),
        writer=writer,
        hooks=KozaTransformHooks(transform_record=[transform_record])
    )
    runner.run()
    return writer.items


# Test the output of the transform


def test_single_row(mock_transform):
    assert len(mock_transform) == 3
    
    # Check entities
    entity_a = mock_transform[0]
    entity_b = mock_transform[1]
    association = mock_transform[2]
    
    assert isinstance(entity_a, Entity)
    assert isinstance(entity_b, Entity)
    assert isinstance(association, Association)
    
    assert entity_a.name == "entity_1"
    assert entity_b.name == "entity_6"
    assert association.predicate == "biolink:related_to"


def test_multiple_rows(mock_transform_multiple_rows):
    assert len(mock_transform_multiple_rows) == 6
    
    # First row entities
    entity_a = mock_transform_multiple_rows[0]
    entity_b = mock_transform_multiple_rows[1]
    association = mock_transform_multiple_rows[2]
    
    assert isinstance(entity_a, Entity)
    assert isinstance(entity_b, Entity)
    assert isinstance(association, Association)
    
    assert entity_a.name == "entity_1"
    assert entity_b.name == "entity_6"
