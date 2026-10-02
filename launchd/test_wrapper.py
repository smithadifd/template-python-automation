"""Run the offline Bash wrapper contract as part of the CI pytest command."""

import os
import subprocess
from pathlib import Path


def test_wrapper_contract():
    directory = Path(__file__).parent
    wrapper = os.environ.get("TOOLNAME_WRAPPER", str(directory / "toolname-run.sh"))
    result = subprocess.run(
        ["bash", str(directory / "test-toolname-run.sh"), wrapper],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr or result.stdout
