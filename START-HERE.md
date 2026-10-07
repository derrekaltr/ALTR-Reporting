# Start here, Derrek

This folder is the ALTR report system: your OnlyFans API key in, on-brand reports out. The same ones Antonio
has been making (Alanna and Lucé account reviews, Yuni's chatting analysis, Vale's top-fan review), as a private
link with a PDF behind a download button.

## Setup, about ten minutes

1. Unzip to `~/Documents/altr-reports-kit` and keep it there. Reports you make will live inside it.
2. Create an API key at https://app.onlyfansapi.com/api-keys with MCP access enabled.
3. In Terminal:
   ```
   cd ~/Documents/altr-reports-kit
   bash setup.sh
   ```
   It checks for Python 3 and Chrome, installs two Python packages, asks for the key, writes it into `.mcp.json`
   (stays on your machine, git-ignored), makes the folder a git repo so Conductor accepts it, and lists the
   creators connected to your API account. If that list prints, setup worked.
4. Open the folder in Conductor as a workspace. The first time, Claude asks to trust the `onlyfans` MCP server.
   Say yes. That gives it the OnlyFans tools: accounts, earnings, fans, chats, mass messages, links.
5. For publishing links (later is fine): `npm i -g vercel` then `vercel login`.

If Conductor does not pick up `.mcp.json`, add the server once at user level:
```
claude mcp add --transport http onlyfans https://app.onlyfansapi.com/mcp/onlyfans-mcp --header "Authorization: Bearer YOUR-KEY"
```

## Things to type

```
Which creators are connected to the OnlyFans API?
How did @alannasworldx do this week against last?
Who are Yuni's top 15 spenders over 90 days, and which ones have not had a personal message in 10 days?
Build a creator-facing account review for Sarah Lloyd, last 30 days, link and PDF.
Whale report for Vale, team-facing, last 90 days.
30-day chatting analysis for Jane Ford, internal.
```

The first three answer in chat. The rest pull the data into a folder, write the report, build the link and the
PDF, run the typesetting checks, show the page renders, and publish only when clean.

## Two things to know

**Money.** API figures are platform-reported and directional: for operating decisions and creator conversations,
not for splits or settlements. Infloww stays the financial record. Every report says so in the footer.

**Credits.** A report pull costs roughly 40 to 150 credits; each fan thread 2 to 3. A 402 error means the balance
is at zero. "What is my credit balance" is a free question.

## What is in the folder

| | |
|---|---|
| `CLAUDE.md` | The rules Claude works by. |
| `CONTEXT/reports-and-data.md` | What the API gives us and every report type we make from it. |
| `CONTEXT/brand-and-pdf.md` | How reports look, how the link and PDF get built, the quality checks. |
| `.claude/skills/make-report` | The one recipe, pull to publish. |
| `lib/` | The engine. API client, pulls, analysis, the design system, builder, checks, deploy. |
| `BRAND-KIT/` | Your brand kit, unchanged. |
| `examples/` | Four finished reports, each as its builder script plus the PDF. The reference for what good looks like. |
| `WORK/` | New reports go here, one folder each. |

To tweak the look: `lib/creator_base.css` (web), `lib/print_base.css` (PDF), and `lib/premium.py`. Change it
there once and every report follows.
