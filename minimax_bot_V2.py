import time
from interfaces import Strategy, Board, Token, IllegalMove

MAX_TIME = 1.0

class MinimaxBotV2(Strategy):
    def authors(self):
        return "Matteo"

    def play(self, current_board: Board, your_token: Token) -> int:
        start = time.time()
        opponent_token = Token.RED if your_token == Token.YELLOW else Token.YELLOW

        def is_time_up():
            return time.time() - start > MAX_TIME

        def clone_board(board: Board) -> Board:
            new_board = Board(board.height, board.width, board.to_win)
            for i in range(board.height):
                for j in range(board.width):
                    new_board._Board__board[i][j] = board.box(i, j)
            return new_board

        def winning_move(board: Board, token: Token) -> int | None:
            for col in range(board.width):
                if Token.EMPTY not in board.column(col):
                    continue
                test_board = clone_board(board)
                try:
                    test_board.play(col, token)
                    if check_winner(test_board, token):
                        return col
                except IllegalMove:
                    continue
            return None

        def score_window(window: list[Token], token: Token) -> int:
            opp_token = Token.RED if token == Token.YELLOW else Token.YELLOW
            score = 0
            if window.count(token) == 4:
                score += 10000
            elif window.count(token) == 3 and window.count(Token.EMPTY) == 1:
                score += 100
            elif window.count(token) == 2 and window.count(Token.EMPTY) == 2:
                score += 10
            if window.count(opp_token) == 3 and window.count(Token.EMPTY) == 1:
                score -= 80
            return score

        def evaluate(board: Board, token: Token) -> int:
            score = 0
            center = board.column(board.width // 2)
            score += center.count(token) * 6

            lines = [board.line(i) for i in range(board.height)] + \
                    [board.column(i) for i in range(board.width)] + \
                    list(board.diagonals())

            for line in lines:
                for i in range(len(line) - 3):
                    window = line[i:i + 4]
                    score += score_window(window, token)
            return score

        def minimax(board: Board, depth, alpha, beta, maximizing):
            if depth == 0 or is_time_up():
                return evaluate(board, your_token), None

            valid_moves = [c for c in range(board.width) if Token.EMPTY in board.column(c)]
            best_move = valid_moves[0] if valid_moves else None

            if maximizing:
                value = float("-inf")
                for col in valid_moves:
                    new_board = clone_board(board)
                    try:
                        new_board.play(col, your_token)
                        new_score, _ = minimax(new_board, depth - 1, alpha, beta, False)
                        if new_score > value:
                            value = new_score
                            best_move = col
                        alpha = max(alpha, value)
                        if beta <= alpha or is_time_up():
                            break
                    except IllegalMove:
                        continue
                return value, best_move
            else:
                value = float("inf")
                for col in valid_moves:
                    new_board = clone_board(board)
                    try:
                        new_board.play(col, opponent_token)
                        new_score, _ = minimax(new_board, depth - 1, alpha, beta, True)
                        if new_score < value:
                            value = new_score
                            best_move = col
                        beta = min(beta, value)
                        if beta <= alpha or is_time_up():
                            break
                    except IllegalMove:
                        continue
                return value, best_move

        # 1. Gagne si possible
        win_now = winning_move(current_board, your_token)
        if win_now is not None:
            return win_now

        # 2. Bloque si l’adversaire peut gagner
        block = winning_move(current_board, opponent_token)
        if block is not None:
            return block

        # 3. Minimax adaptatif
        best_move = -1
        depth = 1
        while not is_time_up():
            _, move = minimax(current_board, depth, float('-inf'), float('inf'), True)
            if not is_time_up() and move is not None:
                best_move = move
            depth += 1

        return best_move


def check_winner(board: Board, token: Token) -> bool:
    def has_consecutive(seq):
        count = 0
        for t in seq:
            if t == token:
                count += 1
                if count >= board.to_win:
                    return True
            else:
                count = 0
        return False

    for row in range(board.height):
        if has_consecutive(board.line(row)):
            return True
    for col in range(board.width):
        if has_consecutive(board.column(col)):
            return True
    for diag in board.diagonals():
        if has_consecutive(diag):
            return True
    return False
