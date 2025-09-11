"""
Test file for transform scripts.

Uses pytest fixtures to define input data and KozaRunner.
Tests the output of transform functions with dynamic discovery.

See the Koza documentation for more information on testing transforms:
https://koza.monarchinitiative.org/Usage/testing/
"""

import sys
from pathlib import Path
from typing import Any, Dict, List

import pytest
from biolink_model.datamodel.pydanticmodel_v2 import Association, Entity
from koza.io.writer.writer import KozaWriter
from koza.runner import KozaRunner, KozaTransformHooks


def discover_transform_module():
    """Dynamically discover and import the transform module."""
    # Find the src directory relative to this test file
    test_dir = Path(__file__).parent
    project_root = test_dir.parent
    src_dir = project_root / "src"
    
    if not src_dir.exists():
        raise ImportError("Could not find src directory")
    
    # Find project directories that contain transform.py
    project_dirs = [
        d for d in src_dir.iterdir() 
        if d.is_dir() and (d / "transform.py").exists()
    ]
    
    if not project_dirs:
        raise ImportError("Could not find any project directory with transform.py")
    
    if len(project_dirs) > 1:
        # For multiple transforms, we could extend this to handle specific ones
        # For now, just use the first one found
        pass
    
    project_name = project_dirs[0].name
    
    # Add src to path and import the transform module
    if str(src_dir) not in sys.path:
        sys.path.insert(0, str(src_dir))
    
    try:
        transform_module = __import__(f"{project_name}.transform", fromlist=["transform_record"])
        return transform_module.transform_record
    except ImportError as e:
        raise ImportError(f"Could not import transform_record from {project_name}.transform: {e}")


# Discover the transform function dynamically
transform_record = discover_transform_module()


class MockWriter(KozaWriter):
    """Mock writer for testing that captures written entities."""
    
    def __init__(self):
        self.items = []

    def write(self, entities):
        self.items += entities

    def finalize(self):
        pass


# Define example test data
@pytest.fixture
def example_row() -> Dict[str, Any]:
    """Example row data for testing single record transformation."""
    return {
        "example_column_1": "entity_1",
        "example_column_2": "entity_6", 
        "example_column_3": "biolink:related_to",
    }


@pytest.fixture
def example_list_of_rows() -> List[Dict[str, Any]]:
    """Example list of rows for testing multiple record transformation."""
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


@pytest.fixture
def mock_transform(example_row) -> List[Any]:
    """Run transform on a single row and return results."""
    writer = MockWriter()
    
    runner = KozaRunner(
        data=iter([example_row]),
        writer=writer,
        hooks=KozaTransformHooks(transform_record=[transform_record])
    )
    runner.run()
    return writer.items


@pytest.fixture
def mock_transform_multiple_rows(example_list_of_rows) -> List[Any]:
    """Run transform on multiple rows and return concatenated results."""
    writer = MockWriter()
    
    runner = KozaRunner(
        data=iter(example_list_of_rows),
        writer=writer,
        hooks=KozaTransformHooks(transform_record=[transform_record])
    )
    runner.run()
    return writer.items


# Test functions
def test_single_row_transform(mock_transform):
    """Test transformation of a single row produces expected entities."""
    assert len(mock_transform) == 3
    
    # Check entity types
    entity_a = mock_transform[0]
    entity_b = mock_transform[1]
    association = mock_transform[2]
    
    assert isinstance(entity_a, Entity)
    assert isinstance(entity_b, Entity)
    assert isinstance(association, Association)
    
    # Check entity properties
    assert entity_a.name == "entity_1"
    assert entity_b.name == "entity_6"
    assert association.predicate == "biolink:related_to"


def test_multiple_rows_transform(mock_transform_multiple_rows):
    """Test transformation of multiple rows produces expected number of entities."""
    assert len(mock_transform_multiple_rows) == 6  # 3 entities per row × 2 rows
    
    # Check first row entities
    entity_a = mock_transform_multiple_rows[0]
    entity_b = mock_transform_multiple_rows[1]
    association = mock_transform_multiple_rows[2]
    
    assert isinstance(entity_a, Entity)
    assert isinstance(entity_b, Entity)
    assert isinstance(association, Association)
    
    assert entity_a.name == "entity_1"
    assert entity_b.name == "entity_6"
    assert association.predicate == "biolink:related_to"


def test_transform_discovery():
    """Test that transform module discovery works correctly."""
    # This test ensures our dynamic discovery is working
    assert transform_record is not None
    assert callable(transform_record)


# Additional test for future multi-transform support
def test_discover_multiple_transforms():
    """Test discovery when multiple transform directories exist (future feature)."""
    # This test is a placeholder for when we support multiple transforms
    # For now, it just verifies we can discover at least one transform
    test_dir = Path(__file__).parent
    project_root = test_dir.parent
    src_dir = project_root / "src"
    
    if src_dir.exists():
        project_dirs = [
            d for d in src_dir.iterdir() 
            if d.is_dir() and (d / "transform.py").exists()
        ]
        assert len(project_dirs) >= 1, "Should find at least one transform directory"