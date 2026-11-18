#!/usr/bin/env bash
# Build the report, then deploy it to Vercel under the project name in slug.txt (same URL every time).
# Needs: npm i -g vercel  and  vercel login  (once). The link is https://<slug.txt>.vercel.app
set -e
cd "$(dirname "$0")"
python3 build_premium.py
python3 ../../lib/build.py || { echo; echo "!! qa_pdf found issues. Fix them at the source, rebuild, then deploy."; exit 1; }
NAME="$(tr -d '[:space:]' < slug.txt)"
export VERCEL_TELEMETRY_DISABLED=1
# first deploy links the folder to a project with that exact name; later deploys reuse .vercel/
if [ ! -d .vercel ]; then
  # The team must be named explicitly: vercel applies no default in non-interactive mode,
  # and the account has two teams called ALTR. (Nov 2026.)
  vercel link --yes --project "$NAME" --scope altr-022397ab >/dev/null 2>&1 \
    || (vercel project add "$NAME" --scope altr-022397ab && vercel link --yes --project "$NAME" --scope altr-022397ab)
fi
vercel deploy --prod --yes --scope altr-022397ab
echo
echo "live: https://$NAME.vercel.app   pdf: https://$NAME.vercel.app/$(python3 -c "import json;print(json.load(open('report.json'))['pdf'])")"
echo "check it on your phone before sending. data/ and qa/ are not deployed (see .vercelignore)."
python3 ../../lib/deliver.py . || echo "!! Drive upload failed (report still live on Vercel); retry: python3 ../../lib/deliver.py ."

