from connect4.core import Board, Strategy, Token, has_winner, legal_moves, opponent_of, require_legal_moves


class KelawinBot(Strategy):
    """Main competitive bot combining tactical checks with deeper minimax."""

    def authors(self) -> str:
        return "Kay and Matteo"

    def play(self, current_board: Board, your_token: Token) -> int:
        moves = self._ordered_moves(current_board)
        opponent_token = opponent_of(your_token)

        for column in moves:
            if self._winning_move(current_board, your_token, column):
                return column

        for column in moves:
            if self._winning_move(current_board, opponent_token, column):
                return column

        best_column, _ = self._minimax(
            current_board,
            your_token,
            opponent_token,
            depth=6,
            alpha=float("-inf"),
            beta=float("inf"),
            maximizing=True,
        )
        return best_column

    def _winning_move(self, board: Board, token: Token, column: int) -> bool:
        candidate = board.copy()
        candidate.play(column, token)
        return has_winner(candidate, token)

    def _score_position(self, board: Board, token: Token, opponent_token: Token) -> int:
        score = board.column(board.width // 2).count(token) * 3

        for row in range(board.height):
            row_values = board.line(row)
            for column in range(board.width - 3):
                score += self._score_group(row_values[column:column + 4], token, opponent_token)

        for column in range(board.width):
            column_values = board.column(column)
            for row in range(board.height - 3):
                score += self._score_group(column_values[row:row + 4], token, opponent_token)

        for row in range(board.height - 3):
            for column in range(board.width - 3):
                score += self._score_group(
                    [board.box(row + offset, column + offset) for offset in range(4)],
                    token,
                    opponent_token,
                )

        for row in range(3, board.height):
            for column in range(board.width - 3):
                score += self._score_group(
                    [board.box(row - offset, column + offset) for offset in range(4)],
                    token,
                    opponent_token,
                )

        return score

    def _ordered_moves(self, board: Board) -> list[int]:
        moves = require_legal_moves(board)
        center = board.width // 2
        return sorted(moves, key=lambda column: abs(column - center))

    def _score_group(self, group: list[Token], token: Token, opponent_token: Token) -> int:
        token_count = group.count(token)
        opponent_count = group.count(opponent_token)
        empty_count = group.count(Token.EMPTY)

        score = 0
        if token_count == 4:
            score += 100
        elif token_count == 3 and empty_count == 1:
            score += 5
        elif token_count == 2 and empty_count == 2:
            score += 2

        if opponent_count == 3 and empty_count == 1:
            score -= 4

        return score

    def _minimax(
        self,
        board: Board,
        token: Token,
        opponent_token: Token,
        depth: int,
        alpha: float,
        beta: float,
        maximizing: bool,
    ) -> tuple[int, float]:
        if has_winner(board, token):
            return -1, float("inf")
        if has_winner(board, opponent_token):
            return -1, float("-inf")

        moves = legal_moves(board)
        if depth == 0 or not moves:
            return -1, float(self._score_position(board, token, opponent_token))

        best_column = moves[0]
        if maximizing:
            best_score = float("-inf")
            for column in self._ordered_moves(board):
                next_board = board.copy()
                next_board.play(column, token)
                _, score = self._minimax(next_board, token, opponent_token, depth - 1, alpha, beta, False)
                if score > best_score:
                    best_score = score
                    best_column = column
                alpha = max(alpha, score)
                if beta <= alpha:
                    break
            return best_column, best_score

        best_score = float("inf")
        for column in self._ordered_moves(board):
            next_board = board.copy()
            next_board.play(column, opponent_token)
            _, score = self._minimax(next_board, token, opponent_token, depth - 1, alpha, beta, True)
            if score < best_score:
                best_score = score
                best_column = column
            beta = min(beta, score)
            if beta <= alpha:
                break
        return best_column, best_score
