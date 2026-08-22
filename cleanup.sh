#!/bin/bash
echo "=== IMA CLEANUP START ==="
source ~/ima_kernel/.env

echo "[1/3] Closing all open PRs by imaosglobal..."
gh pr list --author imaosglobal --state open --json number,url,repository -q '.[] | [.repository.name, .number, .url] | @tsv' | while IFS=$'\t' read -r repo pr url; do
  echo "Closing PR #$pr in $repo"
  gh pr close $pr -R "$repo" -c "Closing — this was opened automatically by an unattended script without review. Apologies for the noise and for wasting maintainer time."
  sleep 2
done

echo "[2/3] Deleting forks created by imaosglobal..."
gh repo list imaosglobal --fork --json nameWithOwner -q '.[].nameWithOwner' | while read repo; do
  if [[ "$repo" != "imaosglobal/Ima-kernel" ]]; then
    echo "Deleting fork: $repo"
    gh repo delete $repo --confirm
    sleep 2
  fi
done

echo "[3/3] DONE. Please rotate your GH_TOKEN now at https://github.com/settings/tokens"
