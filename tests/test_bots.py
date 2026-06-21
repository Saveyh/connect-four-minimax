import unittest

from connect4.bots.kelawin_bot import KelawinBot
from connect4.bots.minimax_bot_v2 import MinimaxBotV2
from connect4.bots.random_bot import RandomBot
from connect4.core import Board, IllegalMove, Token


class BotTests(unittest.TestCase):
    def test_random_bot_raises_when_no_moves_are_available(self) -> None:
        board = Board(height=1, width=2, to_win=2)
        board.play(0, Token.RED)
        board.play(1, Token.YELLOW)

        with self.assertRaises(IllegalMove):
            RandomBot().play(board, Token.YELLOW)

    def test_kelawin_bot_takes_immediate_winning_move(self) -> None:
        board = Board()
        board.play(0, Token.RED)
        board.play(1, Token.RED)
        board.play(2, Token.RED)

        self.assertEqual(KelawinBot().play(board, Token.RED), 3)

    def test_minimax_v2_blocks_immediate_loss(self) -> None:
        board = Board()
        board.play(0, Token.RED)
        board.play(1, Token.RED)
        board.play(2, Token.RED)

        self.assertEqual(MinimaxBotV2().play(board, Token.YELLOW), 3)


if __name__ == "__main__":
    unittest.main()
