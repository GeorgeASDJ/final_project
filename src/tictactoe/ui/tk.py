from __future__ import annotations

import tkinter as tk
from dataclasses import dataclass
from pathlib import Path
from tkinter import messagebox
from typing import Optional

from tictactoe.core.game import GameState, new_game
from tictactoe.core.types import Mark, Move
from tictactoe.players.base import Player
from tictactoe.players.mcts import MCTSBot
from tictactoe.players.qlearning import QLearningBot


@dataclass
class TkSetup:
    size: int = 3
    win_k: Optional[int] = None
    bot: str = "mcts"


class TkApp:
    def __init__(self, root: tk.Tk, setup: TkSetup) -> None:
        self.root = root
        self.setup = setup
        self.state: GameState = new_game(setup.size, setup.win_k)
        self.human_mark = Mark.X
        self.bot_mark = Mark.O
        self.bot: Player = self._make_bot(setup.bot)
        self.buttons: list[list[tk.Button]] = []
        self.bot_delay_ms = 100
        self._bot_thinking = False
        self._build()

    def _make_bot(self, name: str) -> Player:
        if name == "mcts":
            return MCTSBot(self.bot_mark, iterations=600)
        if name == "q":
            return QLearningBot(self.bot_mark, model_path=Path("data/q_table.json"))
        raise ValueError("Unknown bot")

    def _build(self) -> None:
        self.root.title("Tic-Tac-Toe AI")
        frm = tk.Frame(self.root)
        frm.pack(padx=10, pady=10)

        for r in range(self.state.board.size):
            row_btns: list[tk.Button] = []
            for c in range(self.state.board.size):
                b = tk.Button(
                    frm,
                    text="",
                    width=4,
                    height=2,
                    command=lambda rr=r, cc=c: self.on_click(rr, cc),
                )
                b.grid(row=r, column=c, padx=2, pady=2)
                row_btns.append(b)
            self.buttons.append(row_btns)

    def on_click(self, r: int, c: int) -> None:
        if self.state.is_terminal():
            return
        if self._bot_thinking:
            return
        if self.state.to_move != self.human_mark:
            return

        move = Move(r, c)
        if not self.state.board.in_bounds(move) or not self.state.board.is_empty_at(move):
            return

        self.state = self.state.apply(move)
        self._sync_ui()

        if self.state.is_terminal():
            self._finish()
            return
        if self.state.to_move == self.bot_mark:
            self._bot_thinking = True
            self._set_buttons_state("disabled")
            self.root.after(self.bot_delay_ms, self._bot_move)


        move = Move(r, c)
        if not self.state.board.in_bounds(move) or not self.state.board.is_empty_at(move):
            return

        self.state = self.state.apply(move)
        self._sync_ui()

        if self.state.is_terminal():
            self._finish()
            return

        if self.state.to_move == self.bot_mark:
            try:
                bm = self.bot.choose_move(self.state)
            except Exception:
                bm = self.state.board.available_moves()[0]
            self.state = self.state.apply(bm)
            self._sync_ui()

        if self.state.is_terminal():
            self._finish()

    def _sync_ui(self) -> None:
        for r in range(self.state.board.size):
            for c in range(self.state.board.size):
                v = self.state.board.grid[r][c]
                self.buttons[r][c]["text"] = "" if v is None else v.value

    def reset_game(self) -> None:
        self.state = new_game(self.setup.size, self.setup.win_k)
        self._bot_thinking = False
        self._sync_ui()

    def _finish(self) -> None:
        w = self.state.winner()
        if w is None:
            messagebox.showinfo("Result", "DRAW")
        else:
            messagebox.showinfo("Result", f"WINNER: {w.value}")
        self.reset_game()

    def _set_buttons_state(self, state: str) -> None:
        for row in self.buttons:
            for b in row:
                b["state"] = state

    def _bot_move(self) -> None:
        if self.state.is_terminal():
            self._bot_thinking = False
            self._set_buttons_state("normal")
            return

        if self.state.to_move != self.bot_mark:
            self._bot_thinking = False
            self._set_buttons_state("normal")
            return

        try:
            bm = self.bot.choose_move(self.state)
        except Exception:
            moves = self.state.board.available_moves()
            bm = moves[0]

        self.state = self.state.apply(bm)
        self._sync_ui()

        self._bot_thinking = False
        self._set_buttons_state("normal")

        if self.state.is_terminal():
            self._finish()



def run_tk(size: int = 3, win_k: Optional[int] = None, bot: str = "mcts") -> None:
    root = tk.Tk()
    app = TkApp(root, TkSetup(size=size, win_k=win_k, bot=bot))
    app._sync_ui()
    root.mainloop()
