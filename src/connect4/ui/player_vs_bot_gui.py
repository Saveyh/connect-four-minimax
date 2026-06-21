import tkinter as tk

from connect4.bots.kelawin_bot import KelawinBot
from connect4.core import Board, IllegalMove, Token, board_full, has_winner

CELL_SIZE = 80
PADDING = 10


class Connect4GUI:
    def __init__(self, root: tk.Tk, height: int = 6, width: int = 7, to_win: int = 4) -> None:
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
        self.bot = KelawinBot()
        self.accepting_input = True
        self.draw_board()

    def draw_board(self) -> None:
        self.canvas.delete("all")
        for row in range(self.height):
            for column in range(self.width):
                x0 = column * CELL_SIZE + PADDING
                y0 = row * CELL_SIZE + PADDING
                x1 = (column + 1) * CELL_SIZE - PADDING
                y1 = (row + 1) * CELL_SIZE - PADDING
                token = self.board.box(row, column)
                color = {
                    Token.EMPTY: "white",
                    Token.RED: "red",
                    Token.YELLOW: "yellow",
                }[token]
                self.canvas.create_oval(x0, y0, x1, y1, fill=color)

    def click_handler(self, event: tk.Event) -> None:
        if not self.accepting_input:
            return

        column = event.x // CELL_SIZE
        try:
            self.board.play(column, self.token_player)
        except IllegalMove:
            return

        self.accepting_input = False
        self.draw_board()
        if has_winner(self.board, self.token_player):
            self.end_game("You win!")
            return
        if board_full(self.board):
            self.end_game("Draw game.")
            return
        self.root.after(500, self.bot_move)

    def bot_move(self) -> None:
        try:
            column = self.bot.play(self.board.copy(), self.token_bot)
            self.board.play(column, self.token_bot)
            self.draw_board()
            if has_winner(self.board, self.token_bot):
                self.end_game("The bot wins!")
                return
            if board_full(self.board):
                self.end_game("Draw game.")
                return
            self.accepting_input = True
        except IllegalMove:
            self.end_game("Draw game.")

    def end_game(self, message: str) -> None:
        self.accepting_input = False
        self.canvas.unbind("<Button-1>")
        self.canvas.create_text(
            self.canvas.winfo_width() // 2,
            self.canvas.winfo_height() // 2,
            text=message,
            font=("Helvetica", 28),
            fill="white",
        )


def main() -> None:
    root = tk.Tk()
    root.title("Connect Four - Human vs Bot")
    Connect4GUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
