# Running this kit with GPT (OpenAI) instead of Claude

The engine in `lib/` is plain Python and does not care which model drives it. What a GPT needs is the same
thing Claude gets: a way to run the scripts in this folder, and the instructions. Both are set up below.
Nothing here removes the Claude setup; `CLAUDE.md` and `.claude/` stay, so the kit works in Conductor too.

## 0. One-time kit setup (same as START-HERE.md, model-independent)

1. Keep the kit at `~/Documents/altr-reports-kit`.
2. Create an API key at https://app.onlyfansapi.com/api-keys (MCP access optional for GPT; see step 3).
3. `cd ~/Documents/altr-reports-kit && bash setup.sh` — installs the two Python packages, stores the key in
   `.mcp.json` (the REST client `lib/ofapi.py` reads it from there too), and lists your connected creators.
4. Google Chrome installed (renders the PDFs). For publishing: `npm i -g vercel && vercel login`.

Sanity check at any time: `python3 lib/ofapi.py accounts` must print your creators.

## 1. Install the GPT agent: OpenAI Codex CLI

Codex CLI is OpenAI's equivalent of Claude Code: a GPT-driven agent that reads files and runs commands in a
folder on your machine.

```
npm i -g @openai/codex
cd ~/Documents/altr-reports-kit
codex
```

Sign in with your ChatGPT account when it asks (or set `OPENAI_API_KEY`). Codex automatically reads
`AGENTS.md` in this folder — that file carries all of Antonio's rules plus the full pull-to-publish recipe,
so no further prompting setup is needed. Approve its requests to run the `lib/` scripts when it asks.

## 2. Warm prompts

The same lines from START-HERE.md work as-is, typed into Codex:

```
Which creators are connected to the OnlyFans API?
How did @alannasworldx do this week against last?
Who are Yuni's top 15 spenders over 90 days, and which ones have not had a personal message in 10 days?
Build a creator-facing account review for Sarah Lloyd, last 30 days, link and PDF.
Whale report for Vale, team-facing, last 90 days.
30-day chatting analysis for Jane Ford, internal.
```

The first three answer in chat (through `lib/ofapi.py`); the rest run the full pipeline: pull, analyse,
write, build, QA, publish.

## 3. MCP under Codex (optional)

GPT does not need MCP here: quick questions go through `lib/ofapi.py` (REST), and reports always use the
`lib/` scripts anyway. If you still want the OnlyFans MCP tools inside Codex, add to `~/.codex/config.toml`
the stdio bridge (works on every Codex version):

```toml
[mcp_servers.onlyfans]
command = "npx"
args = ["-y", "mcp-remote", "https://app.onlyfansapi.com/mcp/onlyfans-mcp",
        "--header", "Authorization: Bearer YOUR-ONLYFANSAPI-KEY"]
```

Newer Codex builds also accept the HTTP server directly (`url = "https://app.onlyfansapi.com/mcp/onlyfans-mcp"`
with a bearer token); if yours does not, use the bridge above or skip MCP entirely. Remember the key must
have MCP access enabled, or the MCP server answers an empty 403 while REST keeps working.

## 4. Questions from your phone (optional)

For who-is-connected / how-did-X-do questions away from the Mac, build a Custom GPT in ChatGPT:

1. ChatGPT -> Explore GPTs -> Create. Name it "ALTR Reports Q&A".
2. Instructions: paste `CONTEXT/reports-and-data.md`, then add: "Answer questions about ALTR creators using
   the API. Platform figures are directional; Infloww is the financial record. Never send messages, mass
   messages or posts of any kind. List accounts first; never guess an account id. Keep pulls small; list
   endpoints cost 1 credit per 20 results."
3. Add an Action: import `gpt-action/openapi.yaml` from this kit, auth type API Key -> Bearer, paste your
   OnlyFansAPI key.

This path is Q&A only. Report builds need Chrome, the `lib/` scripts and Vercel, so they stay on the Mac
with Codex (or Claude).

## What lives where

| | |
|---|---|
| `AGENTS.md` | The rules + recipe Codex reads automatically (GPT twin of `CLAUDE.md` + the make-report skill). |
| `GPT-SETUP.md` | This file. |
| `gpt-action/openapi.yaml` | Trimmed read-only API schema for a Custom GPT Action. |
| Everything else | Unchanged from Antonio's kit; see START-HERE.md. |
