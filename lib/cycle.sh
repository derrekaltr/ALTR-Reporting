#!/bin/bash
# ALTR twice-monthly auto-publish cycle. Fully hands-off: refresh every data source,
# pull each model, write her prose headlessly, build, QA, and publish (Vercel + Drive)
# only if the typesetting gate and register checks pass. Reports are staged private
# links for Derrek to review before he forwards them to the models; nothing is sent to
# a creator by this job. Notifies Derrek (Telegram Saved Messages) with the run summary
# and any blockers. Scheduled by launchd on the 1st and 15th; also runnable by hand.
set -uo pipefail
export PATH="$HOME/.local/bin:/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin:$PATH"
KIT=~/Documents/altr-reports-kit
TG=~/Documents/altr-telegram
PY=/usr/bin/python3
DATESTR=$(date '+%B %-d, %Y')
PDFDATE=$(date '+%b%d' | tr '[:upper:]' '[:lower:]')
LOG=$TG/exports/cycle-$(date +%Y%m%d-%H%M).log
exec > >(tee -a "$LOG") 2>&1
echo "===== ALTR auto-publish cycle $(date) ====="
notify() { cd "$TG" && $PY notify.py "$1" 2>/dev/null; }
BLOCK=""; flag() { BLOCK="$BLOCK\n- $1"; echo "BLOCKER: $1"; }
PUBLISHED=""; FAILED=""

cd "$KIT" || { notify "CYCLE FAILED: kit folder missing"; exit 1; }

# Pull the team's latest code before running, so changes made during the fortnight go live on the
# next scheduled run without anyone touching this Mac. Never blocks the run if the remote is down.
if git -C "$KIT" remote | grep -q .; then
  BEFORE=$(git -C "$KIT" rev-parse --short HEAD 2>/dev/null)
  if git -C "$KIT" pull --ff-only --quiet 2>/dev/null; then
    AFTER=$(git -C "$KIT" rev-parse --short HEAD 2>/dev/null)
    [ "$BEFORE" != "$AFTER" ] && echo "code updated $BEFORE -> $AFTER" && CODE_NOTE="
Code updated to $AFTER before this run: $(git -C "$KIT" log --format=%s -1)"
  else
    echo "git pull skipped (local changes or remote unreachable)"
  fi
fi

