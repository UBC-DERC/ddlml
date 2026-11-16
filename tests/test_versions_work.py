"""Testing the construction of the ddlml object, and the use of the info_dict class"""

import re
from pathlib import Path

import pytest
from pydantic import ValidationError

from ddlml.object_classes import CURRENT_DDLML_VERSION, ddlml_dict

# There are a few places where I've hardcoded the acceptable versions
# Including in the actual specifications, and then in each of the yaml objects.
REPO_ROOT = Path(__file__).resolve().parents[1]
SPEC = REPO_ROOT / "docs/specifications/SPECIFICATION.md"
EXAMPLE_ENTRIES = [
    REPO_ROOT / "examples/simple_example/database.yaml",
    REPO_ROOT / "examples/data_definitions/dairymodel.yaml",
]


def test_specification_has_right_header():
    """Check that the specification file has the right version number in it."""
    match = re.search(
        pattern=r"^## Version (\S+)\s*$", string=SPEC.read_text(), flags=re.MULTILINE
    )
    assert match, "SPECIFICATION.md has no '## Version …' heading"
    assert match.group(1) == CURRENT_DDLML_VERSION


def test_old_version_fails():
    with pytest.raises(ValidationError):
        ddlml_dict(
            ddlml_version="2024.10.4",
            database={"name": "test_db", "schemas": []},
            info={
                "version": "2026.10.4",
                "title": "Test Model",
                "summary": "A test model for testing purposes",
                "contacts": [],
            },
        )


def test_current_version_passes():
    ddlml_dict(
        ddlml_version=CURRENT_DDLML_VERSION,
        database={"name": "test_db", "schemas": []},
        info={
            "version": "2026.10.4",
            "title": "Test Model",
            "summary": "A test model for testing purposes",
            "contacts": [],
        },
    )


def test_ddaml_version_mismatch_fails():
    with pytest.raises(ValidationError):
        ddlml_dict(
            ddlml_version="2024.10.4",
            database={"name": "test_db", "schemas": []},
            info={
                "version": "2026.10.4",
                "title": "Test Model",
                "summary": "A test model for testing purposes",
                "contacts": [],
            },
        )
