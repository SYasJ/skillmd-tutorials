#!/usr/bin/env python3
"""Draft-translate a short business text with a local Ollama model, then hand it to a human to check.

Usage:
    python3 translate.py sample-en.txt French

Needs Ollama running locally (https://ollama.com) and the model pulled:
    ollama pull qwen2.5-coder:3b

The model output is a DRAFT. A human who speaks the target language checks every number, name and sentence.

License: qwen2.5-coder:3b is under the Qwen RESEARCH LICENSE AGREEMENT (non-commercial: research or evaluation only).
It is fine for trying this workflow. For paid client work, switch MODEL to one whose license allows commercial use,
and read that license first.
"""
import json
import logging
import pathlib
import sys
import time
import urllib.error
import urllib.request
from dataclasses import dataclass

OLLAMA_URL: str = "http://localhost:11434/api/generate"
MODEL: str = "qwen2.5-coder:3b"
TEMPERATURE: float = 0.0
TIMEOUT_S: int = 600
ATTEMPTS: int = 3

log: logging.Logger = logging.getLogger("translate")


@dataclass(frozen=True)
class Draft:
    text: str
    seconds: float
    tokens: int


class OllamaError(RuntimeError):
    """The local Ollama server returned an error or could not be reached."""


def build_prompt(source: str, language: str) -> str:
    """The exact prompt shown in the video."""
    return (f"Translate the following English business text into {language}. "
            "Keep numbers, units and names exactly. "
            "Output only the translation.\n\n" + source)


def call_ollama(prompt: str, model: str, temperature: float) -> dict[str, object]:
    """One POST to Ollama; retries with a warning, then raises the last error with context."""
    body: bytes = json.dumps({"model": model, "prompt": prompt, "stream": False,
                              "options": {"temperature": temperature}}).encode()
    last: Exception | None = None
    for attempt in range(1, ATTEMPTS + 1):
        req = urllib.request.Request(OLLAMA_URL, data=body, headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=TIMEOUT_S) as resp:
                return json.load(resp)
        except urllib.error.HTTPError as e:
            last = OllamaError(f"Ollama HTTP {e.code} for model={model}: {e.read().decode(errors='replace')[:500]}")
        except urllib.error.URLError as e:
            last = OllamaError(f"Cannot reach Ollama at {OLLAMA_URL} (is it running?): {e.reason}")
        log.warning("ollama call failed", extra={"attempt": attempt, "model": model, "error": str(last)})
        time.sleep(2 * attempt)
    assert last is not None
    raise last


def translate(source: str, language: str) -> Draft:
    t0: float = time.time()
    resp: dict[str, object] = call_ollama(build_prompt(source, language), MODEL, TEMPERATURE)
    text = resp.get("response")
    if not isinstance(text, str) or not text.strip():
        raise OllamaError(f"Empty response from model={MODEL}: {json.dumps(resp)[:500]}")
    tokens = resp.get("eval_count")
    return Draft(text=text.strip(), seconds=round(time.time() - t0, 1), tokens=tokens if isinstance(tokens, int) else 0)


def main(argv: list[str]) -> None:
    if len(argv) != 3:
        raise SystemExit("usage: python3 translate.py <source.txt> <Language>")
    path, language = pathlib.Path(argv[1]), argv[2]
    if not path.is_file():
        raise FileNotFoundError(f"Source file not found: {path}")
    draft: Draft = translate(path.read_text(encoding="utf-8"), language)
    print(f"--- DRAFT ({MODEL}, {draft.seconds}s, {draft.tokens} tokens) — check before sending ---")
    print(draft.text)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s %(message)s")
    main(sys.argv)
