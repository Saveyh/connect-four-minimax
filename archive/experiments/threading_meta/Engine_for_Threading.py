import threading
import tkinter as tk
from interfaces import Board, Token, IllegalMove
from random_strategy import RandomStrategy
from minimax_bot import MinimaxBot
from thread_bot import MinimaxBotV3  # Utiliser MinimaxBotV3 ici

CELL_SIZE = 80
PADDING = 10


class Connect4GUI:
    def __init__(self, root, height=6, width=7, to_win=4):
        self.root = root
        self.board = Board(height, width, to_win)
        self.height = height
        self.width = width
        self.to_win = to_win
        self.canvas = tk.Canvas(root, width=width * CELL_SIZE, height=height * CELL_SIZE, bg="blue")
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.click_handler)
        self.token_player = Token.RED
        self.token_bot = Token.YELLOW
        self.bot = MinimaxBotV3()  # Instancier le nouveau bot avec réflexion anticipée
        self.draw_board()
        self.bot_thread = None
        self._stop_thinking = threading.Event()

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

    def click_handler(self, event):
        col = event.x // CELL_SIZE
        try:
            self.board.play(col, self.token_player)
        except IllegalMove:
            return
        self.draw_board()
        if self.check_winner(self.token_player):
            self.end_game("Tu as gagné 🎉 !")
            return

        # Notify the bot that the player has made a move, start background thinking
        self.bot.notify_opponent_move(self.board, self.token_bot)

        # Schedule bot's move after a short delay (to allow time for thinking)
        self.root.after(500, self.bot_move)

    def bot_move(self):
        try:
            col = self.bot.play(self.board, self.token_bot)
            self.board.play(col, self.token_bot)
            self.draw_board()
            if self.check_winner(self.token_bot):
                self.end_game("Le bot a gagné 🤖 !")
        except IllegalMove:
            self.end_game("Match nul !")

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
        self.canvas.unbind("<Button-1>")
        self.canvas.create_text(self.canvas.winfo_width() // 2,
                                self.canvas.winfo_height() // 2,
                                text=message, font=("Helvetica", 32), fill="white")


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Puissance 4 - VS Bot")
    game = Connect4GUI(root)
    root.mainloop()
