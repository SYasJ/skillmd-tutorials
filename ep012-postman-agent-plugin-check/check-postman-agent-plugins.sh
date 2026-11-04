#!/usr/bin/env bash
# skill.md ep012 — READ-ONLY check: did an app add a Postman plugin/hook to your coding agents?
# It only reads files. It changes nothing. macOS / Linux, bash.
# Files checked come from Postman issue #14370 and the comments under it:
#   https://github.com/postmanlabs/postman-app-support/issues/14370
set -u
found=0
check () { # $1 = file, $2 = what it is
  if [ -f "$1" ]; then
    if grep -n -i "postman" "$1" >/dev/null 2>&1; then
      echo "FOUND  $2  ($1)"; grep -n -i "postman" "$1" | sed 's/^/        /'; found=1
    else echo "clean  $2"; fi
  else echo "-      $2 (no file)"; fi
}
check "$HOME/.claude/settings.json"                  "Claude Code settings (enabledPlugins)"
check "$HOME/.claude/plugins/installed_plugins.json" "Claude Code installed plugins"
check "$HOME/.codex/config.toml"                     "Codex config (marketplaces, plugins, hooks.state)"
check "$HOME/.copilot/settings.json"                 "GitHub Copilot CLI settings"
if ls "$HOME/.local/bin" 2>/dev/null | grep -i -q postman; then
  echo "FOUND  Postman CLI in ~/.local/bin"; ls -l "$HOME/.local/bin" | grep -i postman | sed 's/^/        /'; found=1
else echo "clean  ~/.local/bin"; fi
echo
if [ "$found" = 1 ]; then
  echo "Something mentions Postman. If you did not choose this, see README.md (status / remove --dry-run)."
else
  echo "No Postman entries found in the files above."
fi
