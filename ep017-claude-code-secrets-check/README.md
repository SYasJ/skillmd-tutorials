# ep017 · Claude Code "Don't Ask Again" secrets check

From the skill.md Daily video **"Claude Code Security: 'Don't Ask Again' Leaked 2,539 Secrets"** (Nov 8, 2026) → https://www.youtube.com/watch?v=Ik5dX6UYb-w

## What happened (Nov 6–7, 2026)
Security firm Apiiro found that when you answer a Claude Code permission prompt with **"Yes, and don't ask again"**, Claude Code saves an allow rule in `.claude/settings.local.json`. If the rule is one exact command, any password or token you typed into that command is saved in plain text. Apiiro found 2,539 secrets in 1,994 public GitHub repositories (all sources). Report: [The Hacker News, Nov 7, 2026](https://thehackernews.com/2026/11/claude-codes-dont-ask-again-file.html).

## Check one project (30 seconds)
```bash
git ls-files .claude          # settings.local.json listed? then it is committed
cat .claude/settings.local.json   # look for passwords / tokens inside "allow" rules
```

## If it is committed or holds secrets
1. **Rotate every password, token and key it ever held — first.** Removing the file does not remove it from git history or forks.
2. Stop tracking it and ignore it in the project:
   ```bash
   git rm --cached .claude/settings.local.json
   echo ".claude/settings.local.json" >> .gitignore
   git commit -m "Stop tracking Claude Code local settings"
   ```
3. Delete the rules that contain secrets from your local file.
4. Next time keep secrets in environment variables (`$DB_URL`) so a saved rule only holds the variable name, and approve patterns like `Bash(npm run:*)` instead of one exact command.

## Check all your projects at once
`check-claude-settings.sh` (read-only, changes nothing) finds every `.claude/settings.local.json` and `.claude/settings.json` under a folder, says whether git tracks it or ever did, and counts lines that look like secrets:
```bash
bash check-claude-settings.sh ~/projects
```
Real run on a demo repo with a fake password:
```
/tmp/ep017-demo/.claude/settings.local.json
   tracked by git: YES (committed) | in git history: 1 commit(s) | lines that look like secrets: 1
```
The pattern match is a hint, not a scanner — open the file and read it. Passwords inside commands (`PGPASSWORD=`, `sshpass -p`, `mysql -p`) are what common scanners miss most.

## License
MIT (this folder). Uses only bash, git, grep, find.

---
The hands-on, show-every-step style of this series is inspired by FreeAIVault (https://www.youtube.com/@FreeAIVaultTV).
