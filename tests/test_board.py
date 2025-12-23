import pytest

from tictactoe.core.board import Board
from tictactoe.core.types import Mark, Move


def test_place_and_available_moves():
    b = Board.empty(3)
    assert len(b.available_moves()) == 9
    b.place(Move(0, 0), Mark.X)
    assert len(b.available_moves()) == 8
    assert b.grid[0][0] == Mark.X


def test_illegal_move():
    b = Board.empty(3)
    b.place(Move(0, 0), Mark.X)
    with pytest.raises(ValueError):
        b.place(Move(0, 0), Mark.O)
