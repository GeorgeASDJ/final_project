from __future__ import annotations

import json
from pathlib import Path
from typing import Dict


def load_q_table(path: Path) -> Dict[str, Dict[str, float]]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def save_q_table(path: Path, q: Dict[str, Dict[str, float]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(q, ensure_ascii=False, indent=2), encoding="utf-8")
