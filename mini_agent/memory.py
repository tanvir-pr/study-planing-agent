"""Persistent memory across agent steps and runs."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from mini_agent.tools import utc_now_iso


class MemoryStore:
    def __init__(self, path: Path) -> None:
        self.path = path
        self._data: dict[str, Any] = {"runs": [], "steps": []}

    def load(self) -> None:
        if self.path.exists():
            self._data = json.loads(self.path.read_text(encoding="utf-8"))

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(self._data, indent=2) + "\n", encoding="utf-8")

    @property
    def steps(self) -> list[dict[str, Any]]:
        return self._data["steps"]

    def start_run(self, goal: str) -> str:
        run_id = f"run-{len(self._data['runs']) + 1}"
        self._data["runs"].append(
            {"id": run_id, "goal": goal, "started_at": utc_now_iso()}
        )
        return run_id

    def record(self, run_id: str, action: str, detail: dict[str, Any] | None = None) -> None:
        self._data["steps"].append(
            {
                "run_id": run_id,
                "timestamp": utc_now_iso(),
                "action": action,
                "detail": detail or {},
            }
        )
