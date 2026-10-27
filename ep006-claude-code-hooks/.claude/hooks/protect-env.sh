#!/bin/bash
# PreToolUse hook (Read|Edit|Write): keep Claude out of .env files
file=$(jq -r '.tool_input.file_path // ""')
case "$file" in
  *.env|*.env.*)
    echo "Blocked by hook: .env files hold secrets. Do not open them." >&2
    exit 2;;
esac
exit 0
