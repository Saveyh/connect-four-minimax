from __future__ import annotations

import time
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from connect4.bots.kelawin_bot import KelawinBot
from connect4.bots.minimax_bot import MinimaxBot
from connect4.core import Board, IllegalMove, Strategy, Token, board_full, has_winner


def play_match(
    bot1: Strategy,
    bot2: Strategy,
    height: int = 6,
    width: int = 7,
    to_win: int = 4,
    verbose: bool = True,
) -> Token | None:
    board = Board(height, width, to_win)
    current_token = Token.RED
    bots = {Token.RED: bot1, Token.YELLOW: bot2}

    while True:
        bot = bots[current_token]
        try:
            column = bot.play(board.copy(), current_token)
            board.play(column, current_token)
        except IllegalMove:
            if verbose:
                print(f"[{current_token.name}] played an illegal move. Match is a draw.")
            return None

        if verbose:
            print(f"{current_token.name} plays column {column}")
            print(board)
            print("-" * 20)
            time.sleep(0.2)

        if has_winner(board, current_token):
            if verbose:
                print(f"{current_token.name} wins.")
            return current_token

        if board_full(board):
            if verbose:
                print("Draw game.")
            return None

        current_token = Token.YELLOW if current_token == Token.RED else Token.RED


def main() -> None:
    result = play_match(MinimaxBot(), KelawinBot())
    print(f"Final result: {result.name if result else 'DRAW'}")


if __name__ == "__main__":
    main()
