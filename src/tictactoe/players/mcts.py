from __future__ import annotations

import math
import random
from dataclasses import dataclass
from typing import Dict, Optional

from tictactoe.core.game import GameState
from tictactoe.core.types import Mark, Move
from tictactoe.players.base import Player


@dataclass
class Node:
    state: GameState
    parent: Optional["Node"]
    move: Optional[Move]
    visits: int = 0
    value_sum: float = 0.0
    children: Dict[Move, "Node"] = None

    def __post_init__(self) -> None:
        if self.children is None:
            self.children = {}

    def uct_score(self, child: "Node", c: float) -> float:
        if child.visits == 0:
            return float("inf")
        exploit = child.value_sum / child.visits
        explore = c * math.sqrt(math.log(self.visits) / child.visits)
        return exploit + explore


class MCTSBot(Player):
    def __init__(self, mark: Mark, iterations: int = 800, c: float = 1.4) -> None:
        super().__init__(mark)
        self.iterations = iterations
        self.c = c

    def choose_move(self, state: GameState) -> Move:
        root = Node(state=state, parent=None, move=None)

        for _ in range(self.iterations):
            leaf = self._select(root)
            expanded = self._expand(leaf)
            result = self._rollout(expanded.state)
            self._backprop(expanded, result)

        best = None
        best_visits = -1
        for m, ch in root.children.items():
            if ch.visits > best_visits:
                best_visits = ch.visits
                best = m
        if best is None:
            moves = state.board.available_moves()
            if not moves:
                raise ValueError("No moves")
            return random.choice(moves)
        return best

    def _select(self, node: Node) -> Node:
        cur = node
        while not cur.state.is_terminal() and cur.children:
            best_child = None
            best_score = -10**9
            for ch in cur.children.values():
                score = cur.uct_score(ch, self.c)
                if score > best_score:
                    best_score = score
                    best_child = ch
            cur = best_child if best_child is not None else cur
        return cur

    def _expand(self, node: Node) -> Node:
        if node.state.is_terminal():
            return node
        moves = node.state.board.available_moves()
        for m in moves:
            if m not in node.children:
                node.children[m] = Node(state=node.state.apply(m), parent=node, move=m)
                return node.children[m]
        return node

    def _rollout(self, state: GameState) -> float:
        cur = state
        while not cur.is_terminal():
            moves = cur.board.available_moves()
            cur = cur.apply(random.choice(moves))
        return cur.reward_for(self.mark)

    def _backprop(self, node: Node, reward: float) -> None:
        cur: Optional[Node] = node
        while cur is not None:
            cur.visits += 1
            cur.value_sum += reward
            cur = cur.parent
