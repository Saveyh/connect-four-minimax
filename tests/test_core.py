import unittest

from connect4.core import Board, IllegalMove, Token, board_full, has_winner, legal_moves, opponent_of


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

    def test_has_winner_detects_diagonal_alignment(self) -> None:
        board = Board()
        board.play(0, Token.RED)
        board.play(1, Token.YELLOW)
        board.play(1, Token.RED)
        board.play(2, Token.YELLOW)
        board.play(2, Token.YELLOW)
        board.play(2, Token.RED)
        board.play(3, Token.YELLOW)
        board.play(3, Token.YELLOW)
        board.play(3, Token.YELLOW)
        board.play(3, Token.RED)

        self.assertTrue(has_winner(board, Token.RED))

    def test_board_full_reports_draw_state(self) -> None:
        board = Board(height=2, width=2, to_win=2)
        board.play(0, Token.RED)
        board.play(0, Token.YELLOW)
        board.play(1, Token.RED)
        board.play(1, Token.YELLOW)

        self.assertTrue(board_full(board))

    def test_play_rejects_out_of_bounds_column(self) -> None:
        board = Board()

        with self.assertRaises(IllegalMove):
            board.play(-1, Token.RED)

    def test_opponent_of_rejects_empty_token(self) -> None:
        with self.assertRaises(ValueError):
            opponent_of(Token.EMPTY)


if __name__ == "__main__":
    unittest.main()
