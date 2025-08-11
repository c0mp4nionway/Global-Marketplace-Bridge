#!/usr/bin/env bash
set -euo pipefail
ORG_OR_USER=${1:?Usage: setup_github.sh <org-or-user> <repo>}
REPO=${2:?Usage: setup_github.sh <org-or-user> <repo>}
FULL="$ORG_OR_USER/$REPO"

echo "==> Creating labels"
gh label create "area/core" -R "$FULL" --color 0366d6 --description "Core API/service" || true
gh label create "area/web" -R "$FULL" --color 0e8a16 --description "Web frontend" || true
gh label create "area/worker" -R "$FULL" --color fbca04 --description "Worker & jobs" || true
gh label create "track/affiliate" -R "$FULL" --color d93f0b --description "Affiliate engine" || true
gh label create "track/category" -R "$FULL" --color 5319e7 --description "Category intelligence" || true
gh label create "priority/p0" -R "$FULL" --color b60205 --description "Blocker" || true
gh label create "priority/p1" -R "$FULL" --color d93f0b --description "High" || true
gh label create "priority/p2" -R "$FULL" --color fbca04 --description "Medium" || true

echo "==> Creating milestones"
gh milestone create -R "$FULL" "M1: Foundation" --description "Weeks 1-4: Affiliate, Inventory/Offer pipeline" || true
gh milestone create -R "$FULL" "M2: Category v1" --description "Weeks 2-8: Taxonomy+embeddings, adjudication UI" || true
gh milestone create -R "$FULL" "M3: Web App" --description "Weeks 1-10: Next.js basic screens + onboarding" || true
gh milestone create -R "$FULL" "M4: Reliability" --description "Weeks 3-10: jobs, retries, metrics, alerts" || true

echo "==> Creating issues"
gh issue create -R "$FULL" -t "Wire Inventory → Offer → Publish (simulation to live switch)" -b "Acceptance: 95% success, P95 < 10s" -l "area/core,priority/p1" -m "M1: Foundation" || true
gh issue create -R "$FULL" -t "Affiliate redirector + click logs (PID, sub-IDs)" -b "Acceptance: 99% click capture, EPC dashboard" -l "track/affiliate,priority/p1" -m "M1: Foundation" || true
gh issue create -R "$FULL" -t "Taxonomy API integration & category suggestions" -b "Acceptance: accuracy@1 >= 70%" -l "track/category,priority/p1" -m "M2: Category v1" || true
gh issue create -R "$FULL" -t "Adjudication UI (top-3, reasons, approve/override)" -b "Acceptance: resolve 90% low-confidence in 1 click" -l "track/category,area/web,priority/p2" -m "M2: Category v1" || true
gh issue create -R "$FULL" -t "Next.js app: dashboard/import/affiliate/jobs/settings" -b "Acceptance: 6 screens online, CWV pass" -l "area/web,priority/p2" -m "M3: Web App" || true
gh issue create -R "$FULL" -t "Job queue + retries + idempotency" -b "Acceptance: visible retries, idempotent keys" -l "area/worker,priority/p1" -m "M4: Reliability" || true

echo "Done. Open the project board and organize."
