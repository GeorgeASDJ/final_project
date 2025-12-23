from __future__ import annotations

import csv
import random
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional

from tictactoe.core.game import GameState, new_game
from tictactoe.core.types import Mark, Move, other
from tictactoe.training.serialize import save_q_table


def _state_key(state: GameState) -> str:
    return "|".join("".join(row) for row in state.board.as_tuple())


def _action_key(move: Move) -> str:
    return f"{move.row},{move.col}"


@dataclass
class QParams:
    alpha: float = 0.2
    gamma: float = 0.95
    eps: float = 0.2


class QTrainer:
    def __init__(self, params: QParams) -> None:
        self.params = params
        self.q: Dict[str, Dict[str, float]] = {}

    def _get(self, s: str, a: str) -> float:
        return self.q.get(s, {}).get(a, 0.0)

    def _set(self, s: str, a: str, v: float) -> None:
        self.q.setdefault(s, {})[a] = v

    def _best_next(self, state: GameState) -> float:
        moves = state.board.available_moves()
        if not moves:
            return 0.0
        s = _state_key(state)
        return max(self._get(s, _action_key(m)) for m in moves)

    def _policy(self, state: GameState) -> Move:
        moves = state.board.available_moves()
        if random.random() < self.params.eps:
            return random.choice(moves)
        s = _state_key(state)
        best_m = None
        best_v = -10**9
        for m in moves:
            v = self._get(s, _action_key(m))
            if v > best_v:
                best_v = v
                best_m = m
        return best_m if best_m is not None else random.choice(moves)

    def train_selfplay(
        self, episodes: int, log_csv: Optional[Path] = None
    ) -> Dict[str, Dict[str, float]]:
        rows: List[List[str]] = []
        for ep in range(episodes):
            state = new_game(3, 3)
            history: List[tuple[str, str, Mark]] = []

            while not state.is_terminal():
                s = _state_key(state)
                m = self._policy(state)
                a = _action_key(m)
                history.append((s, a, state.to_move))
                state = state.apply(m)

            winner = state.winner()
            for s, a, who in history:
                reward = 0.0
                if winner is not None:
                    reward = 1.0 if winner == who else -1.0

                old = self._get(s, a)
                next_val = 0.0
                new = old + self.params.alpha * (reward + self.params.gamma * next_val - old)
                self._set(s, a, new)

            if log_csv is not None:
                rows.append([str(ep), winner.value if winner else "DRAW"])

        if log_csv is not None:
            log_csv.parent.mkdir(parents=True, exist_ok=True)
            with log_csv.open("w", newline="", encoding="utf-8") as f:
                w = csv.writer(f)
                w.writerow(["episode", "result"])
                w.writerows(rows)

        return self.q


def main() -> None:
    out = Path("data/q_table.json")
    log = Path("data/q_learning_selfplay.csv")
    trainer = QTrainer(QParams())
    q = trainer.train_selfplay(episodes=30000, log_csv=log)
    save_q_table(out, q)
    print(f"Saved: {out}")


if __name__ == "__main__":
    main()
