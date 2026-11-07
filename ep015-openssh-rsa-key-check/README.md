# ep015 · OpenSSH password-bypass + RSA key-size check (skill.md Daily, Nov 7 2026)

From the skill.md Daily video **"AI News Today: DeepMind AI Agents Found 2 Holes in Old RSA Encryption"** → https://www.youtube.com/watch?v=HIPSQjlh7R0

Two read-only checks from the video:

1. **OpenSSH 10.6p2 (Nov 5, 2026)** fixes an sshd password authentication bypass on Linux builds that use musl libc **without PAM** (e.g. Alpine). With some account setups, any password of 256–1,024 characters was accepted ([OpenSSH release notes](https://www.openssh.org/releasenotes.html#10.6p2), [CVE-2026-123158](https://raw.githubusercontent.com/CVEProject/cvelistV5/main/cves/2026/123xxx/CVE-2026-123158.json)). Alpine lists 3.16 → edge as affected when password login is on, an account has `*` as its password and another account has a `$5$`/`$6$` hash ([Alpine advisory](https://alpinelinux.org/posts/2026-11-05-openssh-password-authentication-bypass/)).
2. **Legacy 1024-bit RSA:** on Nov 6, 2026 Google DeepMind said its AI agents, guided by cryptanalysts, found two weaknesses in legacy 1024-bit RSA (signature forgery ~1,600x better than the previous best by DeepMind's theoretical estimate; batch factoring ~30x cheaper per extra key). RSA-2048 and larger are not affected. If you still have 1024-bit keys, replace them.

## Alpine: fix (from the Alpine advisory)

```bash
apk upgrade -U -a
rc-service sshd restart            # upgrading the package does NOT restart a running sshd
sshd -T | grep -i passwordauthentication
```

Can't update yet? Set `PasswordAuthentication no` (Alpine suggests a drop-in `/etc/ssh/sshd_config.d/00-no-passwords.conf`), make sure key login works first and keep your session open, then `sshd -t && rc-service sshd restart`.

## Key size checks (read-only)

```bash
ssh-keygen -lf ~/.ssh/id_rsa.pub                       # first number = bits; 1024 -> replace
openssl x509 -in cert.pem -noout -text | grep "Public-Key"
ssh-keygen -t ed25519                                   # make a new key if you need one
```

## Optional: `check-ssh.sh`

Prints the OpenSSH version, whether sshd allows password logins, whether the libc is musl, and the size of your RSA public keys. It changes nothing. Read it first.

```bash
sh check-ssh.sh
```

---
The hands-on, show-every-step style of this series is inspired by FreeAIVault (https://www.youtube.com/@FreeAIVaultTV). Code: MIT.
