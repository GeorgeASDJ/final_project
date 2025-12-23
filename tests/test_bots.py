from pathlib import Path

import pytest

from tictactoe.core.game import new_game
from tictactoe.core.types import Mark
from tictactoe.players.mcts import MCTSBot
from tictactoe.players.qlearning import QLearningBot


def test_mcts_chooses_legal_move():
    s = new_game(3, 3)
    bot = MCTSBot(Mark.X, iterations=50)
    m = bot.choose_move(s)
    assert s.board.in_bounds(m)
    assert s.board.is_empty_at(m)


def test_qlearning_requires_3x3(tmp_path: Path):
    model = tmp_path / "q.json"
    model.write_text("{}", encoding="utf-8")
    bot = QLearningBot(Mark.X, model_path=model)
    s = new_game(4, 4)
    with pytest.raises(ValueError):
        bot.choose_move(s)
