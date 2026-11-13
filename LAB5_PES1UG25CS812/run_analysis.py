"""Run Pylint, Bandit, and Flake8 and save their real outputs."""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TARGET = ROOT / "pos_system.py"
TOOLS = (
    ("pylint", [sys.executable, "-m", "pylint", str(TARGET)]),
    ("bandit", [sys.executable, "-m", "bandit", "-q", "-r", str(TARGET)]),
    ("flake8", [sys.executable, "-m", "flake8", str(TARGET)]),
)


def main() -> int:
    """Execute available analyzers and save their output."""
    missing = [name for name, _ in TOOLS if shutil.which(name) is None]
    if missing:
        print(
            "Missing tools: "
            + ", ".join(missing)
            + ". Install them with: python -m pip install -r requirements.txt"
        )
        return 2

    failures = 0
    for name, command in TOOLS:
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
        report_path = ROOT / f"{name}_report.txt"
        report_path.write_text(output or "No findings reported.\n", encoding="utf-8")
        print(f"{name}: exit code {completed.returncode}; report: {report_path.name}")
        if completed.returncode not in (0,):
            failures += 1

    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
