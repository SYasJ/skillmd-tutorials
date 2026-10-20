# ep003 · How to make money with AI: 7 steps, one real run

Hands-on tutorial from **[skill.md](https://www.youtube.com/channel/UCMQcMb_sp9gmMCYzhHRaS8g)**.

▶️ **Watch:** https://www.youtube.com/watch?v=7OrHAsuJGT0 (goes live Oct 25, 2026)

The video walks through seven steps, from picking one skill to a first paid test, and shows one real AI run along the way:
a free local model in [Ollama](https://ollama.com) drafts a French translation of a short, **made-up** bakery text in about
30 seconds on a laptop, and a human check then fixes its mistakes. The point of the run: the AI saves time, the human check is
what a client pays for.

No income promises. Most first attempts earn very little; the steps give you a first paid test and a way to repeat it.

| File | What it is |
|---|---|
| [`translate.py`](translate.py) | The script from the video: one prompt to a local Ollama model, prints the draft and the time it took |
| [`sample-en.txt`](sample-en.txt) | The source text (made up for the video, not a real business) |
| [`draft-fr.txt`](draft-fr.txt) | The model's French draft, **unedited** (cold start, 29.1 s, 101 tokens on our Mac) |
| [`draft-fr-run2.txt`](draft-fr-run2.txt) | A second run with the same prompt and temperature 0 (warm model, 14.9 s): different wording, different mistakes |
| [`human-fr.txt`](human-fr.txt) | The same text after a human check |

## Commands, in order

```bash
# needs Ollama installed and running
ollama pull qwen2.5-coder:3b        # see the license note below before any paid work
cat sample-en.txt
python3 translate.py sample-en.txt French
```

`translate.py` uses only the Python standard library (3.10+). Change `MODEL` at the top of the file to use another model.

## The prompt

```
Translate the following English business text into French. Keep numbers, units and names exactly. Output only the translation.
```

Temperature is 0, so answers barely change between runs, but they do change: our two runs gave different wording
(`draft-fr.txt` vs `draft-fr-run2.txt`). Check every draft.

## What the human check fixed (draft-fr.txt → human-fr.txt)
The three shown in the video:
1. "une notification de 48 heures" → "un préavis de 48 heures" (notice)
2. "ne sont jamais expirées" → "n'expirent jamais" (never expire)
3. "nous livrons à l'adresse du magasin dans les 5 km des jours ouvrables" → "nous livrons dans un rayon de 5 km autour de la
   boutique les jours ouvrables" (the delivery sentence had the wrong meaning)

Plus: "blé" (wheat) → "farine" (flour), "sourdough" left in English → "pain au levain", and smaller phrasing edits.
All four numbers (36 hours, 10 loaves, 48 hours, 5 km) came through correctly.

## Templates from the video
**Offer**
> I'll translate your menu and website text, up to 1,000 words, English → French. Delivered in 3 working days.
> 1 round of changes included. One fixed price: ______

**First message**
> Hi, I saw your new menu online. I translated the first 3 lines into French for free, attached.
> If it's useful, I can do the full menu by Friday, for a fixed price.

## Licenses — read before you charge anyone
- `qwen2.5-coder:3b` — **Qwen RESEARCH LICENSE AGREEMENT: non-commercial (research or evaluation only)**; commercial users must
  request a license from Alibaba Cloud. Fine for trying this workflow, **not** for paid client work as-is. Pick a model whose
  license allows commercial use and read that license first (for example, ep002 used `qwen3:4b`, listed as Apache 2.0 —
  check the current license yourself).
- Ollama — MIT
- The code in this folder — MIT (see the repo LICENSE)

## Source for the numbers in the video
Upwork 2026 In-Demand Skills report (February 2026), as reported by Self Employed:
https://www.selfemployed.com/news/upwork-ai-freelance-skills-demand-2026/ — AI-related skills +109% year over year (2025, U.S.
marketplace), AI video generation and editing +329%, AI integration +178%.

## Credits
The hands-on, show-every-step segments of this tutorial are inspired by **[FreeAIVault](https://www.youtube.com/@FreeAIVaultTV)** — go check out their channel.
