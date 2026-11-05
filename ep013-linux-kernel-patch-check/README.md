# ep013 · Linux kernel patch check (skill.md Daily, Nov 6 2026)

From the skill.md Daily video **"OpenAI Linux Kernel Exploits: AI Built 948 Root Hacks for $1.2M"** → https://www.youtube.com/watch?v=dMO3tmc9Ulw

On Nov 4, 2026 OpenAI described a research pipeline that, in one run, reproduced 1,724 Linux kernel bugs and produced 948 local privilege escalation (root) exploits for $1,213,430 in API credits ([OpenAI](https://openai.com/index/a-thousand-fewer-paths-to-root/)). OpenAI's advice: for now, a low-privileged account on a system that isn't fully patched "should be considered functionally equivalent to root access for a well-resourced threat actor." So: patch, and reboot.

## The three commands from the video

```bash
uname -r                                   # which kernel is running

# Ubuntu / Debian
sudo apt update && sudo apt full-upgrade

# Fedora
sudo dnf upgrade --refresh

sudo reboot                                # a new kernel only runs after a restart
```

## Optional: read-only check script

`check-kernel.sh` prints the running kernel, the newest installed kernel packages and whether a reboot is pending. It changes nothing.

```bash
bash check-kernel.sh
```

Read it before running it (it is 25 lines). Tested logic only on Debian/Ubuntu and Fedora package layouts; other distros get a generic hint.

## Licenses
This folder: MIT (see repo root). Linux is GPL-2.0. No third-party code is included.

---
Channel: **skill.md** — https://www.youtube.com/channel/UCMQcMb_sp9gmMCYzhHRaS8g
The hands-on, show-every-step style used across this repo is inspired by FreeAIVault (https://www.youtube.com/@FreeAIVaultTV).