# 1. connectivity / credit / auth preflight
ACCTS=$($PY lib/ofapi.py accounts 2>&1)
echo "$ACCTS" | grep -qE "No OnlyFans API key|\"_error\"|insufficient credits|HTTP 402" && flag "OnlyFans API unreachable or out of credits"
# Listing accounts is free, so it passes even with a zero balance; only a data endpoint reveals an
# empty wallet. Probe one (1 credit) or a whole run silently pulls nothing. (Sarah H, Nov 18 2026.)
FIRST_ACCT=$(head -1 "$KIT/lib/roster.txt" | cut -d"|" -f2)
CREDIT_PROBE=$($PY -c "
import sys; sys.path.insert(0, 'lib')
from ofapi import raw
d = raw('https://app.onlyfansapi.com/api/$FIRST_ACCT/me')
print('BLOCKED' if isinstance(d, dict) and '_error' in d else 'OK')" 2>&1 | tail -1)
if [ "$CREDIT_PROBE" != "OK" ]; then
  notify "CYCLE STOPPED before pulling: the OnlyFans API has no credits left, so no model data can be fetched. Top up at app.onlyfansapi.com, then rerun lib/cycle.sh. Nothing else was spent."
  echo "ABORT: onlyfans api out of credits"; exit 1
fi
# Only warn about accounts we actually report on. The dashboard holds departed models and spare
# pages too, and counting those cried wolf ("10 need re-auth" when all 17 rostered ones were fine).
AF_LIST=$(echo "$ACCTS" | $PY -c '
import sys, re
live = {}
for ln in sys.stdin:
    m = re.match(r"\s*(acct_\w+)\s+@?(\S*)\s+(.*?)\s+auth=(\w+)", ln)
    if m: live[m.group(1)] = (m.group(3).strip() or m.group(2), m.group(4) == "True")
bad = []
for ln in open("lib/roster.txt"):
    ln = ln.strip()
    if not ln: continue
    slug, acct, name, handle = ln.split("|")
    if acct not in live: bad.append((slug, f"{name} (not connected)"))
    elif not live[acct][1]: bad.append((slug, name))
open("/tmp/altr-skip-slugs", "w").write(" ".join(s for s, _ in bad))
print(", ".join(n for _, n in bad))')
[ -n "$AF_LIST" ] && flag "rostered account(s) need re-authentication: $AF_LIST"
SKIP_SLUGS=$(cat /tmp/altr-skip-slugs 2>/dev/null)

# Prose is written by the Claude CLI. If its usage credits are gone, every model fails after we have
# already paid for the OnlyFans pulls, so check it BEFORE pulling anything. (Cost us a full run Nov 3.)
CLAUDE_CHECK=$(echo 'Reply with the single word: ready' | claude -p 2>&1 | head -c 400)
if ! echo "$CLAUDE_CHECK" | grep -qi "ready"; then
  if echo "$CLAUDE_CHECK" | grep -qi "usage credits\|rate limit\|quota"; then
    notify "CYCLE STOPPED before pulling: Claude usage credits are exhausted, so no report prose can be written. Top up at https://claude.ai/settings/usage then rerun lib/cycle.sh. No OnlyFans credits were spent."
    echo "ABORT: claude -p unavailable: $CLAUDE_CHECK"; exit 1
  fi
  flag "Claude CLI check returned unexpected output: $CLAUDE_CHECK"
fi

# Vercel and Drive are the two publish paths. Both have failed silently at the END of a run before
# (Nov 15 2026: the CLI was pointed at the wrong ALTR team, so all 16 deploys were refused after an
# hour of work). Test them here, while failing costs nothing.
if ! vercel whoami >/dev/null 2>&1; then
  notify "CYCLE STOPPED before pulling: the Vercel CLI is not logged in, so no report could be published. Run 'vercel login' on the Mac, then rerun lib/cycle.sh. No credits were spent."
  echo "ABORT: vercel not logged in"; exit 1
fi
VC_PROBE=$(cd "$KIT/WORK/liza-weekly" 2>/dev/null && vercel project ls 2>&1 | grep -c "$(tr -d '[:space:]' < slug.txt)")
if [ "${VC_PROBE:-0}" -eq 0 ]; then
  notify "CYCLE STOPPED before pulling: Vercel is logged in but cannot see the report projects, which usually means the CLI is on the wrong team. Run 'vercel switch altr-022397ab' on the Mac, then rerun lib/cycle.sh. No credits were spent."
  echo "ABORT: vercel scope cannot see report projects"; exit 1
fi
if ! ( echo probe > /tmp/.altr-drive-probe && rclone copyto /tmp/.altr-drive-probe "gdrive-reports:.probe" >/dev/null 2>&1 \
       && rclone delete "gdrive-reports:.probe" >/dev/null 2>&1 ); then
  notify "CYCLE STOPPED before pulling: cannot write to the Google Drive reports folder. Check the rclone remote 'gdrive-reports'. No credits were spent."
  echo "ABORT: drive not writable"; exit 1
fi
rm -f /tmp/.altr-drive-probe

# 2. shared data sources
( cd "$TG" && $PY removelabs.py >/dev/null 2>&1 ) || flag "RemoveLabs DMCA parse failed"
( cd "$TG" && $PY social_pull.py --days 3 >/dev/null 2>&1 && $PY social_pull.py --days 7 >/dev/null 2>&1 ) || flag "Social refresh failed"

# 3. per-model: pull -> analyse -> prose -> build -> QA -> publish
while IFS='|' read -r slug acct name handle; do
  [ -z "$slug" ] && continue
  [ -d "WORK/$slug" ] || { FAILED="$FAILED $slug(no-folder)"; continue; }
  # An unauthenticated account returns 401s and empty data; building on that crashes with a
  # meaningless error. Skip it and say why. (Sarah H, Nov 15 2026.)
  case " $SKIP_SLUGS " in *" $slug "*) echo "--- $slug SKIPPED (needs re-authentication)"
    FAILED="$FAILED $slug(needs-reauth)"; continue;; esac
  echo "--- $slug"
  ( cd "WORK/$slug" && $PY ../../lib/pull_account.py "$acct" --days 7 --ledger-days 21 > pull.log 2>&1 \
      && $PY ../../lib/analyze_ledger.py > analysis.txt 2>&1 )
  # Real out-of-credits only (ofapi prints "402 insufficient credits"). A bare "402" grep used to match
  # unrelated account ids inside error text and killed the whole run, so keep this anchored.
  if grep -qE "insufficient credits|HTTP 402" "WORK/$slug/pull.log" 2>/dev/null; then
    flag "$slug hit 402 (out of credits); stopping pulls"; break; fi
  if grep -q "No connected account matches" "WORK/$slug/pull.log" 2>/dev/null; then
    FAILED="$FAILED $slug(not-connected)"; continue; fi
  if [ ! -f "WORK/$slug/data/cohort.json" ]; then FAILED="$FAILED $slug(pull)"; continue; fi
  if ! $PY lib/write_prose.py "$slug" "$handle" >/dev/null 2>&1; then FAILED="$FAILED $slug(prose)"; continue; fi
  $PY lib/make_builder.py "$slug" "$name" "$handle" "$DATESTR" "ALTR-$slug-$PDFDATE.pdf" >/dev/null 2>&1
  # Must check this: if the builder crashes, build.py happily re-renders the PREVIOUS cycle's stale
  # template.html and the model gets reported as published with last period's numbers. (Nov 3 2026.)
  if ! ( cd "WORK/$slug" && $PY build_premium.py > build.log 2>&1 ); then
    FAILED="$FAILED $slug(builder)"; continue; fi
  if ! ( cd "WORK/$slug" && $PY ../../lib/build.py >/dev/null 2>&1 ); then FAILED="$FAILED $slug(qa)"; continue; fi
  # register double-check in the built output
  if ( cd "WORK/$slug" && grep -liE "need from you|would you|please|comfortable" index.html print.html >/dev/null 2>&1 ); then
    FAILED="$FAILED $slug(register)"; continue; fi
  if ( cd "WORK/$slug" && bash deploy.sh >/dev/null 2>&1 ); then
    PUBLISHED="$PUBLISHED $slug"
  else
    FAILED="$FAILED $slug(deploy)"
  fi
done < "$KIT/lib/roster.txt"

# 3b. Spanish edition for Naza (she reads Spanish; the English build stays for Derrek's review).
# Translates the just-built naza-weekly output; its deploy.sh retries with shortened segments if qa_pdf objects.
if echo "$PUBLISHED" | grep -q "naza-weekly"; then
  if ( cd "$KIT/WORK/naza-es-weekly" && bash deploy.sh >/dev/null 2>&1 ); then
    PUBLISHED="$PUBLISHED naza-es-weekly"
  else
    FAILED="$FAILED naza-es-weekly(spanish)"
  fi
fi

# 4. VERIFY what actually exists, rather than trusting that each step returned 0.
# Every past failure was discovered by Derrek, not by this script, because "published" only meant
# "no command errored". Now we check the real artefacts: a PDF dated today, a file in Drive, and a
# live page showing today's date.
EXPECT=$(grep -c . "$KIT/lib/roster.txt")
VERIFIED=""; UNVERIFIED=""
DRIVE_LIST=$(rclone lsf "gdrive-reports:" -R --files-only 2>/dev/null)
HUMAN_DATE=$(date '+%B %-d, %Y')
while IFS='|' read -r slug acct name handle; do
  [ -z "$slug" ] && continue
  why=""
  [ -f "$KIT/WORK/$slug/ALTR-$slug-$PDFDATE.pdf" ] || why="no PDF"
  echo "$DRIVE_LIST" | grep -qF "$name - @$handle - $(date '+%B %-d %Y').pdf" || why="${why:+$why, }not in Drive"
  url="https://$(tr -d '[:space:]' < "$KIT/WORK/$slug/slug.txt" 2>/dev/null).vercel.app"
  curl -s --max-time 20 "$url" 2>/dev/null | grep -qF "$HUMAN_DATE" || why="${why:+$why, }page not showing today"
  if [ -z "$why" ]; then VERIFIED="$VERIFIED $slug"; else UNVERIFIED="$UNVERIFIED
  $slug: $why"; fi
done < "$KIT/lib/roster.txt"
NV=$(echo $VERIFIED | wc -w | tr -d ' ')

# 5. summary, built from what was verified
if [ "$NV" -eq "$EXPECT" ]; then
  MSG="Auto-publish $(date +%b\ %-d): all $NV reports verified live, in Drive and dated today. Staged for your review."
else
  MSG="Auto-publish $(date +%b\ %-d): WARNING only $NV of $EXPECT reports verified.$UNVERIFIED"
fi
[ -n "$FAILED" ] && MSG="$MSG\nFailed during the run:$FAILED"
[ -n "$BLOCK" ] && MSG="$MSG\nBLOCKERS:$(echo -e "$BLOCK")"
[ -n "$CODE_NOTE" ] && MSG="$MSG$CODE_NOTE"
notify "$MSG"
echo "verified:$VERIFIED"; echo "unverified:$UNVERIFIED"
echo "published:$PUBLISHED"; echo "failed:$FAILED"; echo "===== done $(date) ====="
