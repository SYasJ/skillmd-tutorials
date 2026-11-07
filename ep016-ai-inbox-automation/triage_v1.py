#!/usr/bin/env python3
"""Inbox triage for a small business: sort each customer email, rate urgency and draft a reply for a human to approve.

Usage:
    python3 triage.py inbox/

Needs Ollama running locally (https://ollama.com) and the model pulled:
    ollama pull qwen3:1.7b        # Apache 2.0: commercial use allowed (check the license yourself before client work)

Nothing is ever sent. Drafts go to drafts/<email>.txt and a summary to triage.csv; the owner reads, edits and sends.
Standard library only (Python 3.10+).
"""
import csv
import json
import logging
import pathlib
import sys
import time
import urllib.error
import urllib.request
from dataclasses import dataclass

OLLAMA_URL: str = "http://localhost:11434/api/chat"
MODEL: str = "qwen3:1.7b"
TEMPERATURE: float = 0.0
TIMEOUT_S: int = 600
ATTEMPTS: int = 3
CATEGORIES: list[str] = ["order", "catering", "complaint", "question", "wholesale", "spam"]

SYSTEM_PROMPT: str = (
    "You sort customer emails for Harbor Bakery, a small bakery. "
    "Pick exactly one category, rate urgency 1 (can wait) to 3 (today), "
    "write a one-line summary, and draft a short, friendly reply the owner can send. "
    "Never promise prices, dates or refunds. If something needs the owner's decision, say the owner will confirm."
)

# JSON schema the model must follow (Ollama structured outputs)
SCHEMA: dict[str, object] = {
    "type": "object",
    "properties": {
        "category": {"type": "string", "enum": CATEGORIES},
        "urgency": {"type": "integer", "minimum": 1, "maximum": 3},
        "summary": {"type": "string"},
        "reply": {"type": "string"},
    },
    "required": ["category", "urgency", "summary", "reply"],
}

log: logging.Logger = logging.getLogger("triage")


@dataclass(frozen=True)
class Triage:
    email: str
    category: str
    urgency: int
    summary: str
    reply: str
    seconds: float


class OllamaError(RuntimeError):
    """The local Ollama server returned an error, could not be reached, or broke the schema."""


def call_ollama(email_text: str) -> dict[str, object]:
    """One chat call with the JSON schema; retries with a warning, then raises the last error with context."""
    body: bytes = json.dumps({
        "model": MODEL, "stream": False, "think": False, "format": SCHEMA,
        "options": {"temperature": TEMPERATURE},
        "messages": [{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": email_text}],
    }).encode()
    last: Exception | None = None
    for attempt in range(1, ATTEMPTS + 1):
        req = urllib.request.Request(OLLAMA_URL, data=body, headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=TIMEOUT_S) as resp:
                return json.load(resp)
        except urllib.error.HTTPError as e:
            last = OllamaError(f"Ollama HTTP {e.code} for model={MODEL}: {e.read().decode(errors='replace')[:500]}")
        except urllib.error.URLError as e:
            last = OllamaError(f"Cannot reach Ollama at {OLLAMA_URL} (is it running?): {e.reason}")
        log.warning("ollama call failed", extra={"attempt": attempt, "model": MODEL, "error": str(last)})
        time.sleep(2 * attempt)
    assert last is not None
    raise last


def parse(resp: dict[str, object], email: str, seconds: float) -> Triage:
    """Validate the model's JSON against what we asked for; fail loudly instead of guessing."""
    msg = resp.get("message")
    content = msg.get("content") if isinstance(msg, dict) else None
    if not isinstance(content, str):
        raise OllamaError(f"No message content for {email}: {json.dumps(resp)[:500]}")
    data = json.loads(content)
    if data.get("category") not in CATEGORIES or data.get("urgency") not in (1, 2, 3):
        raise OllamaError(f"Model broke the schema for {email}: {content[:500]}")
    return Triage(email=email, category=data["category"], urgency=data["urgency"],
                  summary=str(data["summary"]).strip(), reply=str(data["reply"]).strip(), seconds=round(seconds, 1))


def triage_one(path: pathlib.Path) -> Triage:
    t0: float = time.time()
    resp = call_ollama(path.read_text(encoding="utf-8"))
    return parse(resp, path.name, time.time() - t0)


def write_outputs(results: list[Triage], out_dir: pathlib.Path) -> None:
    drafts = out_dir / "drafts"
    drafts.mkdir(parents=True, exist_ok=True)
    for r in results:
        (drafts / r.email).write_text(f"DRAFT — check before sending\n\n{r.reply}\n", encoding="utf-8")
    with (out_dir / "triage.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["email", "category", "urgency", "summary", "seconds"])
        for r in sorted(results, key=lambda r: -r.urgency):
            w.writerow([r.email, r.category, r.urgency, r.summary, r.seconds])


def main(argv: list[str]) -> None:
    if len(argv) != 2:
        raise SystemExit("usage: python3 triage.py <inbox-folder>")
    inbox = pathlib.Path(argv[1])
    emails = sorted(inbox.glob("*.txt"))
    if not emails:
        raise FileNotFoundError(f"No .txt emails in {inbox}")
    t0: float = time.time()
    results: list[Triage] = []
    for p in emails:
        r = triage_one(p)
        results.append(r)
        print(f"{r.email:<22} {r.category:<10} urgency {r.urgency}  {r.seconds:>5}s  {r.summary}")
    write_outputs(results, pathlib.Path("."))
    print(f"--- {len(results)} emails in {time.time() - t0:.1f}s ({MODEL}) · drafts/ + triage.csv written · nothing sent ---")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s %(message)s")
    main(sys.argv)
