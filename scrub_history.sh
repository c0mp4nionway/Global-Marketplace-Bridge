#!/usr/bin/env bash
# Scrub sensitive files & strings from the entire Git history and force-push the cleaned repo.
# Repo: c0mp4nionway/Global-Marketplace-Bridge

set -euo pipefail

# ---- CONFIG ----
OWNER="c0mp4nionway"
REPO="Global-Marketplace-Bridge"
REMOTE_URL="https://github.com/${OWNER}/${REPO}.git"
WORKDIR="$(pwd)"
MIRROR_DIR="${WORKDIR}/gmbridge.clean.git"

# Files/paths to remove from ALL history:
read -r -d '' PATHS_TO_REMOVE << 'EOF'
secret.key
config.enc
dropship.db
synced.db
dropship.log
.env
EOF

# Extra globs to remove:
GLOBS=(
  "*.sqlite"
  "*.sqlite3"
  "*.log"
)

# String redactions (regex -> replacement). Add more lines as needed.
read -r -d '' REPLACEMENTS << 'EOF'
# eBay Client IDs (SBX/PRD) -> mask
regex:(?i)circleco-circlegr-(?:sbx|prd)-[a-z0-9-]+==>EBAY_CLIENT_ID_REDACTED
# eBay Client Secret -> mask
regex:(?i)\b(?:sbx|prd)-[a-z0-9-]{8,}==>EBAY_CLIENT_SECRET_REDACTED
# eBay User Tokens (pattern often starts with v^1.) -> mask
regex:(?i)v\^1\..*#.*==>EBAY_USER_TOKEN_REDACTED
# Generic bearer/api tokens (add your own patterns below)
# regex:(?i)(?:apikey|api_key|secret|token)\s*[:=]\s*['"]?[A-Za-z0-9._\-]{16,}['"]?==>REDACTED
EOF

# ---- FUNCTIONS ----
need() {
  command -v "$1" >/dev/null 2>&1 || { echo "Missing dependency: $1"; return 1; }
}

confirm() {
  read -rp "$1 [y/N] " ans
  [[ "${ans,,}" == "y" || "${ans,,}" == "yes" ]]
}

echo "==> PREP: Ensure repo activity is paused and branch protection temporarily disabled (if needed)."
echo "    Repo: ${REMOTE_URL}"
echo

# 0) Dependencies
echo "==> Checking dependencies…"
need git
if ! python -c "import git_filter_repo" >/dev/null 2>&1; then
  echo "git-filter-repo not found; installing into user site-packages…"
  python -m pip install --user git-filter-repo
fi

# 1) Fresh mirror clone
echo "==> Mirror-cloning ${REMOTE_URL} → ${MIRROR_DIR}"
rm -rf "${MIRROR_DIR}"
git clone --mirror "${REMOTE_URL}" "${MIRROR_DIR}"
cd "${MIRROR_DIR}"

# 2) Write removal lists
echo "==> Preparing removal and redaction configs…"
printf "%s" "${PATHS_TO_REMOVE}" > paths-to-remove.txt
printf "%s" "${REPLACEMENTS}" > replacements.txt

# 3) Remove files/paths across history
echo "==> Removing sensitive files across all history…"
cmd=(git filter-repo --force --invert-paths --paths-from-file paths-to-remove.txt)
for g in "${GLOBS[@]}"; do
  cmd+=(--path-glob "$g")
done
"${cmd[@]}"

# 4) Redact string patterns
echo "==> Redacting common secret patterns…"
git filter-repo --force --replace-text replacements.txt

# 5) Garbage-collect to shrink objects
echo "==> Cleaning up unreachable blobs…"
git reflog expire --expire=now --all
git gc --prune=now --aggressive

echo
echo "==> READY to force-push cleaned history to origin (${REMOTE_URL})."
echo "    NOTE: This rewrites history. All collaborators must re-clone afterward."
confirm "Proceed with FORCE PUSH?" || { echo "Aborted before push."; exit 1; }

# 6) Force-push rewritten history
git push --force --tags origin --prune

echo
echo "==> DONE."
cat << 'POST'
Next steps:
  1) Re-enable branch protection and CI on main.
  2) Rotate any secrets that *ever* touched the repo (Fernet key, eBay creds/tokens, AliExpress/affiliate keys).
  3) Ask collaborators to re-clone (history changed).
  4) Add/verify .gitignore stops these files (already covered in your PR bundle).
  5) Optional: scan again
       gitleaks detect --source .
       trufflehog filesystem --no-update .
POST
