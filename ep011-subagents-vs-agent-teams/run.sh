#!/bin/zsh
# The runs from the video. Claude Code 2.1.92 + Ollama (free plan cloud model gemma4:31b-cloud), empty config dir.
# Docs for this setup: https://docs.ollama.com/integrations/claude-code
export ANTHROPIC_BASE_URL=http://localhost:11434
export ANTHROPIC_AUTH_TOKEN=ollama
export ANTHROPIC_API_KEY=""
export CLAUDE_CONFIG_DIR=$PWD/.cfg      # empty, throwaway config
M=gemma4:31b-cloud
T="Read Grep Glob Task Agent"

python3 make_log.py                       # 3,000-line server.log

# r1 · single session (move .claude/agents away first to reproduce exactly)
claude -p "In server.log, find the first ERROR and explain the likely cause in 2 sentences." --model $M --allowedTools "Read Grep Glob" --output-format stream-json --verbose | jq -r -f show.jq
# r2 · log-scout available, not named (Claude ran Grep itself)
claude -p "In server.log, find the first ERROR and explain the likely cause in 2 sentences." --model $M --allowedTools "$T" --output-format stream-json --verbose | jq -r -f show.jq
# r3 · subagent by name
claude -p "Use the log-scout subagent: in server.log, find the first ERROR and explain the likely cause in 2 sentences." --model $M --allowedTools "$T" --output-format stream-json --verbose | jq -r -f show.jq
# r4 · warnings, main session only (agents folder moved away)
claude -p "Read every WARN line in server.log and tell me which service warns most. Answer in 2 sentences." --model $M --allowedTools "$T" --output-format stream-json --verbose | jq -r -f show.jq
# r5 · warnings via log-scout
claude -p "Use the log-scout subagent: read every WARN line in server.log and tell me which service warns most. Answer in 2 sentences." --model $M --allowedTools "$T" --output-format stream-json --verbose | jq -r -f show.jq
# check the real count yourself
grep WARN server.log | awk '{print $3}' | sort | uniq -c | sort -rn
# r6 · agent team (experimental). Watch it: ours never finished shutting down and we stopped it with Ctrl+C.
CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1 claude -p "Create an agent team: spawn 2 teammates named finder and checker. finder finds the first ERROR in server.log, checker double-checks it. Report both in 2 sentences." --model $M --allowedTools "$T" --output-format stream-json --verbose | jq -r -f show.jq
