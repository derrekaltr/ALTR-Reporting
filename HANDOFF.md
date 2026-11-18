# ALTR Reporting System — Handoff

Written October 30, 2026. Owner: Derrek (derrek@altrmgmt.com). Built with Claude Code.

This document is for someone picking up this system cold, or lifting a piece of it into another
project. Every part runs standalone. No credentials are in this file; the inventory at the bottom
says where each one lives on the machine.

---

## What this is

Twice a month (the 1st and 15th, 6:00 AM ET), this machine automatically builds a styled
earnings-and-activity report for every ALTR model: pulls OnlyFans data, scans team chats for open
items, parses DMCA takedown PDFs, pulls social media stats, writes the prose, builds a web page +
PDF, QA-gates it, deploys to Vercel, and files the PDF into Google Drive. It then messages Derrek
on Telegram with a summary or any blockers.

**Hard rule: nothing is ever sent to a model automatically.** Publishing means staging for
Derrek's review. Any message to a client chat requires his explicit go, per send.

## The three projects

| Project | Path | Job |
|---|---|---|
| Report kit | `~/Documents/altr-reports-kit` | Templates, builders, QA, deploy, Drive delivery, the cycle script |
| Chat scanners | `~/Documents/altr-telegram` | Telegram open-items scan, iMessage scan, WhatsApp DMCA PDF parse, Telegram notify |
| Social pipeline | `~/Documents/altr-social` | Instagram / TikTok / X / Facebook stats for main + backup pages |

Scheduler: `~/Library/LaunchAgents/com.altr.reports.cycle.plist` → runs
`altr-reports-kit/lib/cycle.sh` on the 1st and 15th at 06:00.
(Separate job `com.altr.weekly-report` belongs to a different project, not this system.)

## Data flow

```
OnlyFans API ─┐
Telegram ─────┤                                   ┌─> Vercel (one site per model)
iMessage ─────┼─> WORK/<slug>-weekly/data/ ──> build ─> QA gates ─┤
WhatsApp PDFs ┤        + prose.py                 └─> Google Drive PDF
Social APIs ──┘
                                     cycle.sh wraps all of it, then Telegram-notifies Derrek
```

---

## Part 1: The report kit (`~/Documents/altr-reports-kit`)

The original kit is Antonio's; everything under `WORK/` and most of `lib/` was added for ALTR.

### Key files

- `WORK/liza-weekly/build_premium.py` — **the master template.** Every weekly report is this file
  with a different prose block. Liza's prose is inline (she has no `prose.py`); all other models
  have `WORK/<slug>-weekly/prose.py` holding only their narrative strings.
- `lib/make_builder.py <slug> <Name> <handle> <date> <pdf>` — stamps master + prose into a model's
  folder. Uses regex replace on `DATE`/`PDF` constants (count=1), not literal replace.
- `lib/premium.py` + `lib/*.css` — the whole design system (ink `#1d1d1b`, bone `#ebecdc`, mint
  `#b6f2e5`; Archivo + Spline Sans Mono). `check_braces` fails the build on any un-rendered
  `{M(...)}`-style helper call. Do not bypass it.
- `lib/pull_account.py`, `lib/analyze_ledger.py`, `lib/pull_threads.py`, `lib/analyze_threads.py`
  — OF data pull + analysis into `data/*.json`, `analysis.txt`, `threads.txt`.
- `lib/facts.py <slug> <of_user>` — prints every number a prose writer needs for one model.
- `lib/write_prose.py` — headless prose generation (`claude -p`) with validation: AST-parses the
  output, greps forbidden words, requires fan names to appear. Non-zero exit = do not publish.
- `lib/build.py` — renders `template.html` (web) and `print-template.html` → PDF via headless
  Chrome, runs the PDF QA scan. Must end `issues 0`.
- `lib/qa_mobile.py` — 390px viewport check; `docScrollWidth` must equal `vw`.
- `lib/deliver.py` — uploads the PDF to `gdrive:ALTR Reports/<Model>/<Name> - @handle - <date>.pdf`
  (rclone). Greps the builder for `NAME`, `HANDLE`, `DATE` constants. `sync()` creates Drive
  folders for any newly authenticated OF account.
