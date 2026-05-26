import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from connect4.core import Board, Token, has_winner, legal_moves


class BoardTests(unittest.TestCase):
    def test_play_stacks_tokens_from_bottom(self) -> None:
        board = Board()
        board.play(0, Token.RED)
        board.play(0, Token.YELLOW)

        self.assertEqual(board.box(5, 0), Token.RED)
        self.assertEqual(board.box(4, 0), Token.YELLOW)

    def test_has_winner_detects_horizontal_alignment(self) -> None:
        board = Board()
        for column in range(4):
            board.play(column, Token.RED)

        self.assertTrue(has_winner(board, Token.RED))

    def test_legal_moves_excludes_full_columns(self) -> None:
        board = Board(height=2, width=2, to_win=2)
        board.play(0, Token.RED)
        board.play(0, Token.YELLOW)

        self.assertEqual(legal_moves(board), [1])


if __name__ == "__main__":
    unittest.main()
