# ep016 · AI automation for a small business: an inbox assistant that sorts, drafts and never sends

Hands-on tutorial from **[skill.md](https://www.youtube.com/channel/UCMQcMb_sp9gmMCYzhHRaS8g)** · part 2 of *making money with AI* (part 1: [ep003](../ep003-make-money-with-ai/)).

▶️ **Watch:** https://www.youtube.com/watch?v=vYwwHiwiYUs (goes live Nov 8, 2026)

A small Python script reads a folder of customer emails, sorts each one into a category, rates urgency 1–3 and drafts a reply
with a free local model in [Ollama](https://ollama.com). **Nothing is ever sent**: drafts go to `drafts/` and a summary to
`triage.csv`, and the owner approves every reply. The bakery (Harbor Bakery) and all six emails are **made up**.

Everything in `runs/` is exactly what we ran on our Mac (Ollama 0.30.11, CPU), with model output unedited.

| File | What it is |
|---|---|
| [`triage.py`](triage.py) | Final version (v3): qwen3:4b + the owner's facts + definitions + the spam rule in code |
| [`triage_v2.py`](triage_v2.py) | v2: same as final but qwen3:1.7b |
| [`triage_v1.py`](triage_v1.py) | v1: qwen3:1.7b, no facts, no definitions, no spam rule |
| [`facts.txt`](facts.txt) | The owner's facts (made-up bakery) |
| [`inbox/`](inbox/) | The six made-up emails |
| [`runs/v1`](runs/v1), [`runs/v2`](runs/v2), [`runs/v3`](runs/v3) | `triage.csv` + `drafts/` from each recorded run |

## Commands, in order

```bash
# needs Ollama installed and running · standard-library Python 3.10+, no pip installs
ollama pull qwen3:4b                     # 2.5 GB (qwen3:1.7b is 1.4 GB)
python3 triage.py inbox/ facts.txt       # writes drafts/ and triage.csv, sends nothing
```

## What happened (expected: 01 order · 02 complaint · 03 catering · 04 question · 05 wholesale · 06 spam)

| | v1 (1.7B, no fixes) | v2 (1.7B + fixes) | v3 (4B + fixes) |
|---|---|---|---|
| Categories right | 3/6 | 3/6 | 5/6 |
| Time for 6 emails | 51.9 s | 57.1 s | 125.7 s |
| Wrong-order complaint | "order", urgency 2 | complaint, urgency 3 | complaint, urgency 3 |
| Café weekly supply (a sales lead) | **spam** | order | wholesale |
| Sunday-hours question | question, draft **invented** "We're open on Sundays, and we do have cinnamon rolls." | **complaint**, urgency 3 (draft uses the facts) | question |
| Scam email | draft: "We'll be sure to claim the grant as soon as possible." | no draft (code rule) | no draft (code rule) |
| A draft promised something the owner never said | yes ("send it to you by Saturday") | yes ("Please allow us 24 hours") | yes ("Please pick up the new order by 12pm today") |

v3's one miss (birthday cake → catering) comes from our own definition: *catering = food for an event*.

**The three fixes (v1 → v2):** 1) the owner's facts in `facts.txt`, 2) a definition for every category and urgency level in
the prompt, 3) a hard rule in code: spam never gets a draft, whatever the model says.

**Lesson:** the AI sorts and drafts; the owner approves every reply. Keep score during a paid test (emails sorted right, drafts
changed and why) and fix the facts and definitions as you go.

## Privacy
Customer emails are personal data: get the owner's permission, keep the emails on their machine (that's why this uses a local
model), and tell the owner which parts the AI writes.

## Licenses
- `qwen3:1.7b`, `qwen3:4b` — Apache 2.0 ([Qwen3-1.7B](https://huggingface.co/Qwen/Qwen3-1.7B), [Qwen3-4B](https://huggingface.co/Qwen/Qwen3-4B)): commercial use allowed. Check the license yourself before client work.
- Ollama — MIT
- The code in this folder — MIT (see the repo LICENSE)

## Source for the number in the video
U.S. Chamber of Commerce, 2026 Empowering Small Business report (published Oct 2, 2026; survey of 3,732 U.S. small
businesses, July 23 – Aug 6, 2026): 66% of small businesses use AI, up from 23% in 2023; 28% of AI users use it to
communicate with customers. https://www.uschamber.com/technology/2026-empowering-small-business-report

## Credits
The hands-on, show-every-step segments of this tutorial are inspired by **[FreeAIVault](https://www.youtube.com/@FreeAIVaultTV)** — go check out their channel.
