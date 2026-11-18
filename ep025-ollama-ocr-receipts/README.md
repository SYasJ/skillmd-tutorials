# ep025 · Ollama OCR with GLM-OCR — receipts to checked JSON and a CSV, all local

Watch: [Ollama OCR Tutorial: Receipts to JSON Locally. It Skipped One Number](https://www.youtube.com/watch?v=2VSVu_ZFCh8)

Everything we ran on camera, in order. Real runs on an old Intel Mac, CPU only, no GPU (recorded 2026-11-17 UTC).
Ollama **0.30.11** · model **glm-ocr:q8_0** (1.8 GB; `glm-ocr:latest` is 2.7 GB) · Python packages `ollama` 0.6.3 + `pydantic` 2.14.3.
Every receipt and invoice here is **made up** (`make_images.py` draws them). Nothing is uploaded anywhere.

## Commands

```bash
mkdir -p /tmp/ocr-ep && cd /tmp/ocr-ep     # copy this folder's files here

# 01 · get the model (49 s in our run)
ollama pull glm-ocr:q8_0

# 02 · plain text. The prompt must be exact: "Text Recognition: <path>"   (75 s first run in ours)
time ollama run glm-ocr:q8_0 "Text Recognition: ./receipt.png"
# 03 · the same receipt as a bad phone photo (45 s, same text)
time ollama run glm-ocr:q8_0 "Text Recognition: ./receipt-photo.jpg"
#   what went wrong #1: both times it wrote "Tax 2.15" and dropped the printed "8.5%"
#   but it can answer a question about it (7 s):
time ollama run glm-ocr:q8_0 "What is the tax rate on this receipt, and how much was the tip? ./receipt.png"

# 04 · tables -> an HTML table (67 s)
time ollama run glm-ocr:q8_0 "Table Recognition: ./invoice.png"

# 05 · Python
python3 -m venv .venv && .venv/bin/pip install -q ollama pydantic
.venv/bin/python naive.py receipt.png      # what went wrong #2: no schema -> "total" twice, no shop, no items
.venv/bin/python receipt.py receipt.png    # schema via format= ; checks the math ; converts the date

# 07 · a whole folder -> receipts.csv (one row per image, with a status column)
time .venv/bin/python batch.py receipts receipts.csv
column -s, -t receipts.csv

# where the time goes
ollama run --verbose glm-ocr:q8_0 "Text Recognition: ./receipt-photo.jpg"

# done
ollama rm glm-ocr:q8_0
rm -rf /tmp/ocr-ep
```

## Files

| File | What it does |
|---|---|
| `receipt.py` | image → `Receipt` (Pydantic schema passed as `format=`), date converted in code, `find_problems()` checks items = subtotal and subtotal + tax = total |
| `naive.py` | the same request with no schema (what went wrong #2) |
| `batch.py` | every image in a folder → one CSV row, status `OK` or `CHECK: …` |
| `make_images.py` | draws the made-up receipt, the bad phone photo, the invoice and the 3 batch receipts (uses macOS system fonts; change the paths on other systems) |
| `receipt.png`, `receipt-photo.jpg`, `invoice.png`, `receipts/` | the sample images |
| `receipts.csv` | the CSV our run produced |

## What went wrong (all real, shown unedited in the video)

1. **It skips things.** The receipt prints `Tax 8.5%`; both transcripts said `Tax 2.15`. No error. Check the fields you need.
2. **"Extract this receipt as JSON" without a schema** gave `total` twice, no shop name and no items. Pass a schema in `format=`.
3. **The date is copied, not converted.** We asked for YYYY-MM-DD and got `11/14/2026`, exactly as printed. `receipt.py` converts it in code (`DATE_FORMATS`; `%m/%d/%Y` is US order — use `%d/%m/%Y` for day-first receipts).

Not tested: the `Formula Recognition:` prompt, handwriting, faded or folded real receipts. We tested a handful of clean, made-up images, not thousands — keep the checks.

## Licenses

- GLM-OCR model: MIT (zai-org/GLM-OCR on Hugging Face). Ollama: MIT. `ollama` Python library: MIT. Pydantic: MIT.
- The code in this folder: MIT (see the repo LICENSE).

The hands-on, show-every-step style of these tutorials is inspired by **[FreeAIVault](https://www.youtube.com/@FreeAIVaultTV)**. Channel: [skill.md](https://www.youtube.com/channel/UCMQcMb_sp9gmMCYzhHRaS8g).
