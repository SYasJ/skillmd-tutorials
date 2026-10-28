#!/usr/bin/env bash
# Check 03 (Mac) — who signed an app. usage: ./check-signature-macos.sh /Applications/Claude.app
set -euo pipefail
app="${1:?usage: ./check-signature-macos.sh /path/to/App.app}"
codesign -dv --verbose=2 "$app" 2>&1 | grep -E "Identifier|Authority|TeamIdentifier"
codesign --verify --deep --strict "$app" && echo "signature verifies OK"
