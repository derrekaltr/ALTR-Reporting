# ALTR Reports Kit

You are working with Derrek, who runs ALTR Management (OnlyFans creator management). This folder turns live
OnlyFans data (through OnlyFansAPI.com) into ALTR-branded reports: creator-facing account reviews, whale and
top-fan reviews, weekly reports, chatting analyses. Each report is a private link (a scroll experience) with a
PDF reading edition behind a download button.

Read before producing anything:

@CONTEXT/reports-and-data.md
@CONTEXT/brand-and-pdf.md

## How work happens

- **Questions** (who is connected, how did X do this week, top spenders, quiet whales, credit balance) are
  answered in chat with the `onlyfans` MCP tools. Start with `listAccounts`; never guess an account id. Keep
  chat lookups small (15 threads at most); anything bigger is a report.
- **Reports** follow the `make-report` skill. Each report is a folder under `WORK/`, created by
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
7. **Credits are money.** Say the rough cost before a large pull. Reuse `data/`; never re-pull what is on disk.
8. **Links are private.** Readable project name plus random tail, `noindex`, no raw data deployed.

Lead with the finding. Short progress lines while scripts run. When a report is ready: link, PDF path, page
count, and the three findings Derrek would quote.
