# ep024 · Chrome DevTools MCP — real test + safe defaults

Video: [Chrome DevTools MCP: It Found Our Bug. Then We Changed 4 Defaults](https://www.youtube.com/watch?v=NzN9ediRlvE)

We ran **chrome-devtools-mcp v1.13.0** (the `chrome-devtools` CLI that ships in the same npm package) against a tiny demo page we broke on purpose, on a Mac, inside `/tmp`. It found both bugs. Then we looked at the defaults.

## What's here
| File | What |
|---|---|
| `demo-site/index-broken.html` | The demo page with 2 planted bugs (missing `/logo.png`, `cart` not defined) |
| `demo-site/index-fixed.html` | The fixed page (`lang="en"`, `cart` defined; add any `logo.png`) |
| `run-demo.sh` | The exact command sequence from the video |
| `safe-mcp-config.json` | MCP client config with the 4 flags we turn on from day one |

## What we saw (real output, Nov 15 2026)
- `list_console_messages` → `Uncaught ReferenceError: cart is not defined` + two 404s
- `list_network_requests` → `logo.png [404]`, `favicon.ico [404]`
- Screenshot inside `--workspace` → saved; outside → `Access denied … not within any of the configured workspace roots`
- `lighthouse_audit --mode snapshot` → Accessibility 84, SEO 80, 3 failed audits; after the fix Accessibility 96 (the favicon 404 stays — we never made one)
- After a reload, clicking the old uid → `Element with uid 1_3 no longer exists on the page`. The docs: "Always use the latest snapshot."

## The 4 defaults we change
| Default | Flag |
|---|---|
| Usage statistics are collected by Google (enabled by default) | `--no-usage-statistics` |
| Performance tools may send trace URLs to the Google CrUX API | `--no-performance-crux` |
| Network headers are not redacted (`redactNetworkHeaders: false`) | `--redact-network-headers` |
| CLI: unrestricted filesystem access unless you set a workspace | `--workspace=/your/folder` |
Also: `javascriptEvaluation` is on by default (`--no-javascript-evaluation` turns the evaluation tools off). Use a test browser profile, not the one you're logged in with.

## Licenses
- chrome-devtools-mcp: Apache-2.0 (https://github.com/ChromeDevTools/chrome-devtools-mcp)
- Files in this folder: MIT (repo license)

---
The hands-on, show-every-step style of these tutorials is inspired by FreeAIVault (https://www.youtube.com/@FreeAIVaultTV).
