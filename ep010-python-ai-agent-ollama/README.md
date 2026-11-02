# ep010 · Build an AI agent in Python from scratch (Ollama, no framework)

From the skill.md video **"Build an AI Agent in Python From Scratch: Right Math, Wrong Answer"** (Nov 3, 2026):
https://www.youtube.com/watch?v=2enB3D-byoc

Channel: **skill.md** — https://www.youtube.com/channel/UCMQcMb_sp9gmMCYzhHRaS8g

An AI agent is a model in a loop with tools. This folder is the whole agent: one Python file, four tools
(`get_today`, `calculate`, `days_until`, `read_file`), the official `ollama` package, and a local model.

## What's in this folder
| File | What it is |
|---|---|
| `agent.py` | The final agent (58 lines). Model `qwen3:1.7b`, 4 tools, loop with error feedback + step limit. |
| `agent_v1_coder.py` … `agent_v8_days_until.py` | Every version from the video, in order, so you can re-run each mistake. |
| `no_tools.py` | The baseline: ask for today's date with no tools. |
| `notes/todo.txt` | The to-do list the agent reads (`read_file` only works inside `notes/`). |
| `run-log.md` | The real terminal output of each run in the video. |

## Run it
```bash
# 1. Install Ollama: https://ollama.com/download , then:
ollama pull qwen3:1.7b

# 2. Python environment + the official client (MIT)
python3 -m venv .venv
.venv/bin/pip install ollama

# 3. Ask your agent
.venv/bin/python agent.py "What is the date today?"
.venv/bin/python agent.py "Read todo.txt. Which task is due first, and how many days from today is that?"
```
Run it from this folder (it reads `notes/`). The due dates in `todo.txt` were set for Nov 2, 2026 — change them to dates near your "today".

## The 4 mistakes (and fixes) from the video
1. **qwen2.5-coder:3b typed the tool call as text** (a JSON block) instead of making a real tool call → we switched to `qwen3:1.7b`.
2. **Made-up arguments** (`get_today(today='2023-10-05')`), even with a system prompt → the loop now drops arguments the function doesn't have (`inspect.signature`).
3. **Dates fed into the calculator** → answered 21 days (real answer: 4) → added a date tool (`days_until`).
4. **Right numbers, wrong answer** — tool results were just `"4"`, `"17"`, `"25"` → `days_until` now returns `"2026-11-06 is 4 days from today"`. 3 of 3 runs correct after that.

Also tested: `read_file("../../../../etc/hosts")` is refused by the path check; thinking mode (`think=True`) took ~90 s and guessed the date, so it's off.

## Licenses
- This folder: MIT (see repo LICENSE).
- `ollama` Python package: MIT. Ollama: MIT.
- `qwen3:1.7b`: Apache 2.0. `qwen2.5-coder:3b` (only used in v1): Qwen Research License — check it before any commercial use.
- Docs we followed: https://docs.ollama.com/capabilities/tool-calling

## Credit
The hands-on, show-every-step style of our tutorials is inspired by FreeAIVault (https://www.youtube.com/@FreeAIVaultTV).
