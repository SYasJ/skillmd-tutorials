#!/usr/bin/env bash
# Check 02 — who is behind a GitHub repo before you download anything from it.
# Needs the GitHub CLI (https://cli.github.com) and `gh auth login`.
# usage: ./check-repo.sh OWNER/REPO
set -euo pipefail
repo="${1:?usage: ./check-repo.sh OWNER/REPO}"
owner="${repo%%/*}"
echo "== repo $repo"
gh api "repos/$repo" --jq '"created_at   \(.created_at)\nstargazers   \(.stargazers_count)\nforks        \(.forks_count)\nowner type   \(.owner.type)"'
echo "== owner $owner"
if gh api "orgs/$owner" >/dev/null 2>&1; then
  gh api "orgs/$owner" --jq '"organization created_at \(.created_at)\nis_verified  \(.is_verified)\npublic_repos \(.public_repos)"'
else
  gh api "users/$owner" --jq '"user created_at \(.created_at)\npublic_repos \(.public_repos)"'
fi
echo "== release files"
gh api "repos/$repo/releases" --jq '.[].assets[] | "\(.name)  \(.size) bytes  \(.download_count) downloads"' || true
