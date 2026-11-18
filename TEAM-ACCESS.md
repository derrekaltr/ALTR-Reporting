# Giving a teammate full access to the ALTR reporting system

Written for whoever runs ALTR operations. The goal: they can change anything, any time,
without Derrek in the loop, and changes go live on the next scheduled run by themselves.

## What Derrek does once (about 15 minutes)

1. **Put the code on GitHub, privately.**
   ```bash
   cd ~/Documents/altr-reports-kit
   gh repo create altr-reports-kit --private --source=. --push
   gh repo add-collaborator altr-reports-kit <their-github-username> --permission push
   ```
   The repo carries no credentials. `.gitignore` excludes `.mcp.json`, `.env*`, `WORK/*/data/`
   and `.vercel`, and the history was scanned clean before the first push.

2. **Send them the credential files** over 1Password, or any private channel. Not email, not
   a group chat. These four files are everything:
   - `~/Documents/altr-reports-kit/.mcp.json` (OnlyFans API key)
   - `~/Documents/altr-social/config.json` (HikerAPI, ScrapeCreators, Apify)
   - `~/Documents/altr-telegram/config.json` (Telegram api_id / api_hash)
   - the rclone remote: `rclone config show gdrive-reports`

   Better where possible: give them their OWN keys instead of copies of Derrek's, at
   app.onlyfansapi.com/api-keys and each social provider. Then one person can be cut off
   without re-keying everything.

3. **Add them to Vercel**, team ALTR (`altr-022397ab`), so they can deploy and see builds.

4. **Confirm the Mac self-updates.** `lib/cycle.sh` now runs `git pull --ff-only` before each
   scheduled run, so whatever they merge is what runs on the 1st and 15th. Nothing else needed.

## What they can do from their own machine, immediately

- Change report wording, layout, charts, thresholds, the holiday list, the nurture trigger.
- Add or remove a model: edit `lib/roster.txt` and `~/Documents/altr-social/accounts.json`.
- Fix parsers and builders, add QA checks.
- Build and preview any report they have data for, and deploy it to its Vercel link.
- Run a full cycle themselves with `bash lib/cycle.sh` once credentials are in place.

Merging to `main` is all that is required for a change to take effect. The next scheduled run
picks it up, and Derrek's Telegram summary names the commit that shipped.

## The two things that only work on Derrek's Mac

These read local app storage and cannot move to another machine or the cloud:

- **Open items from Gwen and Essence** come from iMessage (`~/Library/Messages/chat.db`).
- **DMCA numbers** come from WhatsApp Desktop's local store.

A teammate's own cycle run produces reports without those two chapters. Derrek's scheduled run
has them. If that matters, the fix is to have Derrek's Mac export both to the shared Drive folder
and have the builders read from there; it is not built yet.

## The honest risk, stated once

Code access is indirect credential access: whatever they merge runs on Derrek's Mac with his
keys, his Telegram session and his iMessage database on the 1st and 15th. That is the intended
trade here, and the control is `git log` after the fact rather than approval before it. If that
ever stops being acceptable, remove the `git pull` block at the top of `lib/cycle.sh` and changes
go back to needing a manual update on the Mac.

## If something breaks

Read `HANDOFF.md` first; it maps every part of the system and lists the known traps.
The cycle writes its log to `~/Documents/altr-telegram/exports/launchd.out`, and every failure
names the model and the stage that failed.
