import json
import shutil
import tempfile
import unittest
from pathlib import Path

from mini_agent.agent import StudyPlannerAgent


class TestStudyPlannerAgent(unittest.TestCase):
    def test_run_creates_plan_and_memory(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "mini_agent").mkdir()
            agent = StudyPlannerAgent(root)
            plan = agent.run(goal="Test goal")
            self.assertTrue(plan.exists())
            memory_path = root / "agent_output" / "memory_log.json"
            self.assertTrue(memory_path.exists())
            data = json.loads(memory_path.read_text(encoding="utf-8"))
            actions = [s["action"] for s in data["steps"]]
            self.assertIn("tool_use", actions)
            self.assertIn("complete_session", actions)

    def test_memory_persists_across_runs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "mini_agent").mkdir()
            agent = StudyPlannerAgent(root)
            agent.run()
            agent2 = StudyPlannerAgent(root)
            agent2.memory.load()
            self.assertEqual(len(agent2.memory.steps), len(agent.memory.steps))
            agent2.run()
            agent2.memory.load()
            self.assertGreater(len(agent2.memory.steps), len(agent.memory.steps))


if __name__ == "__main__":
    unittest.main()
