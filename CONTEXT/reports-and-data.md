---
Last Updated: 2026-10-07
Status: Active
Owner: Antonio
Scope: Company
---

# Reports and data

## Purpose

What the OnlyFans API gives us, what we know about using it, and every report type ALTR makes from it.

## The API

- REST base `https://app.onlyfansapi.com/api`, header `Authorization: Bearer <key>`. Endpoint index written for
  an LLM: https://docs.onlyfansapi.com/llms.txt (about 350 endpoints).
- MCP endpoint `https://app.onlyfansapi.com/mcp/onlyfans-mcp`, same key, about 386 tools. MCP is for questions
  in conversation; the `lib/` scripts (REST) are for anything that becomes a report, because the raw JSON lands
  in `data/` and is reused. A key created without MCP scope works on REST but the MCP server answers an empty 403.
- Accounts are `acct_` plus 32 hex characters. `listAccounts` gives `onlyfans_username`, `display_name`,
  `is_authenticated`. An unauthenticated account needs the creator to re-authenticate from the console or the
  Auth+ iPhone app (three Face Auth attempts per 24 hours).
- Credits: list endpoints cost 1 credit per 20 results. A base pull is 40 to 150 credits, a thread 2 to 3.
  402 means zero balance; every script stops cleanly and resumes from disk on re-run. `getCreditUsage` is free.
- Cloudflare blocks Python's default user agent (error 1010, looks like a 403 key error). The client sends its own.

## Endpoints the reports use (under `/{acct}/`)

| Need | Endpoint | Notes |
|---|---|---|
| Profile, price, counts | `me` | |
| Earnings by type | `statistics/statements/earnings?start_date=YYYY-MM-DD HH:MM:SS&end_date&type=total|subscribes|tips|post|messages|stream` | |
| Profile visits | `statistics/reach/profile-visitors` | with topCountries |
| New subs | `subscribers/statistics?type=new` | |
| Ledger | `transactions?limit=100&startDate=YYYY-MM-DD` | paginate `_pagination.next_page`; `net` is to the creator, `amount` is what the fan paid; drop `status` undo / pending_return |
| Top fans | `fans/top?by=total` with or without dates | lifetime when no dates |
| Spenders, active / expired | `fans/active`, `fans/expired` + `filter[total_spent]=100` | `subscribedOnData.totalSumm` is lifetime. `fans/active` MISSES real top spenders: VIP lists come from the ledger |
| Mass messages | `engagement/messages/mass-messages` | needs both dates; sentCount, viewedCount, purchasedCount, price, rawText |
| Personal messages | `engagement/messages/direct-messages` | needs both dates; toUserId, price, purchasedCount; unsent ones have isCanceled |
| A thread | `chats/{fanId}/messages?limit=100&skip_users=all` | `isFromQueue` = blast, `fromUser.id == fanId` = the fan, `canPurchase` = PPV still unbought |
| Fans in bulk | `users/list?ids=1,2,3` | ten per call |
| Funnel | `tracking-links`, `free-trial-links` (+ stats, subscribers, spenders) | |

Known limits, to be stated not hidden: `isOpened` on messages is unreliable; the chat list order is meaningless
right after a blast; some long-time whale threads return no history before the latest blasts; `subscribedOnData`
can be stale for lapsed-and-returned fans.

## What `lib/` produces from that

`pull_account.py` writes the files above into `data/`. `analyze_ledger.py` turns them into `data/cohort.json`:
window vs previous (net, per day, by type, buyers, median ticket), daily series, revenue by hour and weekday,
every paying fan, and the cohort (window net 500 or lifetime 1,000 and up) with sessions, best night, max and
median ticket, days since last buy, subscription status, plus mass and DM stats (unlock rate by price band).
`pull_threads.py` and `analyze_threads.py` add `data/threads_analysis.json`: per fan, counts of fan / personal /
blast messages, unanswered hours, days since our last personal message, PPV sent and unbought, reply time, the
recent texts on both sides; and across fans, reply-time percentiles, the unanswered list and the quiet list.

## The report types

Two registers. **Creator-facing**: written to her, no asks, no internal words, fans they/them, examples that
show the opportunity rather than the previous team's misconduct. **Internal**: team language, asks for the model
for chatters to relay, compliance flags, thread hygiene.

| Report | Audience | What it answers | Window | Example |
|---|---|---|---|---|
| Account review / transition audit | Creator | Revenue shape (peak vs floor), the sending (blast volume, view rates, list not split), the script (recycled PPV line, mail-merge letters), the top three threads, the rest of the list with the notes on them, the funnel (links, visits to subs, costs never entered), what changes | 30 days, 90-day ledger | `luce-account-review` (two pages), `alanna-account-review` |
| Top-fan review | Creator | The biggest fan's story, the top 24 ledger, the fans who went quiet, the price ceiling, timing, a 30-day plan | 150-day ledger + whale threads | `vale-top-fans` |
| Whale report | Internal | The top-fan review plus unanswered hours, blast-only threads, renewals coming off, win-backs, chatter missteps, API caveats | same | (team cut of Vale) |
| Chatting analysis | Internal | Paid DMs per day, unlock rate by price band, resends, mass view rate, reply time, open customs, compliance (off-platform offers), revenue by hour, asks for the model; split before and after a handover | 30 days, 60-day ledger | `yuni-chatting-analysis` |
| Weekly report | Creator | This week vs last: net and gross, buyers, top five share, new fans, visits, mass open rate, best day, three fans to know, next week's plan | 7 days | rebuild from the skeleton |
| Chatter brief | Internal | Whales gone cold with their last words, identical blast text in whale threads, win-back pool with draft openers (nothing sent) | 7 days | rebuild from the skeleton |

Findings these have surfaced, so you know what to look for: a whale writing for ten hours with every message
unread; 89.6% of net from DMs with a Sunday floor; blasts every 45 to 60 minutes at under 1% viewed; unlock
rate flat across every price band (price is not the lever); customs sold as a closer and never delivered; a
chatter offering Zelle or Telegram; `fans/active` missing every real spender; two stale links carrying a whole
page; 80,961 visits to about 1% visit-to-sub.
