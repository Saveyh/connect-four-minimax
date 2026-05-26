# Connect Four Bots

Cleaned-up public version of a Connect Four project built around a reusable game engine, several bot strategies, and simple Tkinter interfaces.

## What is in this repository

- `src/connect4/core.py`: the board model, token definitions, and shared game helpers.
- `src/connect4/bots/`: the playable bot strategies.
- `src/connect4/ui/`: Tkinter interfaces for human-vs-bot and bot-vs-bot matches.
- `scripts/`: small entry points for running the project locally.
- `archive/experiments/`: older drafts and prototypes kept for reference, separated from the production code.
- `tests/`: basic regression tests for the core game logic.

## Getting started

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Run the project

Play against the main bot:

```bash
python scripts/play_gui.py
```

Watch two bots play against each other:

```bash
python scripts/watch_bots_gui.py
```

Run a terminal bot match:

```bash
python scripts/play_bot_match.py
```

Run tests:

```bash
python -m unittest discover -s tests
```

## Notes before publishing

- The repository is now organized so the public code is separate from archived experiments.
- IDE files should stay untracked.
- If you want to make the repository fully open source, adding a `LICENSE` file is the last important missing public-facing step.
