# ep005 · Claude Code skills tutorial: your first SKILL.md, free with Ollama

Hands-on tutorial from **[skill.md](https://www.youtube.com/channel/UCMQcMb_sp9gmMCYzhHRaS8g)**.

**Watch:** https://www.youtube.com/watch?v=aiJI2tvxEH0

One small folder — `.agents/skills/launch-page/` — turned a generic AI landing page into a page in our house style, with the same prompt and the same model. This folder has the exact skill, every command we ran, the real terminal output and the pages the AI wrote (unedited).

## What's here

| Path | What it is |
|---|---|
| `.agents/skills/launch-page/SKILL.md` | The skill: `name` + `description` (the trigger) + plain steps + a "Don't" list |
| `.agents/skills/launch-page/references/brand.md` | Exact colours/fonts. Loaded only when the skill runs |
| `.claude/skills/launch-page` | Symlink → `../../.agents/skills/launch-page` (Claude Code reads `.claude/skills`, Codex and Gemini CLI read `.agents/skills`) |
| `ai-output/no-skill.html` | Baseline: skills turned off |
| `ai-output/agents-dir-ignored.html` | Skill only in `.agents/skills` — Claude Code didn't load it |
| `ai-output/with-skill.html` | After the symlink: Skill → Read brand.md → Write (9.4 s) |
| `ai-output/plantpal.html` | A different app, same skill (10.1 s) |
| `show.jq` | Turns Claude Code's `stream-json` into one readable line per tool call |
| `run-log.md` | Every command and its real output, in order |

## Steps (exactly what the video shows)

```sh
# 01 · make the folder (in your project)
mkdir -p .agents/skills/launch-page/references
# 02 · write .agents/skills/launch-page/SKILL.md   (copy ours)
# 03 · write .agents/skills/launch-page/references/brand.md

# 04 · point Claude Code at Ollama (lines from https://docs.ollama.com/integrations/claude-code)
export ANTHROPIC_AUTH_TOKEN=ollama
export ANTHROPIC_API_KEY=""
export ANTHROPIC_BASE_URL=http://localhost:11434

# 05 · baseline, skills off
claude --model gemma4:31b-cloud -p "Make a launch page for TideTimer, an app that tells surfers the best tide times. Save it as index.html." \
  --disable-slash-commands --permission-mode acceptEdits --output-format stream-json --verbose | jq -r -f show.jq

# fix for "Claude Code ignored .agents/skills": one copy, both paths
mkdir -p .claude/skills
ln -s ../../.agents/skills/launch-page .claude/skills/launch-page

# 06 · run it again (same prompt, skills on)
claude --model gemma4:31b-cloud -p "Make a launch page for TideTimer, an app that tells surfers the best tide times. Save it as index.html." \
  --permission-mode acceptEdits --output-format stream-json --verbose | jq -r -f show.jq
```

Interactive use: start `claude --model gemma4:31b-cloud` and type `/launch-page` to call the skill directly.

## The 3 things that went wrong

1. **A plugin I already had installed jumped in** with its own skill (brainstorming) and no page was written — even with `--disable-slash-commands`. Fix for a clean test: `export CLAUDE_CONFIG_DIR=/tmp/clean-claude`.
2. **Claude Code 2.1.92 didn't load a skill that was only in `.agents/skills`.** Its docs list `.claude/skills/<name>/SKILL.md` for project skills. Fix: the symlink above. (Codex and Gemini CLI document `.agents/skills`; we did not run them in this video.)
3. **Fully local `qwen2.5-coder:3b` printed the tool call as plain text** — no file after 99.6 s. `ollama ps` showed a 4,096-token context; Ollama's docs recommend 64k+ for Claude Code. On this laptop the free cloud model worked.

## Versions, models, licenses

- Claude Code 2.1.92 (Anthropic) — commercial terms: https://www.anthropic.com/legal/commercial-terms
- Ollama 0.30.11 (MIT). `gemma4:31b-cloud` runs on Ollama's cloud (your prompt is sent to Ollama's servers); on 2026-10-25 Ollama's own error message said it is in the Free plan.
- Gemma 4 31B: Apache 2.0 (https://huggingface.co/google/gemma-4-31B-it)
- qwen2.5-coder:3b: Qwen Research License (non-commercial)
- Agent Skills spec: https://agentskills.io/specification
- The skill and scripts in this folder: MIT (repo license)

AI output is shown unedited. The two no-skill pages link a stock photo from images.unsplash.com; it did not load in our headless screenshots, so the video shows them without it. Every timing is the real wall-clock time from our run.

---
The hands-on, show-every-step style of these tutorials is inspired by **FreeAIVault** (https://www.youtube.com/@FreeAIVaultTV).
