from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from tictactoe.core.board import Board
from tictactoe.core.types import GameConfig, Mark, Move, other


@dataclass
class GameState:
    board: Board
    to_move: Mark
    config: GameConfig

    def winner(self) -> Optional[Mark]:
        return self.board.winner(self.config.k())

    def is_terminal(self) -> bool:
        return self.winner() is not None or self.board.is_full()

    def apply(self, move: Move) -> "GameState":
        new_board = self.board.copy()
        new_board.place(move, self.to_move)
        return GameState(board=new_board, to_move=other(self.to_move), config=self.config)

    def reward_for(self, player: Mark) -> float:
        w = self.winner()
        if w is None:
            return 0.0
        return 1.0 if w == player else -1.0


def new_game(size: int = 3, win_k: Optional[int] = None) -> GameState:
    cfg = GameConfig(size=size, win_k=win_k)
    return GameState(board=Board.empty(size), to_move=Mark.X, config=cfg)
