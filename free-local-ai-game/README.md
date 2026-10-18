# I asked a free local AI to build a game — files from the video

Hands-on tutorial from **[skill.md](https://www.youtube.com/channel/UCMQcMb_sp9gmMCYzhHRaS8g)**.

▶️ **Watch:** https://www.youtube.com/watch?v=Qco2QHSNxMY ("Ollama Tutorial: A Free Local AI Built This Game in 3 Prompts" — goes live Oct 22, 2026)

Everything here is exactly what the AI produced on our Mac — we did not hand-edit the game files.

| File | What it is |
|---|---|
| [`prompts.md`](prompts.md) | Every command and prompt from the video, in order |
| [`snake-try2-buggy.html`](snake-try2-buggy.html) | Try 2 output — runs, but has the two bugs shown in the video |
| [`snake-fixed.html`](snake-fixed.html) | After "make it fix its own bugs" — the working game |

**Play it:** download `snake-fixed.html` and open it in your browser. Arrow keys move, space restarts.

## What you need
- [Ollama](https://ollama.com) (free, open source, MIT license) — macOS, Linux or Windows
- `qwen2.5-coder:3b` — about 1.9 GB, from Alibaba Cloud's Qwen team. It uses the **Qwen Research License**, so it's free for personal and research projects, not commercial use.
- No account, no API key, works offline after the download. Cost: $0.

## Credits
The hands-on, show-every-step style of this tutorial was inspired by **[FreeAIVault](https://www.youtube.com/@FreeAIVaultTV)** — go check out their channel.
