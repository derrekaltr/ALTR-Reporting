---
Last Updated: 2026-10-07
Status: Active
Owner: Antonio
Scope: Company
---

# Brand, link and PDF

## Purpose

How an ALTR report looks and reads, how the link and its PDF are produced, and the checks that keep the PDF
clean. The tokens are Derrek's (`BRAND-KIT/HANDOFF-TOTO-BRANDING.md` is the specification); the premium report
design on top of them is what every report uses, internal ones included. Reports never use the SOP template
in the brand kit.

## The brand in one breath

Ink `#1d1d1b` background always, never white. Raised `#242422`. Bone `#ebecdc` text. Mint `#b6f2e5` as a
highlighter only: the mint half of a heading, the hot bar in a chart, the one closing panel, under 10% of any
page, text on mint is ink. Hairlines `rgba(235,236,220,.14)`. Grain overlay. Archivo for everything readable
(light 200 to 300 weight for headings and numerals in reports), Spline Sans Mono uppercase with tracking for
every label, kicker, caption and running head. No new colours, no shadows, no gradients outside chart bars.

## The link

A scroll experience, not a document: full-viewport opening with the name revealed letter by letter, a hook in
two lines (the second mint), reading-progress bar, side chapter dots, reveal-on-scroll, count-up numerals,
charts whose bars grow in and answer hover with a readout line, fan story cards that expand, a sticky fan
spotlight that follows the ledger, a three-step plan, one mint close with a giant number and a signature.
Mobile-first: phone chart SVGs, tap-to-expand fan rows, inline download buttons, 11px floor, 36px tap targets.
All of this is in `lib/`; the builder only supplies content.

## The PDF

Its own layout, not a print of the site. A4 pages composed one at a time, each full. Cover: name, hook, three
numbers, a short letter, a "what we read" strip, contents. Page two: the short version (findings, three fans,
what changes). Evidence pages: a chart with a facts row under it, side-by-side threads, a fan table with spend
bars and notes, warn cards. Last page: the plan, what good looks like in 30 days, the mint close. Running head
with the chapter name; footer with a page-turn teaser and "03 / 10". Five to ten pages. A light page reads as
unfinished.

## Writing

Written to her (creator-facing) or to the team (internal), never mixed. Numbers in the sentence. Statement
headlines in two halves, plain then mint, each under 26 characters and on one line. No em dashes, no bold
lead-ins, no label-and-colon scaffolding, no decorative emoji. Whole dollars. Every chart captioned with the
mint element named. Creator-facing: no asks, no "we need from you", no tick boxes, no internal words.

## The pipeline

```
WORK/<slug>/build_premium.py   content + numbers -> template.html, print-template.html, report.json
python3 ../../lib/build.py     inlines the brand kit PNGs -> index.html, print.html
                               renders print.html with headless Chrome -> ALTR-<slug>-<date>.pdf
                               runs qa_pdf.py (exit 1 on defects), writes qa/q<N>a.png and q<N>b.png
./deploy.sh                    rebuilds, re-checks, vercel deploy --prod under the name in slug.txt
./takedown.sh                  link gone in seconds
```

The link is `https://<slug.txt>.vercel.app`; the PDF sits at `/<pdf name>` on the same host and the Download
button points to it (a pre-rendered file, never `window.print()`). `vercel.json` sets `noindex` and `no-store`;
`.vercelignore` keeps `data/`, `qa/`, the builder and templates off the host. One source for both editions:
the constants at the top of the builder feed the web chapters and the PDF pages, so they cannot disagree.

## The quality loop

After every build, in order. Stop at the first failure, fix the source, build again.

1. `qa_pdf.py` ends with `issues 0`. It flags a prose block ending on a single word, text under 6pt, text in
   the page margin, text past the sheet, and lists wrapped headings (the two-part chapter h2, chart axes and
   merged table cells are expected; everything else gets shortened). Fix copy, never shrink type.
2. Look at every render in `qa/` (top and bottom half of each page). You are looking for what a scanner cannot
   see: a hole in a page, cards touching, a chart too short for its card, a bar reading as a stripe, a running
   head naming the wrong chapter, a footer teaser pointing to the wrong page.
3. `qa_mobile.py` on the link: `docScrollWidth` equals the viewport, `over`, `clip` and `small` empty, no tap
   target under 36px. Read `qa/m390-full.png`.
4. Grep `print.html` and `index.html`: creator-facing must not contain "need from you", "would you",
   "please", "comfortable"; nothing may contain "hover any" in print or an em dash.
5. `./deploy.sh`, then open the live link on a real phone before anyone else sees it.

## The traps, each now a rule

| Went wrong | Rule |
|---|---|
| Headline ended on a lone word | Two halves under 26 characters each, `h2 em{display:block}`; shorten, never resize |
| A number wrapped | `white-space:nowrap` on every stat, caption, table figure (in the CSS) |
| Stat labels wrapped in a 4-up row | 28 characters max (36 in a 3-up); asserted at build |
| Table note cells wrapped | 40 characters max; assert in the builder |
| Cards overlapped on an over-full page | `.body > *{flex:0 0 auto}` plus a 4.5mm gap; over-full pages lose content, never squeeze |
| A page half empty | Fill it: a second chart, a facts row, a table; grow a chart viewBox rather than stretching rows |
| Mobile layout fired inside the PDF | A4 is about 794px; print CSS forces desktop grids |
| "Hover any bar" printed | Web-only words in `<span class="web">` |
| `{DROP}%` printed literally | Inner strings in an f-string block need their own `f`; asserted at build |
| Em dashes | Refused at build |
| 390px headless screenshots showed false overflow | Headless Chrome enforces about 500px; use `qa_mobile.py` |

One pull, one analysis, one writing pass, one or two build-and-look rounds. Not ten.
