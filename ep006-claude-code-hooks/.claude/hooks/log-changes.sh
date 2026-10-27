#!/bin/bash
# PostToolUse hook (Edit|Write): write every file change to a log
input=$(cat)
tool=$(echo "$input" | jq -r '.tool_name')
file=$(echo "$input" | jq -r '.tool_input.file_path // ""')
dir=$(echo "$input" | jq -r '.cwd')
echo "$(date '+%H:%M:%S')  $tool  $(basename "$file")" >> "$dir/changes.log"
exit 0
