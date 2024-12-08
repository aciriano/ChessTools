from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field
from functools import cached_property

from chess_tools.exceptions import ChessToolsException
from chess_tools.game.enums import Color
from chess_tools.game.piece import ChessPiece

__all__ = ("Square", "Board")


@dataclass
class Square:
    col: int
    row: int

    def __hash__(self) -> int:
        return hash((self.col, self.row))

    def __post_init__(self) -> None:
        """
        Validates that the square's row and column indices are integers greater
        than or equal to 1.

        Raises:
            TypeError: If row or col is not of type int.
            ChessToolsException: If row or col is less than 1.
        """
        if not all([isinstance(i, int) for i in (self.row, self.col)]):
            raise TypeError(f"{self.__class__.__name__}: Row and column must be of type int.")
        if self.row < 1 or self.col < 1:
            raise ChessToolsException(
                f"{self.__class__.__name__}: Row and column must be greater than or equal to 1."
            )

    @cached_property
    def color(self) -> Color:
        """
        Determines the color of the square based on its position.

        The color alternates in a chessboard pattern, starting with white at (1,1).

        Returns:
            Color: The color of the square (WHITE or BLACK).
        """
        return Color.WHITE if (self.row + self.col) % 2 else Color.BLACK

    @cached_property
    def notation(self) -> str:
        """
        Computes the square's position in algebraic notation.

        Returns:
            str: The square's algebraic notation (e.g., 'a1', 'h8').
        """
        return f"{'abcdefgh'[self.col - 1]}{self.row}"


@dataclass
class Board:
    dimension: int
    squares: dict[Square, ChessPiece] = field(init=False)

    def __post_init__(self) -> None:
        if not isinstance(self.dimension, int) or self.dimension < 1:
            raise ChessToolsException(f"Value {self.dimension} is not valid as board dimension.")
        else:
            self.squares = dict()

    def put(self, piece: ChessPiece, square: Square) -> None:
        if not isinstance(piece, ChessPiece) or not isinstance(square, Square):
            raise TypeError(
                f"{self.__class__.__name__}: put function expects a ChessPiece and a "
                f"Square objects. Received: {type(piece).__name__}, {type(square).__name__}."
            )
        elif square in self.squares:
            raise ChessToolsException(f"Square {square} is currently occupied.")
        else:
            self.squares[square] = piece

    def remove(self, square: Square) -> None:
        if not isinstance(square, Square):
            raise TypeError(
                f"{self.__class__.__name__}: remove function expects a Square object. "
                f"Received: {type(square).__name__}."
            )
        elif square not in self.squares:
            raise ChessToolsException(f"Square {square} is not occupied.")
        else:
            del self.squares[square]
