# ep002 · MCP server tutorial (Python SDK v2): give a free local AI live data

Hands-on tutorial from **[skill.md](https://www.youtube.com/channel/UCMQcMb_sp9gmMCYzhHRaS8g)**.

▶️ **Watch:** https://www.youtube.com/watch?v=KmGqDziaxSc (goes live Oct 23, 2026)

We build a tiny MCP server in Python (official MCP Python SDK **v2**), test it with a 15-line client, then connect it to a free
local model in [Ollama](https://ollama.com) with a small agent script. Asked "How many GitHub stars does ollama/ollama have
right now?", the model **without** the tool answered "approximately 12,158" (a guess); **with** the tool it answered
183,721 — the live number from the GitHub API on 18 Oct 2026.

Everything here is exactly what we ran on our Mac (CPU only, no GPU). Model output in the video is unedited.

| File | What it is |
|---|---|
| [`server.py`](server.py) | The MCP server: one tool, `repo_stats(repo)`, that reads public stats from the GitHub API |
| [`test_server.py`](test_server.py) | A tiny MCP client that starts the server, lists its tools and calls one (the fixed version, see bug #2) |
| [`agent.py`](agent.py) | The bridge: MCP tools → Ollama tool calling → final answer. `--no-tools` runs the same question without the tool |
| [`old_server.py`](old_server.py) | The v1 import (`from mcp.server.fastmcp import FastMCP`) that crashes on mcp 2.x — kept to show bug #1 |
| [`pyproject.toml`](pyproject.toml) | The two dependencies |
| [`mcp.json.example`](mcp.json.example) | What `claude mcp add --scope project …` wrote (rename to `.mcp.json` to use it in Claude Code) |

## Commands, in order

```bash
# 1 · set up (needs Ollama + uv installed)
mkdir mcp-server-ollama && cd mcp-server-ollama
uv init --bare --python 3.12 && uv add "mcp[cli]" ollama
ollama pull qwen3:4b            # 2.5 GB, took ~76 s for us

# 2 · test the server on its own
uv run test_server.py

# 3 · ask the local model, with and without the tool
uv run agent.py "How many GitHub stars does ollama/ollama have right now?"
uv run agent.py "How many GitHub stars does ollama/ollama have right now?" --no-tools

# bonus · the same server in Claude Code
claude mcp add --scope project repo-stats -- uv run server.py
claude mcp get repo-stats
```

On our Mac (CPU only) the tool run took about 2 minutes (tool call after ~61 s), the no-tool run about 89 s.

## The three things that broke (and the fixes)
1. **v1 tutorial code crashes on v2.** `from mcp.server.fastmcp import FastMCP` → `ModuleNotFoundError`. In v2, FastMCP is now
   `MCPServer`: `from mcp.server import MCPServer` ([What's new in v2](https://py.sdk.modelcontextprotocol.io/whats-new/)).
2. **`result.structured_content` was `None`.** Our tool returns a plain `dict`, and in our run it had no output schema, so the
   structured content stayed empty. The JSON is in `result.content[0].text`.
3. **`qwen2.5-coder:3b` printed the tool call as text** (a JSON code block) instead of making a tool call, even though
   `ollama show` lists `tools` as a capability. `qwen3:4b` made a real tool call. (Qwen3 also thinks out loud after the tool
   result even with `think=False`, so `agent.py` prints only the text after `</think>`.)

Change the model with `MODEL=… uv run agent.py "…"`.

## Licenses
- MCP Python SDK (`mcp` 2.3.0) — MIT · [github.com/modelcontextprotocol/python-sdk](https://github.com/modelcontextprotocol/python-sdk)
- Ollama 0.30.11 — MIT · `ollama` Python library 0.6.3 — MIT
- `qwen3:4b` — Apache 2.0 · `qwen2.5-coder:3b` (bug #3) — Qwen Research License (personal/research use)
- Claude Code — Anthropic's terms
- The code in this folder — MIT (see the repo LICENSE)

The tool calls the public GitHub API without a token, so GitHub's unauthenticated rate limit applies.

## Credits
The hands-on, show-every-step segments of this tutorial are inspired by **[FreeAIVault](https://www.youtube.com/@FreeAIVaultTV)** — go check out their channel.
