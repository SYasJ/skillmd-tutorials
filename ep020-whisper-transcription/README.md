# ep020 · Whisper AI transcription: free, offline, with real error counts

Hands-on tutorial from **[skill.md](https://www.youtube.com/channel/UCMQcMb_sp9gmMCYzhHRaS8g)**.

▶️ **Watch:** [Whisper AI Transcription: Free & Offline, But It Wrote "Cloud Code"](https://www.youtube.com/watch?v=ocl7QhMDSxg) (goes live Nov 10, 2026)

We transcribed an 82-second clip (230 words, music under the voice, taken from our own video ep006) with OpenAI's open-source
[Whisper](https://github.com/openai/whisper) on a Mac, CPU only, and scored every run against the script that was really read.
Everything in `runs/` is exactly what Whisper wrote, unedited.

| File | What it is |
|---|---|
| [`score.py`](score.py) | Word error rate (word-level edit distance ÷ 230) + a check for the names Claude Code, Ollama, JSON, Gemma |
| [`transcribe.py`](transcribe.py) | The 8-line Python version (small model + initial prompt) |
| [`reference.txt`](reference.txt) | What was really said in the clip |
| [`runs/`](runs/) | Whisper's output for every run (+ the SRT and VTT from the best run) |

The audio clip itself is not included: use any recording of your own and write its exact text into `reference.txt`.

## Commands, in order

```bash
brew install ffmpeg                # macOS · Ubuntu: sudo apt install ffmpeg
pip install -U openai-whisper      # we used openai-whisper 20250625 (it was already installed)

# 1) tiny, no prompt
whisper clip.mp3 --model tiny --language en --fp16 False
python3 score.py reference.txt clip.txt

# 2) bigger models
whisper clip.mp3 --model base  --language en --fp16 False
whisper clip.mp3 --model small --language en --fp16 False

# 3) teach it your words
whisper clip.mp3 --model small --language en --fp16 False --initial_prompt "Claude Code, Ollama, Gemma 4"

# 4) same, 4x faster on our machine (greedy decoding instead of 5 beams)
whisper clip.mp3 --model small --language en --fp16 False --initial_prompt "Claude Code, Ollama, Gemma 4" --beam_size 1 --best_of 1

# 5) Python
python transcribe.py
```

Whisper writes every format by default (`--output_format all`): `.txt`, `.srt`, `.vtt`, `.tsv`, `.json`.
If you leave out `--model`, the CLI uses `turbo` (a much bigger download).

## What happened (one clip, 230 words, our machine)

| Run | Time | Word error rate | "Claude Code" | "Ollama" |
|---|---|---|---|---|
| tiny | 45.2 s | 10.0% (23) | 0 of 4 ("Cloud Code") | 0 of 5 ("Olamma") |
| base | 82.3 s | 3.9% (9) | 4 of 4 | 0 of 5 |
| small | 253.3 s | 3.0% (7) | 4 of 4 | 0 of 5 ("Olama") |
| base + initial prompt | 70.9 s | 27.4% (63) | 3 of 4 | 5 of 5 — but 0:08 → 0:30 skipped |
| base + prompt + `--condition_on_previous_text False` | 67.8 s | 29.6% (68) | 2 of 4 | 0 of 5 |
| small + initial prompt | 258.3 s (257.6 s on a re-run) | 1.3% (3) | 4 of 4 | 5 of 5 |
| small + prompt + `--beam_size 1 --best_of 1` | 64.7 s | 1.3% (3) | 4 of 4 | 5 of 5 |
| Python `transcribe.py` (greedy by default) | 70.1 s | 1.3% (3) | 4 of 4 | 5 of 5 |

Also seen: tiny wrote "Stay out of the test." twice (said once) and turned "Step one, point Claude Code" into "One point-cloth code".
The best runs wrote "It's a **Claude** model" where the clip says "It's a **cloud** model" — the prompt pushed one word too far.
Times include loading the model; they will be different on your machine.

## Tips
1. Start with `small` and set `--language`.
2. Put your names in `--initial_prompt`, keep it short (the code: "custom vocabularies or proper nouns", used for the first window).
3. `--beam_size 1 --best_of 1` if speed matters more than the last bit of accuracy (CLI defaults are 5 and 5).
4. Proofread names and numbers. Whisper never says it's unsure.

## Licenses
- Whisper code and model weights — MIT ([openai/whisper](https://github.com/openai/whisper))
- FFmpeg — LGPL/GPL (installed separately)
- The code in this folder — MIT (see the repo LICENSE)

---
The hands-on, show-every-step style of these tutorials is inspired by FreeAIVault (https://www.youtube.com/@FreeAIVaultTV).
