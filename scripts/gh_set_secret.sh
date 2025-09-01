#!/usr/bin/env bash
# Script to set GitHub repository secrets using gh CLI. Run locally where gh is authenticated.
set -euo pipefail

if ! command -v gh >/dev/null 2>&1; then
  echo "gh CLI not found. Install and authenticate: https://cli.github.com/"
  exit 1
fi

if [ "$#" -lt 2 ]; then
  echo "Usage: $0 SECRET_NAME SECRET_VALUE"
  exit 1
fi

NAME="$1"
VALUE="$2"

gh secret set "$NAME" --body "$VALUE"
echo "Secret $NAME set in repository $(gh repo view --json name -q .name)"
