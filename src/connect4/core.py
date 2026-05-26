from __future__ import annotations

from abc import ABC, abstractmethod
from copy import deepcopy
from enum import Enum
from typing import Iterable


class Token(Enum):
    EMPTY = "."
    RED = "R"
    YELLOW = "Y"


class IllegalMove(Exception):
    """Raised when a move cannot be played on the current board."""


class Board:
    def __init__(self, height: int = 6, width: int = 7, to_win: int = 4) -> None:
        self.height = height
        self.width = width
        self.to_win = to_win
        self.__board = [[Token.EMPTY for _ in range(width)] for _ in range(height)]

    def __repr__(self) -> str:
        return "\n".join(" ".join(token.value for token in row) for row in self.__board)

    def box(self, line_index: int, column_index: int) -> Token:
        return self.__board[line_index][column_index]

    def line(self, index: int) -> list[Token]:
        return list(self.__board[index])

    def column(self, index: int) -> list[Token]:
        return [row[index] for row in self.__board]

    def diagonals(self) -> Iterable[list[Token]]:
        for diagonal_index in range(self.width + self.height - 1):
            yield [
                self.__board[row_index][column_index]
                for row_index, column_index in zip(
                    range(diagonal_index, -1, -1),
                    range(0, diagonal_index + 1),
                )
                if row_index < self.height and column_index < self.width
            ]
            yield [
                self.__board[row_index][column_index]
                for row_index, column_index in zip(
                    range(diagonal_index, -1, -1),
                    range(self.width - 1, self.width - diagonal_index - 2, -1),
                )
                if row_index < self.height and column_index >= 0
            ]

    def play(self, column_index: int, token: Token) -> None:
        if column_index < 0 or column_index >= self.width:
            raise IllegalMove("Column is out of bounds.")

        column = self.column(column_index)
        try:
            drop_height = self.height - 1 - column[::-1].index(Token.EMPTY)
        except ValueError as error:
            raise IllegalMove("Column is already full.") from error
        self.__board[drop_height][column_index] = token

    def copy(self) -> "Board":
        return deepcopy(self)


class Strategy(ABC):
    @abstractmethod
    def authors(self) -> str:
        """Return the author name(s) for this strategy."""

    @abstractmethod
    def play(self, current_board: Board, your_token: Token) -> int:
        """Choose the column index to play."""


def opponent_of(token: Token) -> Token:
    return Token.RED if token == Token.YELLOW else Token.YELLOW


def legal_moves(board: Board) -> list[int]:
    return [column for column in range(board.width) if Token.EMPTY in board.column(column)]


def board_full(board: Board) -> bool:
    return not legal_moves(board)


def has_winner(board: Board, token: Token) -> bool:
    def has_consecutive(sequence: list[Token]) -> bool:
        count = 0
        for current in sequence:
            if current == token:
                count += 1
                if count >= board.to_win:
                    return True
            else:
                count = 0
        return False

    for row in range(board.height):
        if has_consecutive(board.line(row)):
            return True
    for column in range(board.width):
        if has_consecutive(board.column(column)):
            return True
    for diagonal in board.diagonals():
        if has_consecutive(diagonal):
            return True
    return False
