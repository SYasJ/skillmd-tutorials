# ep007 · 3 checks before you install any AI app (fake ChatGPT + Claude desktop apps)

From the skill.md video **"Downloading the Claude Desktop App? Fake Ones on GitHub Hide Malware"** (AI news, Oct 2026):
https://www.youtube.com/watch?v=oTxNPO5FEX8

Channel: **skill.md** — https://www.youtube.com/channel/UCMQcMb_sp9gmMCYzhHRaS8g

## Why
On Oct 27, 2026 Check Point Research published "Yoba": fake GitHub repos + GitHub Pages sites advertising desktop
apps for "GPT-5.6 Sol", "GPT-6 Astra" and "Claude Opus". The ZIP release contains a legitimate, signed OpenAI or
Claude `Setup.exe` that sideloads a malicious `winmm.dll` placed next to it. Check Point found no sign that OpenAI,
Anthropic, ChatGPT or Claude were compromised.
- Blog: https://blog.checkpoint.com/research/yoba-malware-abuses-signed-chatgpt-and-claude-binaries-to-target-ai-users
- Technical report: https://research.checkpoint.com/2026/tricks-from-the-past-deployed-via-signed-chatgpt-and-claude-binaries/

## The 3 checks
1. **Source** — download from the vendor's own page: https://claude.com/download · https://chatgpt.com/download
   (Windows: their installers or the Microsoft Store listing). Not from a search result, a GitHub Pages site or a stranger's release.
2. **Repo owner** — `./check-repo.sh OWNER/REPO` (GitHub CLI): repo age, stars, owner type, org verification,
   release files + download counts. A brand-new personal account with one repo and zero stars "shipping" a big
   company's desktop app is a red flag.
3. **Signature + folder** —
   - Mac: `./check-signature-macos.sh /Applications/Claude.app` (shows the Developer ID / Team ID that signed it).
   - Windows: `check-signatures-windows.ps1 -Path <unzipped folder>` lists the signer of every .exe and .dll.
     A signed `Setup.exe` next to DLLs signed by nobody (or someone else) is exactly this trick.
     **Not run on camera** — we recorded on a Mac.

## What we ran (Oct 28, 2026, ~12:00 UTC)
- `gh api repos/<each of the 4 repos named in the report>` → 3 × `Not Found (HTTP 404)`; the fake "Claude Opus"
  repo still answered, with a release file `Setup-Claude.zip` (112,232,058 bytes, 170 downloads). Its owner account
  was created 69 seconds before the repo; 1 public repo; 0 stars. (We did not download or open the file.)
- `gh api repos/anthropics/claude-code` + `gh api orgs/anthropics` → Organization, verified, on GitHub since 2020.
- `codesign -dv --verbose=2 /Applications/Claude.app` → `Developer ID Application: Anthropic PBC (Q6L2SF6YDW)`.

## Already ran one of these installers?
Check Point says to treat it as a broader compromise, not just a crypto miner (the loader can deliver other payloads).

## License
MIT (this folder). GitHub CLI, codesign and PowerShell are their owners' tools, used under their own terms.

The hands-on, show-every-step style of these tutorials is inspired by FreeAIVault (https://www.youtube.com/@FreeAIVaultTV).
