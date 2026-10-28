# vds-project-student-performance-and-dropout-risk

Interactive dashboard on student dropout risk

## Setup

```bash
uv sync
```

## Run

```bash
uv run python src/main.py            # browser at http://127.0.0.1:8050, hot reload
uv run python src/main.py --desktop  # native window, as in the .exe
```

## Build the .exe

```bash
uv run python build_exe.py            # -> dist/StudentDropoutDashboard.exe
uv run python build_exe.py --onedir   # folder build, starts faster
```

## Project layout

```
assets/                   CSS (and other static files) served by Dash
data/                     dataset (bundled into the .exe)
src/
  app.py                  layout + callbacks  <- build the dashboard here
  paths.py                resource_path() / DATA_FILE, work from source and inside the .exe
  desktop.py              starts the Dash server and opens the pywebview window
  main.py                 command-line entry point
launcher.py               entry script for PyInstaller
build_exe.py              PyInstaller build configuration
```

## Data

[Student Academic Performance and Dropout Risk](https://www.kaggle.com/datasets/mohankrishnathalla/student-academic-performance-and-dropout-risk) by Mohan Krishna Thalla (Kaggle).
