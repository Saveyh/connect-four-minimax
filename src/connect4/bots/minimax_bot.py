from time import perf_counter

from connect4.core import Board, IllegalMove, Strategy, Token, has_winner, iter_lines, opponent_of, require_legal_moves

MAX_TIME_SECONDS = 1.0
WINDOW_LENGTH = 4


class MinimaxBot(Strategy):
    """Iterative deepening minimax bot with a lightweight evaluation."""

    def authors(self) -> str:
        return "Matteo"

    def play(self, current_board: Board, your_token: Token) -> int:
        start_time = perf_counter()
        opponent_token = opponent_of(your_token)
        best_move = self._ordered_moves(current_board)[0]

        immediate_win = self._winning_move(current_board, your_token)
        if immediate_win is not None:
            return immediate_win

        immediate_block = self._winning_move(current_board, opponent_token)
        if immediate_block is not None:
            return immediate_block

        def is_time_up() -> bool:
            return perf_counter() - start_time > MAX_TIME_SECONDS

        def evaluate(board: Board) -> int:
            return self._evaluate(board, your_token, opponent_token)

        def minimax(board: Board, depth: int, alpha: float, beta: float, maximizing: bool) -> tuple[float, int]:
            if has_winner(board, your_token):
                return float("inf"), -1
            if has_winner(board, opponent_token):
                return float("-inf"), -1
            if depth == 0 or is_time_up():
                return float(evaluate(board)), -1

            try:
                valid_moves = self._ordered_moves(board)
            except IllegalMove:
                return 0.0, -1

            chosen_column = valid_moves[0]
            if maximizing:
                best_score = float("-inf")
                for column in valid_moves:
                    next_board = board.copy()
                    next_board.play(column, your_token)
                    score, _ = minimax(next_board, depth - 1, alpha, beta, False)
                    if score > best_score:
                        best_score = score
                        chosen_column = column
                    alpha = max(alpha, score)
                    if beta <= alpha or is_time_up():
                        break
                return best_score, chosen_column

            best_score = float("inf")
            for column in valid_moves:
                next_board = board.copy()
                next_board.play(column, opponent_token)
                score, _ = minimax(next_board, depth - 1, alpha, beta, True)
                if score < best_score:
                    best_score = score
                    chosen_column = column
                beta = min(beta, score)
                if beta <= alpha or is_time_up():
                    break
            return best_score, chosen_column

        depth = 1
        while not is_time_up():
            _, move = minimax(current_board, depth, float("-inf"), float("inf"), True)
            if not is_time_up() and move != -1:
                best_move = move
            depth += 1

        return best_move

    def _winning_move(self, board: Board, token: Token) -> int | None:
        for column in self._ordered_moves(board):
            candidate = board.copy()
            candidate.play(column, token)
            if has_winner(candidate, token):
                return column
        return None

    def _ordered_moves(self, board: Board) -> list[int]:
        moves = require_legal_moves(board)
        center = board.width // 2
        return sorted(moves, key=lambda column: abs(column - center))

    def _evaluate(self, board: Board, token: Token, opponent_token: Token) -> int:
        score = board.column(board.width // 2).count(token) * 4
        for line in iter_lines(board):
            for start in range(len(line) - WINDOW_LENGTH + 1):
                score += self._score_window(line[start:start + WINDOW_LENGTH], token, opponent_token)
        return score

    def _score_window(self, window: list[Token], token: Token, opponent_token: Token) -> int:
        score = 0
        if window.count(token) == WINDOW_LENGTH:
            score += 10_000
        elif window.count(token) == WINDOW_LENGTH - 1 and window.count(Token.EMPTY) == 1:
            score += 120
        elif window.count(token) == WINDOW_LENGTH - 2 and window.count(Token.EMPTY) == 2:
            score += 12
        if window.count(opponent_token) == WINDOW_LENGTH - 1 and window.count(Token.EMPTY) == 1:
            score -= 100
        return score
