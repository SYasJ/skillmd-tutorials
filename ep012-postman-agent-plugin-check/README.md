# ep012 — Postman in your Claude Code / Codex config? A read-only check

Companion to the skill.md Daily video **"Postman Claude Code Plugin Installed Itself. Did You Say Yes?"** (Nov 5, 2026)
Watch: https://www.youtube.com/watch?v=MBo8WvuyA8k

## What happened (Nov 3, 2026)
GitHub issue [postmanlabs/postman-app-support#14370](https://github.com/postmanlabs/postman-app-support/issues/14370) reports that opening
Postman Desktop 12.33.4 logged `auto-existing-upgrade` → `claude-code:installed`, `codex:installed`, and added a Codex plugin + startup hook,
a remote MCP server, a Claude Code plugin and the Postman CLI. Postman's docs for its plugin installer say: *"The installer approves the hook for you."*
A reply in the thread says the plugins are bundled to make setup easier and that the opt-in will be made clearer.

## 1 · Read-only check (changes nothing)
```bash
curl -fsSLO https://raw.githubusercontent.com/SYasJ/skillmd-tutorials/main/ep012-postman-agent-plugin-check/check-postman-agent-plugins.sh
less check-postman-agent-plugins.sh      # read it first — it only runs grep / ls
bash check-postman-agent-plugins.sh
```
Or by hand:
```bash
grep -n postman ~/.claude/settings.json
grep -n postman ~/.claude/plugins/installed_plugins.json
grep -n -A3 postman ~/.codex/config.toml
grep -n postman ~/.copilot/settings.json
ls ~/.local/bin | grep -i postman
```

## 2 · Postman's own installer (from Postman's docs)
Docs: https://learning.postman.com/docs/postman-plugin/install/detected-agents
```bash
npx @postman/postman-plugin status              # which agents have the plugin
npx @postman/postman-plugin remove --dry-run    # preview what remove would do
npx @postman/postman-plugin remove              # uninstall from each detected agent (asks to confirm)
```
`--agent <id>` limits it to one agent. We did **not** run these on our machine for the video; they are quoted from Postman's documentation.

## Notes
- The check script was tested on a demo home folder made from the config lines quoted in issue #14370 (not on anyone's real machine).
- Tools: Postman (Postman, Inc.), Claude Code (Anthropic), Codex (OpenAI), GitHub Copilot (GitHub). This folder is MIT like the repo.

---
Channel: **skill.md** — https://www.youtube.com/channel/UCMQcMb_sp9gmMCYzhHRaS8g · The hands-on, show-every-step style of these tutorials is inspired by FreeAIVault (https://www.youtube.com/@FreeAIVaultTV).
