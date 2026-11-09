#!/bin/sh
# dmarc-check.sh — check whether a domain publishes DMARC (and SPF) records.
# Usage: sh dmarc-check.sh example.com [another.com ...]
# Needs: dig (macOS/Linux: preinstalled or in bind-utils / dnsutils). Read-only: it only does DNS lookups.
[ $# -eq 0 ] && { echo "usage: sh dmarc-check.sh example.com [more domains]"; exit 1; }
for d in "$@"; do
  echo "== $d"
  dm=$(dig +short TXT "_dmarc.$d" | tr -d '"' | grep -i '^v=DMARC1' || true)
  if [ -n "$dm" ]; then echo "DMARC  OK      $dm"; else
    echo "DMARC  MISSING  add a TXT record named _dmarc with:  v=DMARC1; p=none"; fi
  spf=$(dig +short TXT "$d" | tr -d '"' | grep -i '^v=spf1' || true)
  if [ -n "$spf" ]; then echo "SPF    OK      $spf"; else echo "SPF    MISSING  (ask your email provider for the SPF record to publish)"; fi
done
echo "Note: DKIM can't be checked without your provider's selector name. Turn DKIM on in your email provider for your own domain."
