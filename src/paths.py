"""Locating bundled resources (data, assets) from source and inside the PyInstaller .exe."""

from __future__ import annotations

import sys
from pathlib import Path


def resource_path(*parts: str) -> Path:
    """Path to a bundled resource, both when run from source and inside a PyInstaller build."""
    base = getattr(sys, "_MEIPASS", None)
    root = Path(base) if base else Path(__file__).resolve().parents[1]
    return root.joinpath(*parts)


DATA_FILE = resource_path("data", "student_dropout_risk_2026.csv")
