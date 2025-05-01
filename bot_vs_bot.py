from interfaces import Board, Token, IllegalMove
from minimax_bot import MinimaxBot
from BOT_FINAL import Kelawin
from copy import deepcopy

import time

def play_match(bot1, bot2, height=6, width=7, to_win=4, verbose=True):
    board = Board(height, width, to_win)
    current_token = Token.RED
    bots = {Token.RED: bot1, Token.YELLOW: bot2}

    while True:
        bot = bots[current_token]
        try:
            col = bot.play(deepcopy(board), current_token)

            board.play(col, current_token)
        except IllegalMove:
            if verbose:
                print(f"[{current_token.name}] Coup illégal. Match nul.")
            return None

        if verbose:
            print(f"{current_token.name} joue en colonne {col}")
            for row in range(height):
                print(" ".join(board.box(row, col).name[0] for col in range(width)))
            print("-" * 20)
            time.sleep(0.2)

        # Vérification de la victoire
        if check_winner(board, current_token, to_win):
            if verbose:
                print(f"🏆 {current_token.name} gagne !")
            return current_token

        # Match nul (plateau plein)
        if all(board.box(0, c) != Token.EMPTY for c in range(width)):
            if verbose:
                print("Match nul.")
            return None

        # Changement de joueur
        current_token = Token.YELLOW if current_token == Token.RED else Token.RED

def check_winner(board, token: Token, to_win) -> bool:
    def has_consecutive(sequence):
        count = 0
        for t in sequence:
            if t == token:
                count += 1
                if count >= to_win:
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

if __name__ == "__main__":
    bot1 = MinimaxBot()
    bot2 = Kelawin()
    result = play_match(bot1, bot2)
