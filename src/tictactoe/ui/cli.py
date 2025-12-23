from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from tictactoe.core.game import GameState, new_game
from tictactoe.core.types import Mark, other
from tictactoe.players.base import Player
from tictactoe.players.human import HumanCLI
from tictactoe.players.mcts import MCTSBot
from tictactoe.players.qlearning import QLearningBot


@dataclass
class GameSetup:
    size: int
    win_k: Optional[int]
    p_x: Player
    p_o: Player


def _make_player(kind: str, mark: Mark) -> Player:
    if kind == "human":
        return HumanCLI(mark)
    if kind == "mcts":
        return MCTSBot(mark, iterations=800)
    if kind == "q":
        return QLearningBot(mark, model_path=Path("data/q_table.json"))
    raise ValueError("Unknown player kind")


def make_setup(size: int, win_k: Optional[int], x_kind: str, o_kind: str) -> GameSetup:
    return GameSetup(
        size=size,
        win_k=win_k,
        p_x=_make_player(x_kind, Mark.X),
        p_o=_make_player(o_kind, Mark.O),
    )


def play(setup: GameSetup) -> Mark | None:
    state: GameState = new_game(setup.size, setup.win_k)
    players = {Mark.X: setup.p_x, Mark.O: setup.p_o}

    while not state.is_terminal():
        print()
        print(state.board)
        p = players[state.to_move]
        move = p.choose_move(state)
        state = state.apply(move)

    print()
    print(state.board)
    w = state.winner()
    if w is None:
        print("DRAW")
    else:
        print(f"WINNER: {w.value}")
    return w
