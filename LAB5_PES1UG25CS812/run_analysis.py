"""Generate before-and-after reports for Pylint, Bandit, and Flake8."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TARGETS = (
    ("before", ROOT / "pos_system_before.py"),
    ("after", ROOT / "pos_system.py"),
)
ANALYZERS = (
    ("pylint", lambda target: [sys.executable, "-m", "pylint", str(target)]),
    ("bandit", lambda target: [sys.executable, "-m", "bandit", "-q", "-r", str(target)]),
    ("flake8", lambda target: [sys.executable, "-m", "flake8", str(target)]),
)


def main() -> int:
    """Run each analyzer against the original and remediated source."""
    after_failures = 0
    for stage, target in TARGETS:
        for name, command_builder in ANALYZERS:
            command = command_builder(target)
            completed = subprocess.run(
                command,
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
            output = completed.stdout
            if completed.stderr:
                output += completed.stderr
            report_path = ROOT / f"{name}_report_{stage}.txt"
            report_path.write_text(
                output or "No findings reported.\n",
                encoding="utf-8",
            )
            print(
                f"{name} ({stage}): exit code {completed.returncode}; "
                f"report: {report_path.name}"
            )
            if stage == "after" and completed.returncode != 0:
                after_failures += 1
    return 1 if after_failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
