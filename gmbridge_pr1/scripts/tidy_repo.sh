#!/usr/bin/env bash
set -euo pipefail

echo "==> Adding .gitignore entries"
{ 
  echo "secret.key"
  echo "config.enc"
  echo "dropship.db"
  echo "synced.db"
  echo "dropship.log"
  echo ".env"
} >> .gitignore || true

echo "==> Renaming Procfile.txt -> Procfile (if present)"
if [ -f "Procfile.txt" ]; then
  git mv -f Procfile.txt Procfile || mv Procfile.txt Procfile
fi

echo "==> Renaming requirements.txt.txt -> requirements.txt (if present)"
if [ -f "requirements.txt.txt" ]; then
  git mv -f requirements.txt.txt requirements.txt || mv requirements.txt.txt requirements.txt
fi

echo "==> Creating archive/ and moving legacy copies"
mkdir -p archive
for p in dropship-automator python-getting-started dropship_automator_sandbox_ready.py Global_Marketplace_Bridge.txt; do
  if [ -e "$p" ]; then
    git mv -f "$p" "archive/$(basename "$p")" || mv "$p" "archive/$(basename "$p")"
  fi
done

echo "==> Stop tracking local artifacts"
git rm --cached -f secret.key config.enc dropship.db synced.db dropship.log || true

echo "==> Commit changes"
git add .gitignore Procfile requirements.txt .github/workflows/ scripts/tidy_repo.sh archive || true
git commit -m "chore(repo): cleanup secrets, add Procfile & CI, archive legacy" || true

echo "==> Done. Review the commit and push."
