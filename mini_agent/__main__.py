"""Run with: python -m mini_agent"""

from pathlib import Path

from mini_agent.agent import StudyPlannerAgent


def main() -> None:
    root = Path(__file__).resolve().parent.parent
    agent = StudyPlannerAgent(root)
    plan = agent.run()
    print("Study planner agent finished.")
    print(f"  Plan file: {plan}")
    print(f"  Memory log: {root / 'agent_output' / 'memory_log.json'}")


if __name__ == "__main__":
    main()
