import random
import math
from interfaces import Board, Token, Strategy  # Assure-toi que les imports soient corrects


WINDOW_LENGTH = 4


class MyStrategy(Strategy):
    def authors(self) -> str:
        return "Ton Nom"

    def play(self, current_board: Board, your_token: Token) -> int:
        valid_locations = self.get_valid_locations(current_board)
        _, column = self.minimax(current_board, 4, -math.inf, math.inf, True, your_token)
        return column if column in valid_locations else random.choice(valid_locations)

    def get_valid_locations(self, board: Board) -> list[int]:
        return [c for c in range(board.width) if board.column(c).count(Token.EMPTY) > 0]

    def is_terminal_node(self, board: Board) -> bool:
        return self.winning_move(board, Token.RED) or self.winning_move(board, Token.YELLOW) or len(self.get_valid_locations(board)) == 0

    def winning_move(self, board: Board, piece: Token) -> bool:
        # Check horizontal
        for r in range(board.height):
            row = board.line(r)
            for c in range(board.width - 3):
                if row[c:c+4].count(piece) == 4:
                    return True

        # Check vertical
        for c in range(board.width):
            col = board.column(c)
            for r in range(board.height - 3):
                if col[r:r+4].count(piece) == 4:
                    return True

        # Diagonals
        for diag in board.diagonals():
            for i in range(len(diag) - 3):
                if diag[i:i+4].count(piece) == 4:
                    return True
        return False

    def minimax(self, board: Board, depth: int, alpha: float, beta: float, maximizingPlayer: bool, player_piece: Token) -> tuple[int, float]:
        valid_locations = self.get_valid_locations(board)
        opponent_piece = Token.RED if player_piece == Token.YELLOW else Token.YELLOW
        is_terminal = self.is_terminal_node(board)

        if depth == 0 or is_terminal:
            if is_terminal:
                if self.winning_move(board, player_piece):
                    return (None, float("inf"))
                elif self.winning_move(board, opponent_piece):
                    return (None, float("-inf"))
                else:
                    return (None, 0)
            else:
                return (None, self.score_position(board, player_piece))

        if maximizingPlayer:
            value = -math.inf
            best_col = random.choice(valid_locations)
            for col in valid_locations:
                try:
                    new_board = self.copy_board(board)
                    new_board.play(col, player_piece)
                    new_score = self.minimax(new_board, depth - 1, alpha, beta, False, player_piece)[1]
                    if new_score > value:
                        value = new_score
                        best_col = col
                    alpha = max(alpha, value)
                    if alpha >= beta:
                        break
                except:
                    continue
            return best_col, value
        else:
            value = math.inf
            best_col = random.choice(valid_locations)
            for col in valid_locations:
                try:
                    new_board = self.copy_board(board)
                    new_board.play(col, opponent_piece)
                    new_score = self.minimax(new_board, depth - 1, alpha, beta, True, player_piece)[1]
                    if new_score < value:
                        value = new_score
                        best_col = col
                    beta = min(beta, value)
                    if alpha >= beta:
                        break
                except:
                    continue
            return best_col, value

    def score_position(self, board: Board, piece: Token) -> int:
        score = 0
        center_column = board.column(board.width // 2)
        score += center_column.count(piece) * 3

        # Horizontal
        for r in range(board.height):
            row = board.line(r)
            for c in range(board.width - 3):
                window = row[c:c + WINDOW_LENGTH]
                score += self.evaluate_window(window, piece)

        # Vertical
        for c in range(board.width):
            col = board.column(c)
            for r in range(board.height - 3):
                window = col[r:r + WINDOW_LENGTH]
                score += self.evaluate_window(window, piece)

        # Diagonals
        for diag in board.diagonals():
            for i in range(len(diag) - 3):
                window = diag[i:i + WINDOW_LENGTH]
                score += self.evaluate_window(window, piece)

        return score

    def evaluate_window(self, window: list[Token], piece: Token) -> int:
        score = 0
        opp_piece = Token.RED if piece == Token.YELLOW else Token.YELLOW

        if window.count(piece) == 4:
            score += 100
        elif window.count(piece) == 3 and window.count(Token.EMPTY) == 1:
            score += 5
        elif window.count(piece) == 2 and window.count(Token.EMPTY) == 2:
            score += 2
        if window.count(opp_piece) == 3 and window.count(Token.EMPTY) == 1:
            score -= 4

        return score

    def copy_board(self, board: Board) -> Board:
        new_board = Board(board.height, board.width, board.to_win)
        for r in range(board.height):
            for c in range(board.width):
                token = board.box(r, c)
                if token != Token.EMPTY:
                    new_board._Board__board[r][c] = token
        return new_board
