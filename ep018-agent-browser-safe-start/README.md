# ep018 · agent-browser safe start (4 switches)

Companion to the skill.md video **Vercel Agent Browser: 47K Stars, Every Safety Switch Off by Default** → https://www.youtube.com/watch?v=vXSW22HhvbY

[vercel-labs/agent-browser](https://github.com/vercel-labs/agent-browser) (Apache-2.0) gives an AI agent a real browser from the shell.
Its own security page says: *"All security features are opt-in"* and *"By default, agent-browser imposes no restrictions on navigation, actions, or output."*
These files turn on the four switches from the video. They are copied from the official docs at
https://agent-browser.dev/security (fetched 2026-11-08); only the domains are placeholders.

> **Honest note:** we read the docs, the README and the npm install script, but **we did not run agent-browser** for this video.
> Test these files yourself before relying on them, and replace `your-app.com` with the sites your agent actually needs.

## Files

| File | What it does |
|---|---|
| `agent-browser.json` | Project config: content boundaries on, output capped at 50,000 characters, domain allowlist, action policy file |
| `policy.json` | Permissive policy: allow everything except `eval`, `download`, `upload` |
| `policy-strict.json` | Restrictive policy: deny by default, allow only navigate / snapshot / click / scroll / wait / get |

## The four switches (same thing as flags)

```bash
npm install -g agent-browser
agent-browser install            # downloads Chrome for Testing (first time only)

agent-browser \
  --allowed-domains "your-app.com,*.your-app.com" \
  --action-policy ./policy.json \
  --content-boundaries \
  --max-output 50000 \
  open https://your-app.com

agent-browser snapshot -i        # interactive elements, each with a ref like @e1
```

Environment variables also exist: `AGENT_BROWSER_ALLOWED_DOMAINS`, `AGENT_BROWSER_ACTION_POLICY`,
`AGENT_BROWSER_CONTENT_BOUNDARIES`, `AGENT_BROWSER_MAX_OUTPUT`.

## Fine print (from the docs)

- The domain allowlist **is not an operating-system firewall**. Pair it with network egress controls if you need a real boundary.
- Content boundaries are **defense-in-depth**: they only help if your model and orchestrator respect the markers.
- WebSocket / EventSource blocking is best-effort; denying `eval` makes it stronger.
- Keep agent-browser updated: v0.41.0 (Oct 29, 2026) rejected MCP tool arguments that could override the allowlist; v0.40.0 (Oct 27) stopped exposing saved tokens to page scripts.

## Licenses

- agent-browser: Apache-2.0 (Vercel Labs). The JSON snippets are adapted from its docs.
- This folder: MIT, like the rest of this repo.

---
The hands-on, show-every-step style of this series is inspired by FreeAIVault (https://www.youtube.com/@FreeAIVaultTV).
