from __future__ import annotations

import abc
from dataclasses import dataclass
from functools import cached_property

from chess_tools.game.enums import Color


__all__ = ("ChessPiece", "King", "Queen", "Rook", "Knight", "Bishop", "Pawn")


@dataclass
class ChessPiece(abc.ABC):
    color: Color
    value: float
    symbol: str

    @cached_property
    def name(self) -> str:
        return self.__class__.__name__

    @property
    @abc.abstractmethod
    def icon(self) -> str:
        raise NotImplementedError

    # @abc.abstractmethod
    # def reachable_squares(self, square: Square, dimension: int) -> list[Square]:
    #     raise NotImplementedError


class King(ChessPiece):
    def __init__(self, color: Color) -> None:
        super().__init__(color=color, value=4.0, symbol="K")

    @property
    def icon(self) -> str:
        return "♔" if self.color is Color.WHITE else "♚"


class Queen(ChessPiece):
    def __init__(self, color: Color) -> None:
        super().__init__(color=color, value=9.0, symbol="Q")

    @property
    def icon(self) -> str:
        return "♕" if self.color is Color.WHITE else "♛"


class Rook(ChessPiece):
    def __init__(self, color: Color) -> None:
        super().__init__(color=color, value=5.0, symbol="R")

    @property
    def icon(self) -> str:
        return "♖" if self.color is Color.WHITE else "♜"


class Knight(ChessPiece):
    def __init__(self, color: Color) -> None:
        super().__init__(color=color, value=3.0, symbol="N")

    @property
    def icon(self) -> str:
        return "♘" if self.color is Color.WHITE else "♞"


class Bishop(ChessPiece):
    def __init__(self, color: Color) -> None:
        super().__init__(color=color, value=3.0, symbol="B")

    @property
    def icon(self) -> str:
        return "♗" if self.color is Color.WHITE else "♝"


class Pawn(ChessPiece):
    def __init__(self, color: Color) -> None:
        super().__init__(color=color, value=1.0, symbol="")

    @property
    def icon(self) -> str:
        return "♙" if self.color is Color.WHITE else "♟"
