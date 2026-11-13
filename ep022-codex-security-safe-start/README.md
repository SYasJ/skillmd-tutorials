# ep022 · OpenAI Codex Security — safe start (limits first)

From the skill.md video **[OpenAI Codex Security: No Cost Cap by Default, 96-Hour Deep Scans](https://www.youtube.com/watch?v=L05fB96mdC8)** (repo spotlight, Nov 14, 2026).

**Not run by us.** We read the README, `docs/cli.md`, `SECURITY.md`, the GitHub Action README and the release notes of
[openai/codex-security](https://github.com/openai/codex-security) (v0.10.0, Apache-2.0), and checked the npm package
(`npm view`: official OpenAI publisher, no preinstall/install/postinstall scripts). We did not run a scan: scans with OpenAI
models need Codex Security access, and our automated safety checks blocked running the CLI. Everything below is built
only from the official docs — check them again before you rely on it.

## What's in this folder

| File | What it is |
|---|---|
| `safe-scan.sh` | The commands from the README, plus a time limit and a cost limit on every scan |
| `codex-security.yml` | The official weekly GitHub Action example (`github-action/examples/repository.yml`), with notes on the two lines that matter |

## The fine print we cover in the video (all quoted from the docs, fetched Nov 13, 2026)

- **No cost limit unless you set one.** Action input `max-cost`: "unset means no cost limit". CLI `--max-cost USD` "stops the scan and workers after estimated cost exceeds the limit; in-flight requests can finish above it." "Without a limit, usage reporting remains best effort."
- **Deep Scan time.** Discovery time: "its default and maximum are 5760 minutes (96 hours)" (enforced).
- **Standard scan time.** "Standard scans have no time allowance by default." `--max-time` is advisory: "This is not a hard timeout or a minimum runtime."
- **Default model.** "The default model and effort are `gpt-5.6-sol` and `xhigh`." Up to 8 delegated workers.
- **Trust.** SECURITY.md: "Codex Security runs under your local account. Scan only repositories you trust and have permission to assess." Deep-scan workers are read-only, but that "does not make the worker an isolated, offline environment or disable inherited MCP servers."
- **Bug bounty.** "Prompt injection or a model misusing access it already has does not qualify by itself."
- **macOS note (policy generation).** "On macOS, the bundled runtime does not fully enforce write restrictions under `/tmp` (including `/private/tmp`)."
- **Access.** learn.chatgpt.com: "Scans using OpenAI inference require Codex Security access." Other providers in the README: Amazon Bedrock, OpenRouter, Fireworks AI, Cheaper Inference.

Our advice (opinion, not from the docs): set `--max-time` and `--max-cost` on every scan, start with `--diff origin/main`,
and scan code you don't trust inside a throwaway container or VM, not on your main machine.

## Licenses

- Codex Security (CLI, SDK, Action): Apache-2.0 — https://github.com/openai/codex-security/blob/main/LICENSE
- `codex-security.yml` is adapted from the official example in that repo (Apache-2.0).
- Our files here: MIT (see the root LICENSE).

## Credit

The hands-on, show-every-step style of this series is inspired by FreeAIVault (https://www.youtube.com/@FreeAIVaultTV).
Channel: skill.md on YouTube (video link at the top).
