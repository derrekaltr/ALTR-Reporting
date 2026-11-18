#!/usr/bin/env bash
# Take the link offline immediately (removes the Vercel project named in slug.txt).
set -e
cd "$(dirname "$0")"
NAME="$(tr -d '[:space:]' < slug.txt)"
vercel remove "$NAME" --yes
rm -rf .vercel
echo "https://$NAME.vercel.app is gone."
