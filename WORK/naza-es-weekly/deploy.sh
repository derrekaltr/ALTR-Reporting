#!/usr/bin/env bash
# Spanish edition of ../naza-weekly. Translates the built source templates, renders, deploys, files to Drive.
set -e
cd "$(dirname "$0")"
python3 ../../lib/translate_report.py "../naza-weekly" .
# Spanish runs longer than English; if qa_pdf flags overflow or lone words, shorten those segments and retry (twice).
for try in 1 2 3; do
  if python3 ../../lib/build.py > /tmp/es-build.log 2>&1; then tail -2 /tmp/es-build.log; break; fi
  [ "$try" = 3 ] && { echo "!! Spanish render still failing qa_pdf after 2 shorten passes:"; tail -12 /tmp/es-build.log; exit 1; }
  python3 ../../lib/translate_report.py --shorten "../naza-weekly" . --log /tmp/es-build.log
done
NAME="$(tr -d '[:space:]' < slug.txt)"
export VERCEL_TELEMETRY_DISABLED=1
if [ ! -d .vercel ]; then
  vercel link --yes --project "$NAME" >/dev/null 2>&1 || vercel project add "$NAME" && vercel link --yes --project "$NAME"
fi
vercel deploy --prod --yes
PDF=$(python3 -c "import json;print(json.load(open('report.json'))['pdf'])")
DEST=$(python3 -c "import json;m=json.load(open('es-meta.json'));print(f\"{m['name']}/{m['name']} - {m['handle']} - {m['date'].replace(',','')} (Espanol).pdf\")")
rclone copyto "$PDF" "gdrive-reports:$DEST" && echo "uploaded -> $DEST" || echo "!! Drive upload failed; retry the rclone line by hand."
echo "live: https://$NAME.vercel.app   pdf: https://$NAME.vercel.app/$PDF"
