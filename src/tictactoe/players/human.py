from __future__ import annotations

from tictactoe.core.game import GameState
from tictactoe.core.types import Move
from tictactoe.players.base import Player


class HumanCLI(Player):
    def choose_move(self, state: GameState) -> Move:
        moves = state.board.available_moves()
        allowed = {(m.row, m.col) for m in moves}

        while True:
            raw = input(f"Player {self.mark.value} move (row col): ").strip()
            parts = raw.split()
            if len(parts) != 2:
                print("Enter two ints: row col")
                continue
            try:
                r = int(parts[0])
                c = int(parts[1])
            except ValueError:
                print("Not ints")
                continue
            if (r, c) not in allowed:
                print("Illegal move")
                continue
            return Move(r, c)
