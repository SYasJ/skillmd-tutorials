#!/bin/sh
# Minimal Claude Fable 5.2 call with the Anthropic Messages API.
# Needs your own key in ANTHROPIC_API_KEY. Prices (Nov 9, 2026): $8 / 1M input tokens, $40 / 1M output tokens.
# Usage: sh fable-call.sh "your prompt"
PROMPT="${1:-Say hello in five words.}"
curl -s https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "content-type: application/json" \
  -d "{\"model\":\"claude-fable-5-2\",\"max_tokens\":512,\"messages\":[{\"role\":\"user\",\"content\":\"$PROMPT\"}]}"
echo
