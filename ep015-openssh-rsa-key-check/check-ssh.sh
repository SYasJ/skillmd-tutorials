#!/bin/sh
# Read-only: OpenSSH version, password login setting, libc, RSA key sizes. Changes nothing.
echo "== OpenSSH version"; ssh -V 2>&1
if command -v sshd >/dev/null 2>&1; then
  echo "== sshd PasswordAuthentication (needs root to read the full config)"
  sshd -T 2>/dev/null | grep -i '^passwordauthentication' || echo "run as root to see: sshd -T | grep -i passwordauthentication"
fi
echo "== libc"; if ldd --version 2>&1 | grep -qi musl; then echo "musl (check the OpenSSH 10.6p2 / Alpine advisory)"; else ldd --version 2>&1 | head -1; fi
echo "== RSA public keys in ~/.ssh"
for k in "$HOME"/.ssh/*.pub; do [ -f "$k" ] || continue; ssh-keygen -lf "$k"; done | grep -i rsa || echo "no RSA keys found"
echo "Anything showing 1024 (RSA) -> replace it. Fix for Alpine: apk upgrade -U -a && rc-service sshd restart"
