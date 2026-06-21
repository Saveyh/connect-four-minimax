from __future__ import annotations

import argparse
from collections.abc import Sequence

from connect4.bots import BlockingBot, KelawinBot, MinimaxBot, MinimaxBotV2, RandomBot
from connect4.core import Strategy
from connect4.match import play_match
from connect4.ui.bot_vs_bot_gui import main as bot_vs_bot_main
from connect4.ui.player_vs_bot_gui import main as player_vs_bot_main

BOT_REGISTRY: dict[str, type[Strategy]] = {
    "blocking": BlockingBot,
    "kelawin": KelawinBot,
    "minimax": MinimaxBot,
    "minimax-v2": MinimaxBotV2,
    "random": RandomBot,
}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="connect4",
        description="Play Connect Four locally with bots and Tkinter demos.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("human", help="Launch the human-vs-bot Tkinter interface.")
    subparsers.add_parser("arena", help="Launch the bot-vs-bot Tkinter interface.")

    match_parser = subparsers.add_parser("match", help="Run a terminal match between two bots.")
    match_parser.add_argument("--red", choices=sorted(BOT_REGISTRY), default="minimax")
    match_parser.add_argument("--yellow", choices=sorted(BOT_REGISTRY), default="kelawin")
    match_parser.add_argument("--height", type=int, default=6)
    match_parser.add_argument("--width", type=int, default=7)
    match_parser.add_argument("--to-win", type=int, default=4, dest="to_win")
    match_parser.add_argument("--delay", type=float, default=0.2)
    match_parser.add_argument("--quiet", action="store_true")

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "human":
        player_vs_bot_main()
        return 0

    if args.command == "arena":
        bot_vs_bot_main()
        return 0

    red_bot = BOT_REGISTRY[args.red]()
    yellow_bot = BOT_REGISTRY[args.yellow]()
    winner = play_match(
        red_bot,
        yellow_bot,
        height=args.height,
        width=args.width,
        to_win=args.to_win,
        verbose=not args.quiet,
        turn_delay=args.delay,
    )
    print(f"Final result: {winner.name if winner else 'DRAW'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
