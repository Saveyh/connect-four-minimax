import time

from connect4.core import Board, Strategy, Token, has_winner, legal_moves, opponent_of

MAX_TIME_SECONDS = 1.0


class MinimaxBotV2(Strategy):
    """Improved minimax bot that prioritizes urgent wins and blocks."""

    def authors(self) -> str:
        return "Matteo"

    def play(self, current_board: Board, your_token: Token) -> int:
        start_time = time.time()
        opponent_token = opponent_of(your_token)

        immediate_win = self._winning_move(current_board, your_token)
        if immediate_win is not None:
            return immediate_win

        immediate_block = self._winning_move(current_board, opponent_token)
        if immediate_block is not None:
            return immediate_block

        best_move = legal_moves(current_board)[0]
        depth = 1
        while time.time() - start_time <= MAX_TIME_SECONDS:
            _, move = self._minimax(
                current_board,
                your_token,
                opponent_token,
                depth,
                float("-inf"),
                float("inf"),
                True,
                start_time,
            )
            if time.time() - start_time <= MAX_TIME_SECONDS and move is not None:
                best_move = move
            depth += 1
        return best_move

    def _winning_move(self, board: Board, token: Token) -> int | None:
        for column in legal_moves(board):
            candidate = board.copy()
            candidate.play(column, token)
            if has_winner(candidate, token):
                return column
        return None

    def _minimax(
        self,
        board: Board,
        your_token: Token,
        opponent_token: Token,
        depth: int,
        alpha: float,
        beta: float,
        maximizing: bool,
        start_time: float,
    ) -> tuple[float, int | None]:
        if depth == 0 or time.time() - start_time > MAX_TIME_SECONDS:
            return float(self._evaluate(board, your_token)), None

        valid_moves = legal_moves(board)
        if not valid_moves:
            return 0.0, None

        best_move = valid_moves[0]
        if maximizing:
            value = float("-inf")
            for column in valid_moves:
                next_board = board.copy()
                next_board.play(column, your_token)
                score, _ = self._minimax(
                    next_board,
                    your_token,
                    opponent_token,
                    depth - 1,
                    alpha,
                    beta,
                    False,
                    start_time,
                )
                if score > value:
                    value = score
                    best_move = column
                alpha = max(alpha, value)
                if beta <= alpha or time.time() - start_time > MAX_TIME_SECONDS:
                    break
            return value, best_move

        value = float("inf")
        for column in valid_moves:
            next_board = board.copy()
            next_board.play(column, opponent_token)
            score, _ = self._minimax(
                next_board,
                your_token,
                opponent_token,
                depth - 1,
                alpha,
                beta,
                True,
                start_time,
            )
            if score < value:
                value = score
                best_move = column
            beta = min(beta, value)
            if beta <= alpha or time.time() - start_time > MAX_TIME_SECONDS:
                break
        return value, best_move

    def _evaluate(self, board: Board, token: Token) -> int:
        score = board.column(board.width // 2).count(token) * 6
        lines = [board.line(index) for index in range(board.height)]
        lines.extend(board.column(index) for index in range(board.width))
        lines.extend(board.diagonals())

        for line in lines:
            for start in range(len(line) - 3):
                score += self._score_window(line[start:start + 4], token)
        return score

    def _score_window(self, window: list[Token], token: Token) -> int:
        opponent_token = opponent_of(token)
        score = 0
        if window.count(token) == 4:
            score += 10_000
        elif window.count(token) == 3 and window.count(Token.EMPTY) == 1:
            score += 100
        elif window.count(token) == 2 and window.count(Token.EMPTY) == 2:
            score += 10
        if window.count(opponent_token) == 3 and window.count(Token.EMPTY) == 1:
            score -= 80
        return score
