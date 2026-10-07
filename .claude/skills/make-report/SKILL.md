---
name: make-report
description: Make any ALTR report from live OnlyFans data (account review, top-fan or whale report, weekly, chatting analysis, chatter brief) as a link plus PDF: scaffold, pull, analyse, write, build, check, publish. Use whenever Derrek asks for a report, review, audit, analysis or brief on a creator.
---

# Make a report

Read CONTEXT/reports-and-data.md (which report, which data) and CONTEXT/brand-and-pdf.md (how it looks, the
checks) first. Open the matching example in `examples/` (PDF and builder) before writing.

1. **Confirm** creator, report type, audience (creator-facing or internal), window. Say the rough credit cost.
2. **Account**: `listAccounts`, copy the `acct_` id. If `is_authenticated` is false, stop and say so.
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
8. **Look**: open every `qa/q<N>a.png` and `q<N>b.png` with the Read tool. Then `python3 ../../lib/qa_mobile.py`
   and read `qa/m390-full.png`. Then the grep from CONTEXT step 4.
9. **Publish**: `./deploy.sh` (it rebuilds and refuses on defects). Confirm the URL and the PDF URL answer.
10. **Report back**: link, PDF path, page count, three quotable findings. If any step was skipped, say which.

If Derrek needs both a creator version and a team version of the same analysis, build two folders from the
same constants; the creator one never carries asks, compliance findings or thread-hygiene notes.
