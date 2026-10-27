#!/bin/bash
# PreToolUse hook (Bash): block every delete command before it runs
cmd=$(jq -r '.tool_input.command // ""')
if echo "$cmd" | grep -Eq '(^|[;&| ])(rm|rmdir|unlink)( |$)'; then
  echo "Blocked by hook: deleting files is not allowed here. Stop and ask the user." >&2
  exit 2
fi
exit 0
