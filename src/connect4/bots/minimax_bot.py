import time

from connect4.core import Board, Strategy, Token, legal_moves, opponent_of

MAX_TIME_SECONDS = 1.0


class MinimaxBot(Strategy):
    """Iterative deepening minimax bot with a lightweight evaluation."""

    def authors(self) -> str:
        return "Matteo"

    def play(self, current_board: Board, your_token: Token) -> int:
        start_time = time.time()
        opponent_token = opponent_of(your_token)
        best_move = legal_moves(current_board)[0]

        def is_time_up() -> bool:
            return time.time() - start_time > MAX_TIME_SECONDS

        def evaluate(board: Board) -> int:
            return self._count_sequences(board, your_token, 4) - self._count_sequences(board, opponent_token, 4)

        def minimax(board: Board, depth: int, alpha: float, beta: float, maximizing: bool) -> tuple[float, int]:
            if depth == 0 or is_time_up():
                return float(evaluate(board)), -1

            valid_moves = legal_moves(board)
            if not valid_moves:
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

    def _count_sequences(self, board: Board, token: Token, length: int) -> int:
        score = 0
        lines = [board.line(index) for index in range(board.height)]
        lines.extend(board.column(index) for index in range(board.width))
        lines.extend(board.diagonals())

        for line in lines:
            for start in range(len(line) - length + 1):
                window = line[start:start + length]
                if window.count(token) == length and window.count(Token.EMPTY) == 0:
                    score += 1000
                elif window.count(token) == length and Token.EMPTY in window:
                    score += 10 ** length
        return score
