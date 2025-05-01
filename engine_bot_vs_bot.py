import tkinter as tk
from interfaces import Board, Token, IllegalMove
from minimax_bot import MinimaxBot
from BOT_FINAL import Kelawin
from copy import deepcopy


CELL_SIZE = 80
PADDING = 10
DELAY = 500  # délai en ms entre les coups

class Connect4BotVsBotGUI:
    def __init__(self, root, height=6, width=7, to_win=4):
        self.root = root
        self.board = Board(height, width, to_win)
        self.height = height
        self.width = width
        self.to_win = to_win
        self.canvas = tk.Canvas(root, width=width * CELL_SIZE, height=height * CELL_SIZE, bg="blue")
        self.canvas.pack()
        self.token_bot1 = Token.RED
        self.token_bot2 = Token.YELLOW
        self.bot1 = MinimaxBot()
        self.bot2 = Kelawin()
        self.current_token = self.token_bot1
        self.draw_board()
        self.root.after(DELAY, self.play_turn)

    def draw_board(self):
        self.canvas.delete("all")
        for row in range(self.height):
            for col in range(self.width):
                x0 = col * CELL_SIZE + PADDING
                y0 = row * CELL_SIZE + PADDING
                x1 = (col + 1) * CELL_SIZE - PADDING
                y1 = (row + 1) * CELL_SIZE - PADDING
                token = self.board.box(row, col)
                color = {
                    Token.EMPTY: "white",
                    Token.RED: "red",
                    Token.YELLOW: "yellow"
                }[token]
                self.canvas.create_oval(x0, y0, x1, y1, fill=color)

    def play_turn(self):
        if self.current_token == self.token_bot1:
            bot = self.bot1
        else:
            bot = self.bot2

        try:
            col = bot.play(deepcopy(self.board), self.current_token)

            self.board.play(col, self.current_token)
        except IllegalMove:
            self.end_game("Coup illégal joué. Match nul.")
            return

        self.draw_board()

        if self.check_winner(self.current_token):
            gagnant = "Bot 1 (Rouge)" if self.current_token == self.token_bot1 else "Bot 2 (Jaune)"
            self.end_game(f"{gagnant} a gagné 🎉 !")
            return

        if all(self.board.box(0, c) != Token.EMPTY for c in range(self.width)):
            self.end_game("Match nul !")
            return

        self.current_token = self.token_bot2 if self.current_token == self.token_bot1 else self.token_bot1
        self.root.after(DELAY, self.play_turn)

    def check_winner(self, token: Token) -> bool:
        def has_consecutive(sequence):
            count = 0
            for t in sequence:
                if t == token:
                    count += 1
                    if count >= self.to_win:
                        return True
                else:
                    count = 0
            return False

        for row in range(self.height):
            if has_consecutive(self.board.line(row)):
                return True
        for col in range(self.width):
            if has_consecutive(self.board.column(col)):
                return True
        for diag in self.board.diagonals():
            if has_consecutive(diag):
                return True
        return False

    def end_game(self, message):
        self.canvas.create_text(self.canvas.winfo_width() // 2,
                                self.canvas.winfo_height() // 2,
                                text=message, font=("Helvetica", 32), fill="white")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Puissance 4 - Bot vs Bot")
    game = Connect4BotVsBotGUI(root)
    root.mainloop()
