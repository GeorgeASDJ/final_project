from tictactoe.core.game import new_game
from tictactoe.core.types import Move


def test_win_row_3x3():
    s = new_game(3, 3)
    s = s.apply(Move(0, 0))
    s = s.apply(Move(1, 0))
    s = s.apply(Move(0, 1))
    s = s.apply(Move(1, 1))
    s = s.apply(Move(0, 2))
    assert s.winner() is not None
    assert s.is_terminal()
