"""Build the Windows executable with PyInstaller.

    uv run python build_exe.py            # single StudentDropoutDashboard.exe in dist/
    uv run python build_exe.py --onedir   # folder build: starts faster, ship the whole folder
"""

from __future__ import annotations

import argparse
import os

import PyInstaller.__main__

NAME = "StudentDropoutDashboard"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--onedir", action="store_true", help="build a folder instead of a single .exe")
    args = parser.parse_args()

    sep = os.pathsep
    PyInstaller.__main__.run([
        "launcher.py",
        "--name", NAME,
        "--noconfirm",
        "--clean",
        "--windowed",  # no console window
        "--onedir" if args.onedir else "--onefile",
        "--paths", "src",
        "--add-data", f"data{sep}data",
        "--add-data", f"assets{sep}assets",
        # Dash and Plotly load JS bundles and JSON schemas from package data at runtime.
        "--collect-data", "dash",
        "--collect-data", "plotly",
        "--collect-submodules", "dash",
    ])


if __name__ == "__main__":
    main()
