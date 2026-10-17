"""Local tools the study-planning agent can call (no network, no API keys)."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def tool_list_topics(data_dir: Path) -> list[str]:
    """Return available study topics (simulated course catalog)."""
    catalog = data_dir / "topics.json"
    if not catalog.exists():
        catalog.parent.mkdir(parents=True, exist_ok=True)
        default = ["Python basics", "Functions and modules", "Data structures"]
        catalog.write_text(json.dumps(default, indent=2) + "\n", encoding="utf-8")
    return json.loads(catalog.read_text(encoding="utf-8"))


def tool_pick_topic(topics: list[str], memory_steps: list[dict]) -> str:
    """Choose a topic not recently completed (rule-based)."""
    completed = {
        s.get("detail", {}).get("topic")
        for s in memory_steps
        if s.get("action") == "complete_session"
    }
    for topic in topics:
        if topic not in completed:
            return topic
    return topics[0]


def tool_write_study_plan(output_dir: Path, topic: str, duration_minutes: int) -> Path:
    """Create a study session plan file on disk."""
    output_dir.mkdir(parents=True, exist_ok=True)
    plan_path = output_dir / "study_session_plan.md"
    body = f"""# Study session plan

**Topic:** {topic}
**Duration:** {duration_minutes} minutes
**Created:** {utc_now_iso()}

## Objectives
- Review core concepts for {topic}
- Complete one short practice exercise

## Schedule
1. Warm-up (5 min): skim notes
2. Focus ({duration_minutes - 15} min): guided practice
3. Wrap-up (10 min): summarize key takeaways in your own words
"""
    plan_path.write_text(body, encoding="utf-8")
    return plan_path


def tool_append_session_log(output_dir: Path, topic: str, plan_path: Path) -> Path:
    """Append a line to a running session log (world-changing action)."""
    log_path = output_dir / "session_log.txt"
    line = f"{utc_now_iso()} | planned | {topic} | {plan_path.name}\n"
    with log_path.open("a", encoding="utf-8") as f:
        f.write(line)
    return log_path
