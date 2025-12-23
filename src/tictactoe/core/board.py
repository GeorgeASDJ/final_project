from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Optional, Sequence, Tuple

from tictactoe.core.types import Mark, Move


@dataclass
class Board:
    size: int
    grid: List[List[Optional[Mark]]]

    @classmethod
    def empty(cls, size: int) -> "Board":
        return cls(size=size, grid=[[None for _ in range(size)] for _ in range(size)])

    def copy(self) -> "Board":
        return Board(self.size, [row[:] for row in self.grid])

    def in_bounds(self, move: Move) -> bool:
        return 0 <= move.row < self.size and 0 <= move.col < self.size

    def is_empty_at(self, move: Move) -> bool:
        return self.grid[move.row][move.col] is None

    def place(self, move: Move, mark: Mark) -> None:
        if not self.in_bounds(move):
            raise ValueError("Move out of bounds")
        if not self.is_empty_at(move):
            raise ValueError("Cell is not empty")
        self.grid[move.row][move.col] = mark

    def available_moves(self) -> List[Move]:
        moves: List[Move] = []
        for r in range(self.size):
            for c in range(self.size):
                if self.grid[r][c] is None:
                    moves.append(Move(r, c))
        return moves

    def is_full(self) -> bool:
        return all(cell is not None for row in self.grid for cell in row)

    def as_tuple(self) -> Tuple[Tuple[str, ...], ...]:
        def cell_to_str(x: Optional[Mark]) -> str:
            return x.value if x is not None else "."

        return tuple(tuple(cell_to_str(c) for c in row) for row in self.grid)

    def __str__(self) -> str:
        rows = []
        for r in range(self.size):
            rows.append(" ".join("." if c is None else c.value for c in self.grid[r]))
        return "\n".join(rows)

    def _lines(self, win_k: int) -> Iterable[Sequence[Optional[Mark]]]:
        n = self.size
        k = win_k

        for r in range(n):
            for c in range(n - k + 1):
                yield [self.grid[r][c + i] for i in range(k)]

        for c in range(n):
            for r in range(n - k + 1):
                yield [self.grid[r + i][c] for i in range(k)]

        for r in range(n - k + 1):
            for c in range(n - k + 1):
                yield [self.grid[r + i][c + i] for i in range(k)]

        for r in range(n - k + 1):
            for c in range(k - 1, n):
                yield [self.grid[r + i][c - i] for i in range(k)]

    def winner(self, win_k: int) -> Optional[Mark]:
        for line in self._lines(win_k):
            if line[0] is None:
                continue
            if all(cell == line[0] for cell in line):
                return line[0]
        return None
