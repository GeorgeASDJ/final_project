from __future__ import annotations

import argparse

from tictactoe.ui.cli import make_setup, play
from tictactoe.ui.tk import run_tk


def main() -> None:
    parser = argparse.ArgumentParser(prog="tictactoe")
    parser.add_argument("--ui", choices=["cli", "tk"], default="cli")
    parser.add_argument("--size", type=int, default=3)
    parser.add_argument("--k", type=int, default=0)
    parser.add_argument("--x", choices=["human", "mcts", "q"], default="human")
    parser.add_argument("--o", choices=["human", "mcts", "q"], default="mcts")
    args = parser.parse_args()
    win_k = args.size if args.k == 0 else args.k

    if win_k < 3:
        raise SystemExit("Error: --k must be >= 3")
    if win_k > args.size:
        raise SystemExit("Error: --k must be <= --size")

    win_k = None if args.k == 0 else args.k

    if args.ui == "tk":
        run_tk(size=args.size, win_k=win_k, bot=args.o)
        return

    setup = make_setup(size=args.size, win_k=win_k, x_kind=args.x, o_kind=args.o)
    play(setup)


if __name__ == "__main__":
    main()
