# ep021 · Try Claude Fable 5.2 from the API (one curl call)

From the skill.md Daily video: https://www.youtube.com/watch?v=-5oWKU8YPtE  (story 1, Nov 10 2026)

**What happened:** On Nov 9, 2026 Anthropic released Claude Fable 5.2 and Claude Mythos 5.2 ("the same underlying model"; Fable has cyber and biology safeguards and is available to everyone, Mythos goes to vetted organizations). The API model ID is `claude-fable-5-2`. Price: $8 per million input tokens and $40 per million output tokens (fast mode $16 / $80).
Source: https://www.anthropic.com/claude-fable-and-mythos-5-2

## The call

```sh
export ANTHROPIC_API_KEY=...   # your own key, never commit it
sh fable-call.sh "Explain what formalizing a proof means in two sentences."
```

`fable-call.sh` is a plain Messages API request (`POST https://api.anthropic.com/v1/messages`) with `"model": "claude-fable-5-2"` and `max_tokens` 512 to keep the cost small. Keep the prompt free of double quotes, or build the JSON with `jq`.

**Tip from the video:** Artificial Analysis lists Fable 5.2 at max effort as #1 of 74 on its Intelligence Index, but also the most expensive per task (~$26.54). Test it on your own tasks, and compare against a cheaper model, before switching.

Note: we did not run this call on camera (no paid key used in the video); it follows the standard Messages API format. MIT license, like the rest of this repo.

---
Channel: [skill.md](https://www.youtube.com/channel/UCMQcMb_sp9gmMCYzhHRaS8g) · The hands-on, show-every-step style is inspired by FreeAIVault (https://www.youtube.com/@FreeAIVaultTV).
