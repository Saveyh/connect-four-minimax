# Connect Four Minimax
![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)
![Tkinter](https://img.shields.io/badge/UI-Tkinter-FFCC00?logo=python&logoColor=black)
![Game](https://img.shields.io/badge/Game-Connect%20Four-D7263D)
![AI](https://img.shields.io/badge/AI-Minimax-1F6FEB)

Connect Four project built around a reusable game engine, several bot strategies, and lightweight Tkinter interfaces for local play and bot-vs-bot demos.

## Highlights

- Reusable board engine with isolated game rules in `src/connect4/core.py`
- Multiple bot strategies, including minimax-based variants
- Tkinter interfaces for human-vs-bot and bot-vs-bot matches
- CLI entry point for running matches without touching internal modules
- Archived prototypes separated from the production package
- GitHub Actions workflow for automated validation

## Project layout

```text
src/connect4/
  bots/        Bot strategies
  ui/          Tkinter interfaces
  cli.py       Command-line entry point
  core.py      Board model and game rules
  match.py     Terminal match runner
tests/         Regression tests
scripts/       Thin local launchers
archive/       Older experiments kept out of the main package
```

## Installation

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

`requirements.txt` installs the package in editable mode together with the development tools used by CI.

## Usage

Play against the main bot:

```bash
connect4 human
```

Watch two bots play in the GUI:

```bash
connect4 arena
```

Run a terminal bot match:

```bash
connect4 match --red minimax --yellow kelawin
```

Run the same CLI through Python:

```bash
python -m connect4 match --quiet
```

Legacy launchers remain available in `scripts/` for convenience after installation.

## Development

Run the test suite:

```bash
python -m unittest discover -s tests -v
```

Run style checks:

```bash
pycodestyle --exclude .git,.venv,venv,archive,.idea src scripts tests
```

Run type checks:

```bash
pytype src scripts tests
```

## Publishing notes

- The code intended for public use is isolated from historical experiments.
- The package is installable and exposes a stable CLI entry point.
- A repository license is still worth adding, but that choice should be made explicitly by the owner.
