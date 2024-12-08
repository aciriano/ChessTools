from __future__ import annotations

from enum import Enum


class Color(Enum):
    WHITE = "white"
    BLACK = "black"


class Result(Enum):
    UNDEFINED = ""
    WHITE = "1-0"
    BLACK = "0-1"
    DRAW = "0.5-0.5"
