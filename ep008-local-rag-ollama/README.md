# ep008 · Local RAG with Ollama: chat with your PDFs (Python, no LangChain)

**Watch:** https://www.youtube.com/watch?v=6uEi19mQSBg (skill.md, publishes 2026-10-30)

A free local model (llama3.2:3b) invented an answer about a NASA PDF. With RAG — chunks, embeddings, the 4 closest chunks, then an answer that must quote its page — it answered correctly. One file, 48 lines, two pip packages, everything runs on your computer.

## What's here

| File | What it is |
|---|---|
| `rag.py` | The final script (48 lines): prompt asks for the exact quote, nomic prefixes, keyword boost for rare words |
| `versions/rag_v1.py` | Version 1 (44 lines), as first run in the video |
| `versions/rag_v2.py` | + "give the complete answer, then quote the exact sentence" (fix for mistake 1) |
| `versions/rag_v3.py` | + `search_document:` / `search_query:` prefixes from the nomic-embed-text model card (did not fix mistake 2 by itself) |
| `requirements.txt` | `ollama==0.6.3`, `pypdf==6.21.4` |
| `run-log.md` | Every real run from the video: command, output, time |

## Run it

```bash
# 1. models (Ollama must be installed: https://ollama.com/download)
ollama pull nomic-embed-text      # 274 MB, embedding model
ollama pull llama3.2:3b           # 2.0 GB, chat model

# 2. packages, in a virtual environment
python3 -m venv .venv && source .venv/bin/activate
pip install ollama pypdf

# 3. ask a question about any PDF (the first run builds file.pdf.index.json)
python rag.py artemis-ii-reference-guide.pdf "Who built the TACHELES payload on Artemis II, and what does it test?"
```

The example PDF is NASA's *Artemis II Reference Guide* (2026, 138 pages): https://www.nasa.gov/artemis-ii-media-resources/ — download it there (not included here). Any text PDF works.

Questions used in the video:

```
python rag.py artemis-ii-reference-guide.pdf "Who built the TACHELES payload on Artemis II, and what does it test?"
python rag.py artemis-ii-reference-guide.pdf "How many radiation sensors covered the Orion spacecraft on Artemis I?"
python rag.py artemis-ii-reference-guide.pdf "On what date did Artemis II actually launch?"
```

## What happened (real runs, see run-log.md)

- **No RAG:** llama3.2:3b invented "Technological Adaptation of CubeSats for Habitat Exploration" and "a radiation shield made of water and liquid hydrogen" (31 s).
- **v1, first run:** indexed 525 chunks in 122 s; answered "German Aerospace Center (DLR) … electrical components", page 78 (19 s). But the sources were p.117, p.86, p.78, p.126 — only p.78 is about TACHELES.
- **Mistake 1:** "5,600 (page 15)" — page 15 says 5,600 passive **and 34 active**. Fix: ask for the complete answer + the exact quote (v2).
- **Mistake 2:** embeddings match meaning, not spelling, so the rare name TACHELES pulled the wrong pages. The model-card prefixes (v3) alone did not help (p.115, p.10, p.58, p.78). A keyword boost for words found in fewer than 2% of chunks did: p.78 first, p.17 joins, complete answer.
- **Not in the PDF:** final version says "I don't know". v1 said "I don't know" and then mixed in Artemis I's launch date (Nov. 16, 2022).

## Tips

1. "Page" = the PDF page (page 15 is printed as page 9 in this PDF).
2. Build the index once; answers then took 7–41 s here (CPU, laptop).
3. Use the same embedding model for indexing and questions (Ollama docs). Changed the model? Delete the `.index.json` and rebuild.
4. Scanned PDFs have no text layer; pypdf returns nothing — OCR them first.

## Licenses

- This folder: MIT (see the repo LICENSE).
- [ollama-python](https://github.com/ollama/ollama-python): MIT · [pypdf](https://github.com/py-pdf/pypdf): BSD-3-Clause
- [nomic-embed-text](https://huggingface.co/nomic-ai/nomic-embed-text-v1.5): Apache-2.0 · [Llama 3.2](https://ollama.com/library/llama3.2): Llama 3.2 Community License (Meta)
- The NASA PDF is a US government work used as an example; no endorsement by NASA, Meta, Nomic or Ollama is implied.

---
Channel: **skill.md** — https://www.youtube.com/channel/UCMQcMb_sp9gmMCYzhHRaS8g
The hands-on, show-every-step style is inspired by FreeAIVault (https://www.youtube.com/@FreeAIVaultTV).
