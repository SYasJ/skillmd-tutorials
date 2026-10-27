#!/bin/bash
# PreToolUse hook (Bash): block rm -rf before it runs
cmd=$(jq -r '.tool_input.command // ""')
if echo "$cmd" | grep -Eq 'rm +-[a-zA-Z]*(rf|fr)'; then
  echo "Blocked by hook: rm -rf is not allowed in this project." >&2
  exit 2
fi
exit 0
