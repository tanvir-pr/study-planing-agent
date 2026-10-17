"""Rule-based study planner demonstrating week-1 agent properties."""

from __future__ import annotations

from pathlib import Path

from mini_agent.memory import MemoryStore
from mini_agent.tools import (
    tool_append_session_log,
    tool_list_topics,
    tool_pick_topic,
    tool_write_study_plan,
)

DEFAULT_GOAL = "Plan an autonomous study session for the course"
SESSION_MINUTES = 45


class StudyPlannerAgent:
    """
    Autonomous loop: decides the next action from goal + memory until the plan exists.
    Uses tools for catalog lookup and file writes; memory persists every step.
    """

    def __init__(self, project_root: Path) -> None:
        self.project_root = project_root
        self.data_dir = project_root / "mini_agent" / "data"
        self.output_dir = project_root / "agent_output"
        self.memory = MemoryStore(self.output_dir / "memory_log.json")

    def run(self, goal: str = DEFAULT_GOAL) -> Path:
        self.memory.load()
        run_id = self.memory.start_run(goal)
        self.memory.record(run_id, "start", {"goal": goal})

        # Autonomy: agent chooses its own sequence (no interactive prompts).
        self.memory.record(run_id, "decide", {"next": "load_topics"})
        topics = tool_list_topics(self.data_dir)
        self.memory.record(run_id, "tool_use", {"tool": "list_topics", "count": len(topics)})

        self.memory.record(run_id, "decide", {"next": "pick_topic"})
        topic = tool_pick_topic(topics, self.memory.steps)
        self.memory.record(run_id, "decide", {"chosen_topic": topic})

        self.memory.record(run_id, "decide", {"next": "write_plan"})
        plan_path = tool_write_study_plan(self.output_dir, topic, SESSION_MINUTES)
        self.memory.record(
            run_id,
            "tool_use",
            {"tool": "write_study_plan", "path": str(plan_path.relative_to(self.project_root))},
        )

        log_path = tool_append_session_log(self.output_dir, topic, plan_path)
        self.memory.record(
            run_id,
            "action",
            {"effect": "appended_session_log", "path": str(log_path.relative_to(self.project_root))},
        )

        self.memory.record(run_id, "complete_session", {"topic": topic})
        self.memory.save()
        return plan_path
