# ep011 · Claude Code subagents vs agent teams vs skills (real runs)

From the skill.md video **"Claude Code Subagents vs Agent Teams: Same Answer, 9x the Tokens"** (Nov 4, 2026):
https://www.youtube.com/watch?v=7kIfoTmPArs

Channel: **skill.md** — https://www.youtube.com/channel/UCMQcMb_sp9gmMCYzhHRaS8g

One question ("find the first ERROR in server.log") asked three ways: a single Claude Code session, with a subagent,
and with an experimental agent team. Same answer every time. Input tokens reported by Claude Code: **84,449** (single
session), **42,430** (subagent, asked by name), **778,572** (agent team, which then got stuck trying to shut its team down).

## What's in this folder
| File | What it is |
|---|---|
| `.claude/agents/log-scout.md` | The read-only subagent from the video (`Read, Grep, Glob`). |
| `make_log.py` | Generates the 3,000-line test `server.log` (seed 11, one ERROR at line 2418). |
| `run.sh` | Every command from the video, in order (r1–r6). |
| `show.jq` | The jq filter that turns `--output-format stream-json` into the readable lines on screen. |
| `run-log.md` | The real output of r1–r6 (condensed by show.jq). |

## Setup we used (free)
- Claude Code **2.1.92** pointed at **Ollama 0.30.11** (`ANTHROPIC_BASE_URL=http://localhost:11434`), model `gemma4:31b-cloud`
  (Ollama free plan) — see https://docs.ollama.com/integrations/claude-code. **Not a Claude model**, so token counts are
  for this setup only, one run each.
- An empty, throwaway `CLAUDE_CONFIG_DIR`, so none of your own settings, skills or agents load.

## What happened
1. **r2** — `log-scout` was available and its description says "Use proactively", but Claude ran Grep itself.
2. **r3** — asked by name, it delegated. Main session turn: 23,480 input tokens; the subagent's first turn: 2,074.
3. **r4/r5** — "which service warns most?": the first subagent returned `search 7`, a second one `api 12`, the main session alone also said 12. The real count is **api 11** (`grep WARN server.log | awk '{print $3}' | sort | uniq -c`).
4. **r6** — `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` in print mode: TeamCreate + finder/checker spawned; a new helper said it had "no previous context"; right answer after 42.5 s; then `Cannot cleanup team with 1 active member(s): checker`, repeated shutdown requests, 7 final answers, 778,572 input tokens total. We stopped it with Ctrl+C.
   Note: the current docs say print mode (`-p`) doesn't spawn teammates; our older 2.1.92 did. Your version may differ.

## Settings from the docs
```json
{ "env": {
  "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "0",
  "CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH": "1"
} }
```
`0` keeps named subagents from launching as teammates; `1` turns off subagent nesting (default: up to 3 layers).
Docs: https://code.claude.com/docs/en/agent-teams · https://code.claude.com/docs/en/sub-agents · https://code.claude.com/docs/en/skills · https://code.claude.com/docs/en/costs

## Licenses
- This folder: MIT (see repo LICENSE). Claude Code: Anthropic's terms. Ollama: MIT. Gemma 4: Google's Gemma terms (cloud model via Ollama).

## Credit
The hands-on, show-every-step style of our tutorials is inspired by FreeAIVault (https://www.youtube.com/@FreeAIVaultTV).
