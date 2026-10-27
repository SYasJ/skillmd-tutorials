#!/bin/bash
# PreToolUse hook (Bash): block delete commands and any command that touches .env
cmd=$(jq -r '.tool_input.command // ""')
if echo "$cmd" | grep -Eq '(^|[;&| ])(rm|rmdir|unlink)( |$)'; then
  echo "Blocked by hook: deleting files is not allowed here. Stop and ask the user." >&2
  exit 2
fi
if echo "$cmd" | grep -q '\.env'; then
  echo "Blocked by hook: .env files hold secrets. Do not open them." >&2
  exit 2
fi
exit 0