- `lib/cycle.sh` — the full auto-publish: preflight (API key valid, credits, auth count) →
  refresh DMCA + social → per-model pull/analyze/prose/build/QA/deploy → Telegram notify.
- `lib/roster.txt` — `slug|acct_id|Name|of_username`, one line per recurring report (21 lines).
- `lib/holidays.py` — `next_occasion()` feeds the "shoot ahead" calendar card.
- `lib/translate_report.py` — Spanish editions. Extracts every visible text segment from a built
  report, translates in one `claude -p` call (numbers/names/handles validated unchanged), caches
  approved translations in the dest folder's `es-map.json` (only new segments cost a call), and
  auto-shortens segments that make the PDF overflow (`--shorten ... --log`). Naza's Spanish report
  (`WORK/naza-es-weekly`) builds this way from `naza-weekly` on every cycle; the pattern works for
  any model and any language by pointing it at a different folder and editing the prompt.
- `WORK/kels-review/` — one-off account-review (transition audit) format; good example of the
  report_skeleton evidence/what-changes structure. Not in the roster.

### Reuse notes

- To add a model: authenticate her on onlyfansapi.com, add a roster line, write `prose.py` (or let
  `write_prose.py` do it), run `make_builder`, build, deploy. `deliver.py sync` makes her Drive folder.
- The design system (`premium.py` + CSS) is fully separable: it only needs the builder to emit
  HTML through its helpers (`hero`, `ch`, `big`, `ichart`, `warn`, `qtable`, `PrintDoc`...).
- Web and PDF layouts are built separately in each builder (`H` list vs `doc.page(...)`). They
  share constants, never markup.

### Register rules (enforced, do not relax)

Creator-facing copy: plain language only. No analytics jargon ("bands", "lanes", "baseline"), no
soft verbs ("eased", "softer"), no metaphors, no internal words (whale/chatter/blast), no
"please", no em dashes, numbers inside the sentence ("Net income went down 28%, from X to Y").
The build greps for these and fails. Internal/team reports may use internal vocabulary.

### Money conventions

