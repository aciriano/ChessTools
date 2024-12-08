from __future__ import annotations

from typing import Any

import pytest

from chess_tools.exceptions import ChessToolsException
from chess_tools.game.board import Board
from chess_tools.game.board import Square
from chess_tools.game.enums import Color
from chess_tools.game.piece import ChessPiece


class TestSquare:
    """Test suite for the Square class."""

    def test_initialization(self):
        """Test basic initialization of Square."""
        square = Square(row=1, col=1)
        assert square.row == 1
        assert square.col == 1
        assert square.color == Color.BLACK

    @pytest.mark.parametrize("col, row", [(0, 1), (1, 0)])
    def test_invalid_value(self, col: Any, row: Any):
        """Test invalid initializations for Square objects."""
        with pytest.raises(ChessToolsException):
            Square(col=col, row=row)

    @pytest.mark.parametrize("col, row", [(1, ""), ("", 1)])
    def test_invalid_type(self, col: Any, row: Any):
        """Test invalid initializations for Square objects."""
        with pytest.raises(TypeError):
            Square(col=col, row=row)

    @pytest.mark.parametrize("row, col, expected", [(1, 1, Color.BLACK), (1, 2, Color.WHITE)])
    def test_color(self, row: int, col: int, expected: Color):
        """Test the color calculation for different positions."""
        assert Square(col=col, row=row).color == expected

    @pytest.mark.parametrize("col, row, notation", [(1, 1, "a1"), (8, 1, "h1"), (7, 7, "g7")])
    def test_notation(self, col: int, row: int, notation: str) -> None:
        """Test the algebraic notation representation of Square."""
        Square(row=row, col=col).notation == notation


class MockPiece(ChessPiece):
    def __init__(self, color: Color):
        super().__init__(value=0.0, symbol="M", color=color)

    def get_moves(self) -> list:
        return []


class TestBoard:
    @pytest.fixture
    def board(self):
        """Fixture to create a new chess board."""
        return Board(dimension=8)

    @pytest.fixture
    def square(self):
        """Fixture to create a default square."""
        return Square(row=1, col=1)

    @pytest.fixture
    def piece(self):
        """Fixture to create a generic chess piece."""
        return MockPiece(color=Color.WHITE)

    def test_board_initialization(self, board: Board):
        """Test board initialization with valid dimensions."""
        assert board.dimension == 8
        assert isinstance(board.squares, dict)
        assert len(board.squares) == 0

    @pytest.mark.parametrize("dimension", [0, "invalid"])
    def test_invalid_board_initialization(self, dimension: Any):
        """Test board initialization with invalid dimensions."""
        with pytest.raises(ChessToolsException):
            Board(dimension=dimension)

    def test_put_piece_on_empty_square(self, board: Board, piece: MockPiece, square: Square):
        """Test placing a piece on an empty square."""
        board.put(piece, square)
        assert board.squares[square] == piece

    def test_put_piece_on_occupied_square(self, board, piece, square):
        """Test placing a piece on an already occupied square."""
        board.put(piece, square)
        with pytest.raises(ChessToolsException):
            board.put(piece, square)

    def test_put_invalid_piece_or_square(self, board):
        """Test placing an invalid piece or on an invalid square."""
        with pytest.raises(TypeError):
            board.put("invalid_piece", Square(1, 1))

        with pytest.raises(TypeError):
            board.put(ChessPiece(color=Color.WHITE), "invalid_square")

    def test_remove_piece_from_occupied_square(
        self, board: Board, piece: MockPiece, square: Square
    ):
        """Test removing a piece from an occupied square."""
        board.put(piece, square)
        board.remove(square)
        assert square not in board.squares

    def test_remove_piece_from_empty_square(self, board, square):
        """Test removing a piece from an empty square."""
        with pytest.raises(ChessToolsException):
            board.remove(square)

    def test_remove_with_invalid_square(self, board):
        """Test removing a piece using an invalid square."""
        with pytest.raises(TypeError):
            board.remove("invalid_square")
