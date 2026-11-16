# tests/test_output_yaml.py
import os
import subprocess
from pathlib import Path

import yaml

from ddlml.cli import main

EXAMPLE = "examples/data_definitions/dairymodel.yaml"
GOLDEN = Path("tests/golden/output.yaml")


def test_simple_example(tmp_path):
    output = tmp_path / "output.yaml"
    code = main(
        [
            "examples/simple_example/database.yaml",
            "--output",
            str(output),
        ]
    )
    assert code == 0
    assert output.exists()


def test_output_yaml_matches_golden(tmp_path):
    output = tmp_path / "output.yaml"
    subprocess.run(
        ["ddlml", str(EXAMPLE), "--output", str(output)],
        check=True,
    )

    produced = yaml.safe_load(output.read_text())

    if os.environ.get("UPDATE_GOLDEN"):
        GOLDEN.parent.mkdir(parents=True, exist_ok=True)
        GOLDEN.write_text(yaml.safe_dump(produced, sort_keys=True))

    expected = yaml.safe_load(GOLDEN.read_text())
    assert produced == expected
