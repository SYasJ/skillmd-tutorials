# ep014 · NVIDIA Auto Ontology — the duplicate-column test

From the skill.md repo spotlight **"NVIDIA Auto Ontology: Stops AI Agents Guessing Your Data (Mostly)"**
Watch: https://www.youtube.com/watch?v=aU4_Ch_FYlE

## What's here

| File | What it is |
|---|---|
| `dupcols.py` | 15 lines of plain Python (stdlib `sqlite3` only) that reproduce the *pattern* described in [NVIDIA/auto-ontology issue #408](https://github.com/NVIDIA/auto-ontology/issues/408): building each result row as a dict keyed by column name silently drops columns that share a name. |
| `output.txt` | The real output of `python3 dupcols.py` from the video (Python 3, macOS). |

**This is our own code, not Auto Ontology's.** We did not run Auto Ontology for the video (it needs Docker and an NVIDIA API key); we read its README, code and issues on Nov 6, 2026.

## Run it

```bash
python3 dupcols.py
```

Expected:

```
1) same column names, no error:
columns : ['id', 'id', 'name', 'name']
raw row : (1, 100, 'Ada', 'first order')
as dict : {'id': 100, 'name': 'first order'}

2) fix: give every column its own name:
columns : ['customer_id', 'order_id', 'customer', 'order_name']
raw row : (1, 100, 'Ada', 'first order')
as dict : {'customer_id': 1, 'order_id': 100, 'customer': 'Ada', 'order_name': 'first order'}
```

**The takeaway:** if you use a text-to-SQL agent (Auto Ontology or any other) whose connector returns rows as dicts, alias every column in joins (`c.id AS customer_id, o.id AS order_id`). Issue #408 reports the same loss on Auto Ontology's Postgres, MySQL and SQLite connectors, with `error=None`, so nothing retries. Check the issue for the current status.

## Licenses

- `dupcols.py`: MIT (this repo).
- NVIDIA Auto Ontology: Apache-2.0 — https://github.com/NVIDIA/auto-ontology (not included here).

---
Channel: [skill.md on YouTube](https://www.youtube.com/channel/UCMQcMb_sp9gmMCYzhHRaS8g)
The hands-on, show-every-step style of these tutorials is inspired by FreeAIVault (https://www.youtube.com/@FreeAIVaultTV).
