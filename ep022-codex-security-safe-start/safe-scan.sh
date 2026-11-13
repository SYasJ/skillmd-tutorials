#!/usr/bin/env bash
# ep022 · Codex Security safe start — commands from the openai/codex-security README + limits.
# NOT RUN BY US (see README.md). Requires Node.js 22.13+ (22.x), 24.x or 26.x and Python 3.10+.
set -euo pipefail

# 1) install + sign in (README Quick start)
npm install --global @openai/codex-security
cs login            # or: npx @openai/codex-security login

# 2) small first scan: only the changes from main, with a time allowance and a cost limit
#    --max-time = minutes (advisory for Standard scans), --max-cost = estimated USD
cs scan . --diff origin/main --max-time 15 --max-cost 5

# 3) read the REPORT path it prints (check the exclusions), then find it again later with:
cs scans show

# 4) export the saved threat model without another analysis
cs export --artifact threat-model --output threatmodel.md

# Deep Scan: set your own discovery limit (the default AND maximum is 96 hours)
# cs scan . --mode deep --max-time 90 --max-cost 20
