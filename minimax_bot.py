import time
from interfaces import Strategy, Board, Token, IllegalMove

MAX_TIME = 1.0  # secondes

class MinimaxBot(Strategy):
    def authors(self):
        return "Matteo"

    def play(self, current_board: Board, your_token: Token) -> int:
        start_time = time.time()
        opponent_token = Token.RED if your_token == Token.YELLOW else Token.YELLOW

        def is_time_up():
            return time.time() - start_time > MAX_TIME

        def evaluate(board: Board) -> int:
            def count_sequences(token: Token, length: int) -> int:
                count = 0
                lines = []
                lines.extend(board.line(i) for i in range(board.height))
                lines.extend(board.column(i) for i in range(board.width))
                lines.extend(board.diagonals())
                for line in lines:
                    for i in range(len(line) - length + 1):
                        window = line[i:i + length]
                        if window.count(token) == length and window.count(Token.EMPTY) == 0:
                            count += 1000  # victoire certaine
                        elif window.count(token) == length and Token.EMPTY in window:
                            count += 10 ** length
                return count

            return count_sequences(your_token, 4) - count_sequences(opponent_token, 4)

        def minimax(board: Board, depth: int, alpha: int, beta: int, maximizing: bool) -> tuple[int, int]:
            if depth == 0 or is_time_up():
                return evaluate(board), -1

            valid_moves = [c for c in range(board.width) if Token.EMPTY in board.column(c)]
            if not valid_moves:
                return 0, -1

            best_col = valid_moves[0]
            if maximizing:
                max_eval = float('-inf')
                for col in valid_moves:
                    new_board = clone_board(board)
                    try:
                        new_board.play(col, your_token)
                        eval, _ = minimax(new_board, depth - 1, alpha, beta, False)
                        if eval > max_eval:
                            max_eval = eval
                            best_col = col
                        alpha = max(alpha, eval)
                        if beta <= alpha or is_time_up():
                            break
                    except IllegalMove:
                        continue
                return max_eval, best_col
            else:
                min_eval = float('inf')
                for col in valid_moves:
                    new_board = clone_board(board)
                    try:
                        new_board.play(col, opponent_token)
                        eval, _ = minimax(new_board, depth - 1, alpha, beta, True)
                        if eval < min_eval:
                            min_eval = eval
                            best_col = col
                        beta = min(beta, eval)
                        if beta <= alpha or is_time_up():
                            break
                    except IllegalMove:
                        continue
                return min_eval, best_col

        # essaie plusieurs profondeurs tant que le temps le permet
        best_score = float('-inf')
        best_move = -1
        depth = 1
        while not is_time_up():
            score, move = minimax(current_board, depth, float('-inf'), float('inf'), True)
            if not is_time_up():
                best_score = score
                best_move = move
                depth += 1

        return best_move


def clone_board(board: Board) -> Board:
    new_board = Board(board.height, board.width, board.to_win)
    for row in range(board.height):
        for col in range(board.width):
            token = board.box(row, col)
            if token != Token.EMPTY:
                new_board._Board__board[row][col] = token  # accès privé (pas recommandé mais fonctionnel ici)
    return new_board
