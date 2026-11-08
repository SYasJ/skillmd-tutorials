#!/usr/bin/env bash
# check-claude-settings.sh — skill.md ep017
# Finds Claude Code settings files (.claude/settings.local.json and .claude/settings.json)
# under a folder, says whether git tracks them (or ever did), and counts lines that look like secrets.
# Read-only: it changes nothing. Usage:  bash check-claude-settings.sh [folder]   (default: current folder)
set -u
ROOT="${1:-.}"
PATTERN='PGPASSWORD=|sshpass -p|mysql[^"]* -p[^ "]+|password=|passwd|token=|api[_-]?key|secret|AKIA[0-9A-Z]{16}|ghp_[A-Za-z0-9]{20,}|npm_[A-Za-z0-9]{20,}|://[^/ :"]+:[^@ "]+@'
found=0
while IFS= read -r f; do
  found=1
  proj=$(dirname "$(dirname "$f")")
  rel=".claude/$(basename "$f")"
  tracked="no git"; history="-"
  if git -C "$proj" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    if git -C "$proj" ls-files --error-unmatch "$rel" >/dev/null 2>&1; then tracked="YES (committed)"; else tracked="no"; fi
    n=$(git -C "$proj" log --all --oneline -- "$rel" 2>/dev/null | wc -l | tr -d ' ')
    history="$n commit(s)"
  fi
  hits=$(grep -Eic "$PATTERN" "$f" 2>/dev/null || true)
  echo "$f"
  echo "   tracked by git: $tracked | in git history: $history | lines that look like secrets: $hits"
done < <(find "$ROOT" -type f \( -path '*/.claude/settings.local.json' -o -path '*/.claude/settings.json' \) -not -path '*/node_modules/*' 2>/dev/null)
[ "$found" = 1 ] || echo "No Claude Code settings files found under $ROOT"
echo
echo "If a file is tracked or has secrets: 1) rotate those secrets first  2) git rm --cached .claude/settings.local.json"
echo "3) echo '.claude/settings.local.json' >> .gitignore  4) delete the secret rules from the file  5) use \$ENV_VARS in commands"
