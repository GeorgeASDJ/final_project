from __future__ import annotations

from abc import ABC, abstractmethod

from tictactoe.core.game import GameState
from tictactoe.core.types import Mark, Move


class Player(ABC):
    def __init__(self, mark: Mark) -> None:
        self.mark = mark

    @abstractmethod
    def choose_move(self, state: GameState) -> Move:
        raise NotImplementedError
