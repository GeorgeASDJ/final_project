from __future__ import annotations

import random
from pathlib import Path
from typing import Dict, Tuple

from tictactoe.core.game import GameState
from tictactoe.core.types import Mark, Move
from tictactoe.players.base import Player
from tictactoe.training.serialize import load_q_table


def _state_key(state: GameState) -> str:
    return "|".join("".join(row) for row in state.board.as_tuple())


def _action_key(move: Move) -> str:
    return f"{move.row},{move.col}"


class QLearningBot(Player):
    def __init__(self, mark: Mark, model_path: Path, eps: float = 0.05) -> None:
        super().__init__(mark)
        self.q: Dict[str, Dict[str, float]] = load_q_table(model_path)
        self.eps = eps

    def choose_move(self, state: GameState) -> Move:
        if state.board.size != 3 or state.config.k() != 3:
            raise ValueError("QLearningBot supports only 3x3 with k=3")

        moves = state.board.available_moves()
        if not moves:
            raise ValueError("No moves")

        if random.random() < self.eps:
            return random.choice(moves)

        s = _state_key(state)
        qs = self.q.get(s, {})
        best = None
        best_val = -10**9
        for m in moves:
            a = _action_key(m)
            val = qs.get(a, 0.0)
            if val > best_val:
                best_val = val
                best = m
        return best if best is not None else random.choice(moves)
