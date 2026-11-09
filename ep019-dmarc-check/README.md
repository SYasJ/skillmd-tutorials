# ep019 · Is Outlook bouncing your email? Check your DMARC record

From the skill.md Daily video: https://www.youtube.com/watch?v=CbBZbkyq_r8  (story 3, Nov 9 2026)

**What happened:** MailRoute reported (Nov 6, 2026) that since Nov 5 Outlook.com has been rejecting some email from domains that don't publish a DMARC record, including Hotmail, Live and MSN addresses. The bounce they saw: `550 5.7.1 Message rejected: Message lacks SPF/DKIM/DMARC Auth Records`. Microsoft had not announced this change when we checked. Microsoft's published rule (support page for error 550 5.7.515) covers senders of 5,000+ messages a day.
Sources: https://mailroute.net/blog/outlook-rejecting-email-without-dmarc · https://support.microsoft.com/outlook/fix-ndr-error-550-5-7-515-in-outlook-com

## The 30-second check

```sh
dig +short TXT _dmarc.example.com
```

- Output starting with `v=DMARC1` → you have a DMARC record.
- No output → add a DNS **TXT** record named `_dmarc` with the value:

```
v=DMARC1; p=none
```

`p=none` only asks receivers for reports; it doesn't block anything. Then make sure **SPF or DKIM passes** for the domain in your From address (a DMARC record alone isn't enough). On Microsoft 365, turn on DKIM for your own domain. Later, once the reports look clean, you can move to `p=quarantine` or `p=reject`.

## Check several domains at once

```sh
sh dmarc-check.sh example.com example.org
```

`dmarc-check.sh` only does DNS lookups (read-only). MIT license, like the rest of this repo.

---
Channel: [skill.md](https://www.youtube.com/channel/UCMQcMb_sp9gmMCYzhHRaS8g) · The hands-on, show-every-step style is inspired by FreeAIVault (https://www.youtube.com/@FreeAIVaultTV).
