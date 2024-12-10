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

    @cached_property
    def icon(self) -> str:
        """
        Determines a visual representation of the square based on its color.

        Returns:
            str: A Unicode character representing the square's color.
        """
        return "◻" if self.color is Color.WHITE else "◼"


@dataclass
class Board:
    """
    Represents a chessboard with a given dimension and manages the placement
    of chess pieces on its squares.

    Attributes:
        dimension (int): The size of the chessboard (e.g., 8 for an 8x8 board).
        squares (dict[Square, ChessPiece]): A mapping of squares to the chess pieces
            currently occupying them. This is initialized as an empty dictionary.
    """

    dimension: int
    squares: dict[Square, ChessPiece] = field(init=False)

    def __post_init__(self) -> None:
        """
        Validates the board's dimension and initializes the squares dictionary.

        Raises:
            ChessToolsException: If the dimension is not a positive integer.
        """
        if not isinstance(self.dimension, int) or self.dimension < 1:
            raise ChessToolsException(f"Value {self.dimension} is not valid as board dimension.")
        else:
            self.squares = dict()

    def put(self, piece: ChessPiece, square: Square) -> None:
        """
        Places a chess piece on the specified square.

        Args:
            piece (ChessPiece): The chess piece to place on the board.
            square (Square): The square where the piece will be placed.

        Raises:
            TypeError: If `piece` is not a ChessPiece or `square` is not a Square.
            ChessToolsException: If the square is already occupied.
        """
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
        """
        Removes the chess piece from the specified square.

        Args:
            square (Square): The square from which to remove the piece.

        Raises:
            TypeError: If `square` is not a Square.
            ChessToolsException: If the square is not occupied.
        """
        if not isinstance(square, Square):
            raise TypeError(
                f"{self.__class__.__name__}: remove function expects a Square object. "
                f"Received: {type(square).__name__}."
            )
        elif square not in self.squares:
            raise ChessToolsException(f"Square {square} is not occupied.")
        else:
            del self.squares[square]
