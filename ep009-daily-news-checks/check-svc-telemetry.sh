#!/bin/sh
# Check for the svc-telemetry SSH key added by the trojanized Anthropic.claude-code 2.1.312/2.1.313 (Cursor marketplace, Oct 29 2026).
# Read-only: it only searches your authorized_keys file.
grep -qs svc-telemetry ~/.ssh/authorized_keys && echo "FOUND: you are impacted - see Cursor's notice" || echo "not found"
