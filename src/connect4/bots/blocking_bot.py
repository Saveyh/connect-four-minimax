import math
import random

from connect4.core import Board, Strategy, Token, has_winner, legal_moves, opponent_of

WINDOW_LENGTH = 4


class BlockingBot(Strategy):
    """Simple alpha-beta bot kept as an alternative baseline."""

    def authors(self) -> str:
        return "Project archive adaptation"

    def play(self, current_board: Board, your_token: Token) -> int:
        valid_moves = legal_moves(current_board)
        _, chosen_column = self._minimax(current_board, 4, float("-inf"), float("inf"), True, your_token)
        return chosen_column if chosen_column in valid_moves else random.choice(valid_moves)

    def _is_terminal(self, board: Board) -> bool:
        return has_winner(board, Token.RED) or has_winner(board, Token.YELLOW) or not legal_moves(board)

    def _minimax(
        self,
        board: Board,
        depth: int,
        alpha: float,
        beta: float,
        maximizing: bool,
        player_token: Token,
    ) -> tuple[float, int | None]:
        moves = legal_moves(board)
        opponent_token = opponent_of(player_token)

        if depth == 0 or self._is_terminal(board):
            if has_winner(board, player_token):
                return float("inf"), None
            if has_winner(board, opponent_token):
                return float("-inf"), None
            return float(self._score_position(board, player_token)), None

        if maximizing:
            best_score = -math.inf
            best_column = random.choice(moves)
            for column in moves:
                next_board = board.copy()
                next_board.play(column, player_token)
                score, _ = self._minimax(next_board, depth - 1, alpha, beta, False, player_token)
                if score > best_score:
                    best_score = score
                    best_column = column
                alpha = max(alpha, best_score)
                if alpha >= beta:
                    break
            return best_score, best_column

        best_score = math.inf
        best_column = random.choice(moves)
        for column in moves:
            next_board = board.copy()
            next_board.play(column, opponent_token)
            score, _ = self._minimax(next_board, depth - 1, alpha, beta, True, player_token)
            if score < best_score:
                best_score = score
                best_column = column
            beta = min(beta, best_score)
            if alpha >= beta:
                break
        return best_score, best_column

    def _score_position(self, board: Board, token: Token) -> int:
        score = board.column(board.width // 2).count(token) * 3
        for row in range(board.height):
            row_values = board.line(row)
            for column in range(board.width - 3):
                score += self._score_window(row_values[column:column + WINDOW_LENGTH], token)
        for column in range(board.width):
            column_values = board.column(column)
            for row in range(board.height - 3):
                score += self._score_window(column_values[row:row + WINDOW_LENGTH], token)
        for diagonal in board.diagonals():
            for start in range(len(diagonal) - 3):
                score += self._score_window(diagonal[start:start + WINDOW_LENGTH], token)
        return score

    def _score_window(self, window: list[Token], token: Token) -> int:
        opponent_token = opponent_of(token)
        score = 0
        if window.count(token) == 4:
            score += 100
        elif window.count(token) == 3 and window.count(Token.EMPTY) == 1:
            score += 5
        elif window.count(token) == 2 and window.count(Token.EMPTY) == 2:
            score += 2
        if window.count(opponent_token) == 3 and window.count(Token.EMPTY) == 1:
            score -= 4
        return score
