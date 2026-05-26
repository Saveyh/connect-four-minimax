import secrets

from connect4.core import Board, Strategy, Token, legal_moves


class RandomBot(Strategy):
    """Baseline strategy that always plays a legal random move."""

    def authors(self) -> str:
        return "Sebastien Vaucher"

    def play(self, current_board: Board, your_token: Token) -> int:
        del your_token
        return secrets.choice(legal_moves(current_board))
