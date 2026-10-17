# Study planning agent (Week 1)

Course project for exploring **AI agent** fundamentals. This repo includes a small **mini agent simulator** you can run locally with no API keys.

## Mini agent demo

The `mini_agent` package is a rule-based study planner. It plans one study session end-to-end and writes files under `agent_output/`.

### Run

From the repository root:

```bash
python3 -m mini_agent
```

### Week-1 properties in this code

| Property | What it means here | Where to look |
|----------|-------------------|---------------|
| **Autonomy** | The agent picks its own next steps toward a fixed goal (load topics → choose topic → write plan) without asking the user at each step. | `mini_agent/agent.py` — `StudyPlannerAgent.run()` |
| **Tool use** | It calls plain Python functions that stand in for tools (catalog lookup, plan writer, log append). | `mini_agent/tools.py` |
| **Memory** | Every decision and tool call is appended to a JSON log that persists across runs. | `mini_agent/memory.py` → `agent_output/memory_log.json` |
| **Action** | It changes the world by creating/updating files (study plan, session log, topic catalog). | `agent_output/study_session_plan.md`, `session_log.txt` |

### Outputs

After a run you should see:

- `agent_output/memory_log.json` — step-by-step memory
- `agent_output/study_session_plan.md` — generated study session
- `agent_output/session_log.txt` — append-only log of planned sessions
- `mini_agent/data/topics.json` — created on first run if missing

### Tests

```bash
python3 -m unittest discover -s tests -v
```

## Other files

- `hi.py` — minimal placeholder from the initial repo scaffold.
