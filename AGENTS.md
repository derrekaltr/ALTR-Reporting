# ALTR Reports Kit

You are working with Derrek, who runs ALTR Management (OnlyFans creator management). This folder turns live
OnlyFans data (through OnlyFansAPI.com) into ALTR-branded reports: creator-facing account reviews, whale and
top-fan reviews, weekly reports, chatting analyses. Each report is a private link (a scroll experience) with a
PDF reading edition behind a download button.

Read before producing anything:

- `CONTEXT/reports-and-data.md` (what the API gives us, every report type)
- `CONTEXT/brand-and-pdf.md` (how reports look, how they are built, the checks)

## How work happens

- **Questions** (who is connected, how did X do this week, top spenders, quiet whales, credit balance) are
  answered in chat. If the `onlyfans` MCP server is configured, use its tools; otherwise call the REST API
  through `lib/ofapi.py` (run `python3 lib/ofapi.py accounts` to list creators, or import `get`/`walk` from it
  in a short Python snippet). Never guess an account id; list accounts first. Keep chat lookups small
  (15 threads at most); anything bigger is a report.
- **Reports** follow the recipe below. Each report is a folder under `WORK/`, created by
  `python3 lib/new_report.py`. The scripts in `lib/` pull, analyse, build and check; the only file written per
  report is `build_premium.py` in that folder.
- **The reference for quality** is `examples/`: Lucé and Alanna for creator-facing, Yuni chatting analysis for
  internal, Vale top fans for an API-driven creator review. Open the PDF and the builder before writing.

## Rules

1. **Two registers.** Creator-facing: written to her, plain, no internal words (chatter, blast, whale), no asks
   of any kind, fans as they/them, nothing embarrassing. Internal: team language, asks for the model, compliance
   flags. Never mix; when one analysis serves both, build two documents.
2. **Platform money is directional.** For operations and coaching. Infloww is the financial record for splits.
   Footers say "platform-reported figures".
3. **The PDF is judged on typesetting.** No lone last words, no wrapped heading, no number split across lines,
   no text under 6pt, no collided cards, no half-empty page. `lib/build.py` fails on defects; then look at every
   render in `qa/` before publishing.
4. **The brand is fixed.** Ink, bone, mint, Archivo plus Spline Sans Mono, grain. No new colours or shadows.
   The design lives in `lib/`, never in a report.
5. **Writing.** No em dashes. No decorative emoji. Short sentences with the number in them. Headings in two
   halves, plain then mint, each under about 26 characters.
6. **Never send anything.** No mass messages, DMs, posts, list or promo changes unless Derrek asks for that
   exact action in that conversation.
7. **Credits are money.** Say the rough cost before a large pull (a report pull is roughly 40 to 150 credits,
   each fan thread 2 to 3; a 402 means the balance is at zero). Reuse `data/`; never re-pull what is on disk.
8. **Links are private.** Readable project name plus random tail, `noindex`, no raw data deployed.

## Making a report, pull to publish

Read both CONTEXT docs first. Open the matching example in `examples/` (PDF and builder) before writing.

1. **Confirm** creator, report type, audience (creator-facing or internal), window. Say the rough credit cost.
2. **Account**: list accounts (MCP `listAccounts` or `python3 lib/ofapi.py accounts`), copy the `acct_` id.
   If `is_authenticated` is false, stop and say so.
3. **Scaffold** from the kit root: `python3 lib/new_report.py <first-name>-<type> "<Creator name>"`.
4. **Pull**, inside `WORK/<slug>/`: `python3 ../../lib/pull_account.py <acct> --days 30 --ledger-days 90`
   (weekly: `--days 7 --ledger-days 21`; whales: `--days 30 --ledger-days 150`; chatting: `--days 30 --ledger-days 60`).
   Watch for `ERROR` lines; a 402 means credits are out.
5. **Analyse**: `python3 ../../lib/analyze_ledger.py` (whales: `--whale 500 --life 1000`). Read the printout.
   When fans are named: `python3 ../../lib/pull_threads.py` then `python3 ../../lib/analyze_threads.py`; it
   prints each thread's recent messages so quotes are exact.
6. **Write** `build_premium.py` in the folder (the skeleton is already there). Constants at the top, every
   number once, read from `data/cohort.json` and `data/threads_analysis.json` or typed in from a diagnostic.
   Web chapters with `ch() big() fig() story() ledger() spot() plan_step() closer()`; PDF pages with
   `doc.page() head() fnd() nums() warn() thread() qtable()`. Chapters come from what the data says; never pad.
   Every PDF page full. Register rules from CONTEXT apply word for word.
7. **Build**: `python3 build_premium.py && python3 ../../lib/build.py`. An AssertionError names the label, note,
   heading, em dash or placeholder to fix. The build must end with `issues 0`.
8. **Look**: open every `qa/q<N>a.png` and `q<N>b.png` and actually view the images. Then
   `python3 ../../lib/qa_mobile.py` and view `qa/m390-full.png`. Then the grep from CONTEXT quality step 4.
9. **Publish**: `./deploy.sh` (it rebuilds and refuses on defects). Confirm the URL and the PDF URL answer.
10. **Report back**: link, PDF path, page count, three quotable findings. If any step was skipped, say which.

If Derrek needs both a creator version and a team version of the same analysis, build two folders from the
same constants; the creator one never carries asks, compliance findings or thread-hygiene notes.

Lead with the finding. Short progress lines while scripts run. When a report is ready: link, PDF path, page
count, and the three findings Derrek would quote.
