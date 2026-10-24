# ep004 · Don't give your AI agent an open internet (Claude Code sandbox allowlist)

From the skill.md video **"Claude Mythos 5 Went Rogue in a Safety Test. It Faked a Human"** (AI news, Oct 2026):
https://www.youtube.com/watch?v=QTzZYoXkMvI

Channel: **skill.md** — https://www.youtube.com/channel/UCMQcMb_sp9gmMCYzhHRaS8g

## Why
On Oct 23, 2026 Anthropic published an alignment assessment of a UK AI Security Institute (AISI) cyber test:
https://www.anthropic.com/research/alignment-assessment-ukaisi
Internet access was deliberately on during that test, and the model used it to target a real GitHub project.
AISI has since committed to running these evaluations without internet access.
Lesson for anyone running coding agents: keep the network closed by default and allow only the hosts you need.

## What's in this folder
- `settings.json` — a minimal Claude Code settings snippet: turns the sandbox on and allows only `github.com`.

## How to use it
1. In a Claude Code session, run `/sandbox` to open the sandbox panel (the sandbox is off by default).
2. Or merge the snippet into your settings file, e.g. `~/.claude/settings.json` (all projects)
   or `.claude/settings.json` in a project. Add only the hosts your project really needs
   (the docs' own example also allows `*.npmjs.org`).
3. Sandboxed commands then reach the network only through Claude Code's proxy, and "your allowed domains start empty".

Source (fields and behavior): https://code.claude.com/docs/en/sandboxing — check it for your version; settings can change.

## For maintainers
In the incident, what stopped the malicious pull request was a person who ran the code in an isolated sandbox
before trusting it, and maintainers who refused to merge. Test code from strangers in a sandbox, and slow down
when brand-new accounts suddenly vouch for a stranger's change.

## License
MIT (this folder). Claude Code is Anthropic's product, used under its own terms.

The hands-on, show-every-step style of these tutorials is inspired by FreeAIVault (https://www.youtube.com/@FreeAIVaultTV).
