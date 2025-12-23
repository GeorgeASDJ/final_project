from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional, Tuple


class Mark(str, Enum):
    X = "X"
    O = "O"


Coord = Tuple[int, int]


@dataclass(frozen=True)
class Move:
    row: int
    col: int

    def as_coord(self) -> Coord:
        return (self.row, self.col)


def other(mark: Mark) -> Mark:
    return Mark.O if mark == Mark.X else Mark.X


@dataclass(frozen=True)
class GameConfig:
    size: int = 3
    win_k: Optional[int] = None

    def k(self) -> int:
        return self.win_k if self.win_k is not None else self.size
