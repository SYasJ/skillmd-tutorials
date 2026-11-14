# ep023 · llama.cpp v1.0 — a private, ChatGPT-style server on a Mac

Watch: [llama.cpp Tutorial: I Asked for a Poem, It Asked to Run JavaScript](https://www.youtube.com/watch?v=UbwZSZJCdCY)

Everything we ran on camera, in order. Real runs on an Intel Mac, CPU only, Saturday 2026-11-14.
llama.cpp release **b12359** = tag **v1.0.0** (published 2026-11-13). Model: **ggml-org/Qwen3-1.7B-GGUF : Q4_K_M** (1.28 GB).

## Commands (`commands.sh`)

```bash
mkdir -p /tmp/llamacpp-ep && cd /tmp/llamacpp-ep

# 01 · download the release (Intel Mac). Apple silicon: ...-bin-macos-arm64.tar.gz
curl -L -O https://github.com/ggml-org/llama.cpp/releases/download/b12359/llama-b12359-bin-macos-x64.tar.gz
# verify against the digest GitHub lists for the asset
shasum -a 256 llama-b12359-bin-macos-x64.tar.gz
# expected: 25320d529077ef5a3d16e7b5da26438f221d88c8c0930a32b0c79457f5eede56
tar xzf llama-b12359-bin-macos-x64.tar.gz
./llama-b12359/llama-server --version      # version: 1.0.0-dev (build 12359, ...)

# 03 · start the server; LLAMA_CACHE keeps the model in ./models (not a hidden cache)
LLAMA_CACHE=./models ./llama-b12359/llama-server -hf ggml-org/Qwen3-1.7B-GGUF:Q4_K_M
# -> "listening on http://127.0.0.1:9931"   (v1.0 default port is 9931, not 8080; use --port 8080 if you need the old one)

# in a second terminal
curl http://127.0.0.1:9931/health

# 05 · the OpenAI-style API (thinking on: 22.3 s, 295 tokens in our run)
time curl -s http://127.0.0.1:9931/v1/chat/completions -H 'Content-Type: application/json' \
  -d '{"messages":[{"role":"user","content":"Name 3 coffee shops run by robots. One line each."}]}'

# thinking off: 5.7 s, 69 tokens in our run
time curl -s http://127.0.0.1:9931/v1/chat/completions -H 'Content-Type: application/json' \
  -d '{"messages":[{"role":"user","content":"Name 3 coffee shops run by robots. One line each."}],"chat_template_kwargs":{"enable_thinking":false}}' \
  | jq -r '.choices[0].message.content, .usage.completion_tokens'

# 06 · Python with the OpenAI SDK (in a venv under /tmp)
python3 -m venv venv && ./venv/bin/pip install -q openai
./venv/bin/python chat.py
# 07 · forced JSON via a schema
./venv/bin/python extract.py     # our run: date came back as 2023-11-20 (wrong year)
./venv/bin/python extract2.py    # + system message with today's date -> 2026-11-20

# done? stop the server (Ctrl+C) and delete the folder
rm -rf /tmp/llamacpp-ep
```

## Files

| File | What it does |
|---|---|
| `commands.sh` | the commands above |
| `chat.py` | one chat request with the OpenAI Python SDK pointed at `http://127.0.0.1:9931/v1`, thinking off |
| `extract.py` | structured output: `response_format` with a JSON schema (name, date, time) |
| `extract2.py` | same + a system message with today's date (fixes the wrong year) |

## What went wrong (all real, shown unedited in the video)

1. **Port 8080 → connection refused.** In v1.0 `llama-server` defaults to port **9931** (see `tools/server/README.md`, `--port`).
2. **The built-in web UI's browser tools.** Asked for a 4-line poem, Qwen3-1.7B asked to use `get_info`, then `run_javascript`, from "Browser Tools". The UI asks permission every time; we clicked Deny.
3. **JSON shape ≠ correct facts.** The schema forced valid JSON, but the model wrote the year 2023. Giving it today's date fixed it.

Also seen: the startup log warns `no API key is set and CORS allows all origins`. The server listens on 127.0.0.1 by default; add `--api-key` before you ever bind it to your network.

## Licenses

- llama.cpp / ggml: MIT — https://github.com/ggml-org/llama.cpp
- Qwen3-1.7B (GGUF by ggml-org): Apache-2.0 — https://huggingface.co/ggml-org/Qwen3-1.7B-GGUF
- openai-python: Apache-2.0 — https://github.com/openai/openai-python
- Our scripts in this folder: MIT (this repo)

## Credits

Made for the skill.md YouTube channel (https://www.youtube.com/channel/UCMQcMb_sp9gmMCYzhHRaS8g).
The hands-on, show-every-step style of these tutorials is inspired by FreeAIVault (https://www.youtube.com/@FreeAIVaultTV).
