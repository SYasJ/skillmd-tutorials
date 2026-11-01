# ep009 · Daily news checks (Nov 2, 2026)

Two things from **skill.md Daily, Nov 2 2026** that you can do right now.
Video: https://www.youtube.com/watch?v=0yPpbH5gLuU · channel: skill.md https://www.youtube.com/channel/UCMQcMb_sp9gmMCYzhHRaS8g

## 1 · Were you hit by the trojanized Claude Code extension in Cursor?

On Oct 29, 2026 Cursor's extension marketplace served malicious `Anthropic.claude-code` versions **2.1.312 and 2.1.313** (Windows + macOS), not built by Anthropic, between about 2:27am and 1:35pm PT. They tried to add an attacker SSH key labelled `svc-telemetry`, open a reverse SSH tunnel and persist. Official VS Code Marketplace and Open VSX versions were not affected (per The Hacker News).

Check (macOS / Linux), from Cursor's notice:

```bash
grep -qs svc-telemetry ~/.ssh/authorized_keys && echo "FOUND: you are impacted" || echo "not found"
```

Windows (PowerShell): use the exact command in Cursor's notice (it also checks `C:\ProgramData\ssh\administrators_authorized_keys`).

If it says FOUND:
- Uninstalling the extension may not be sufficient.
- macOS: download `remediate-macos.sh` from Cursor's notice and run it as the affected user, not as root. Windows: `remediate-windows.ps1` from an elevated PowerShell.
- Rotate credentials and sessions from a trusted (clean) system.

Source: https://cursor.com/blog/claude-code-extension-security-notice (Oct 29, updated Oct 30 2026) · https://thehackernews.com/2026/10/official-claude-code-vs-code-extension.html

## 2 · Opt your website out of AI training (robots.txt)

Add to `robots.txt` (see `robots.txt.example`):

```
User-Agent: __usage_ai-training
Disallow: /
```

Keep one folder open (example from the IETF draft):

```
User-Agent: __usage_ai-training
Disallow: /
Allow: /press-kit/
```

Notes:
- `__usage_ai-training` is a policy token, not a crawler: search engines can still index your pages.
- `User-Agent: *` does **not** cover it ("wildcard groups ... MUST NOT be interpreted as matching the policy token"). Name the token.
- Microsoft: honored from Feb 1, 2027 · Google: "intends to support" it "in early 2027" · OpenAI: aims to implement it "in the coming months". It is a voluntary signal and the IETF draft is not yet a standard.

Sources: https://blogs.bing.com/search/2026/10/your-content-your-choice-clearer-preferences-for-training-and-grounding/ · https://developers.google.com/crawling/docs/crawlers-fetchers/google-common-crawlers · https://openai.com/index/helping-websites-express-ai-training-preferences/ · https://datatracker.ietf.org/doc/draft-kelley-aipref-training-preference-signal/

---
The hands-on, show-every-step style of this series is inspired by FreeAIVault (https://www.youtube.com/@FreeAIVaultTV).