- Platform money is directional; **Infloww is the system of record** for payouts.
- All displayed figures are net (creator's 80% share); `GROSS = NET / 0.8` where shown.
- OnlyFans API credits cost real money — don't loop pulls carelessly.

## Part 2: Chat scanners (`~/Documents/altr-telegram`)

- `scan.py` — Telethon (MTProto, logged in as Derrek, **read-only**) exports model group chats and
  extracts open items (customs owed, requests). Quote negative chat ids: `--ids="-100..."`.
- iMessage: Gwen and Essence are on iMessage; the scanner reads `~/Library/Messages/chat.db`
  directly (Apple epoch is nanoseconds since 2001; message text may need `attributedBody` decode).
- `removelabs.py` — finds the newest DMCA "status" PDF in the WhatsApp Desktop local store
  (`ChatStorage.sqlite`, group "Derrek <> RemoveLabs"), parses it with pymupdf. The vendor changed
  the PDF format Oct 9, 2026 (added a DETECTED column); the parser handles both layouts.
  `OF_ALIASES` inside maps vendor names → OF usernames.
- `notify.py` — sends the cycle summary to Telegram **Saved Messages only** ("me"). It cannot
  message clients; keep it that way.
- `config.json` — Telegram api_id/api_hash, plus a read-only Postgres URL for the "What Is
  Working" CRM. **The CRM connection is unused by the pipeline** (it was schema reference only)
  and can be deleted.
- Guadalupe has no chat anywhere; her reports simply skip open items.

## Part 3: Social pipeline (`~/Documents/altr-social`)

- `altr_social.py pull|export|trials|status` — pulls per-page stats into SQLite
  (`altr-social.db`), exports template-shaped `social.json` per model.
- `accounts.json` — the roster: 22 models / 38 pages (instagram, tiktok, x, facebook; `farm: true`
  marks backup/promo pages). Add a page here and the next pull picks it up.
- Provider chain, in order: **HikerAPI → ScrapeCreators → Apify.** HikerAPI is required for
  18+-walled Instagram profiles (the others see nothing). All HikerAPI calls need a custom
  `User-Agent` header or Cloudflare blocks them (error 1010).
- Schema mirrors the What Is Working CRM semantics (accounts / posts / post_metrics /
  account_metrics, coalesce-on-save, baseline ratio = views ÷ 30-day average) so the numbers are
  comparable, but the data is all pulled locally.
- Report chapters auto-skip a page below threshold (<100 views, <100 likes, <50 followers gained)
  so farm pages with no traction don't produce absurd chapters.

## Credentials inventory (locations only — never commit values)

| Credential | Where it lives | Used for |
|---|---|---|
| OnlyFans API key | `altr-reports-kit/.mcp.json` | all OF data (credit-metered) |
| Telegram api_id / api_hash + session | `altr-telegram/config.json` + session file | chat scan, notify |
| HikerAPI key | `altr-social/config.json` | Instagram (18+ walled) |
| ScrapeCreators key | `altr-social/config.json` | IG/TikTok/X fallback |
| Apify token | `altr-social/config.json` | TikTok/X/Facebook scrapers |
| Google Drive OAuth | rclone remotes `gdrive:` / `gdrive-reports:` (`~/.config/rclone/rclone.conf`) | PDF delivery |
| Claude CLI session | `claude` login on this machine | report prose (`write_prose.py`); cycle aborts early if its usage credits run out |
| CRM Postgres URL (read-only) | `altr-telegram/config.json` | unused; safe to remove |

If you hand any project folder to someone, **strip these files first.** Rotate any key you share
by accident. OnlyFans account auth itself lives on onlyfansapi.com (deeplink flow,
`auth_type: "mobile_app"`), not on this machine.

## Known gotchas

- macOS has no `timeout`; zombie headless Chrome can hang `qa_mobile.py` — `pkill` and rerun.
- Two Pythons on this machine (Homebrew 3.14 vs CLT 3.9); packages are installed per-interpreter.
  The kit runs on `python3` = Homebrew 3.14.
- rclone uses the shared Google client_id, which Google retires during 2026. When Drive uploads
  start failing, create your own client_id (rclone.org/drive guide) — five-minute fix.
- The rclone remote uses `scope = drive.file`, so it can only see folders it created itself. When
  someone moves "ALTR Reports" inside a hand-made Drive folder, path lookups fail with "directory
  not found" even though nothing was deleted. Fixed Nov 3 2026 by adding remote `gdrive-reports:`
  pinned to `root_folder_id = 1Ki8KGyP2-r6UF19QdubqUAp5kLQN8Ehq`; delivery uses that remote and now
  survives moves and renames. The folder currently sits at
  ALTR Management / 04 Reporting & Analytics / ALTR Reports.
- Prose needs Claude CLI usage credits. When they run out, `claude -p` prints "You're out of usage
  credits" and every model fails at the prose step AFTER its OnlyFans pull is already paid for. The
  preflight now tests the CLI first and aborts before spending anything.
- The in-loop credit check must stay anchored (`insufficient credits|HTTP 402`). A bare grep for
  "402" once matched an unrelated account id inside an error listing and killed a whole run.
- `deliver.py` names files `Name - @handle - Date.pdf`. A one-off report on the same date will
  overwrite the weekly unless you upload it manually under a distinct name (see the Kells
  account review for the pattern).
- Vercel project names live in each `WORK/*/slug.txt`; `.vercel/` links the folder. The URL never
  changes across deploys.
- Preflight greps for API errors must not match substrings of account ids (an id containing "402"
  once false-positived an "out of credits" alert).

## Operating it

```bash
# one model, end to end
cd WORK/<slug>-weekly
python3 ../../lib/pull_account.py --days 7 --ledger-days 90
python3 ../../lib/analyze_ledger.py && python3 ../../lib/pull_threads.py && python3 ../../lib/analyze_threads.py
python3 build_premium.py && python3 ../../lib/build.py   # must end "issues 0"
python3 ../../lib/qa_mobile.py                            # docScrollWidth == 390
bash deploy.sh                                            # Vercel + Drive

# everything (what the schedule runs)
bash lib/cycle.sh
```

Review flow: cycle publishes → Derrek gets the Telegram summary → he reviews the links → only
then does anyone send a link to a model, manually, one at a time.
