import tkinter as tk

from connect4.bots.kelawin_bot import KelawinBot
from connect4.bots.minimax_bot import MinimaxBot
from connect4.core import Board, IllegalMove, Token, board_full, has_winner

CELL_SIZE = 80
PADDING = 10
DELAY_MS = 500


class Connect4BotVsBotGUI:
    def __init__(self, root: tk.Tk, height: int = 6, width: int = 7, to_win: int = 4) -> None:
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
        self.bot2 = KelawinBot()
        self.current_token = self.token_bot1
        self.draw_board()
        self.root.after(DELAY_MS, self.play_turn)

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

    def play_turn(self) -> None:
        bot = self.bot1 if self.current_token == self.token_bot1 else self.bot2

        try:
            column = bot.play(self.board.copy(), self.current_token)
            self.board.play(column, self.current_token)
        except IllegalMove:
            self.end_game("Illegal move played. Draw game.")
            return

        self.draw_board()

        if has_winner(self.board, self.current_token):
            winner = "Bot 1 (Red)" if self.current_token == self.token_bot1 else "Bot 2 (Yellow)"
            self.end_game(f"{winner} wins!")
            return

        if board_full(self.board):
            self.end_game("Draw game.")
            return

        self.current_token = self.token_bot2 if self.current_token == self.token_bot1 else self.token_bot1
        self.root.after(DELAY_MS, self.play_turn)

    def end_game(self, message: str) -> None:
        self.canvas.create_text(
            self.canvas.winfo_width() // 2,
            self.canvas.winfo_height() // 2,
            text=message,
            font=("Helvetica", 28),
            fill="white",
        )


def main() -> None:
    root = tk.Tk()
    root.title("Connect Four - Bot vs Bot")
    Connect4BotVsBotGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
