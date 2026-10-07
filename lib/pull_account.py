# -*- coding: utf-8 -*-
"""
Generic base pull for one creator account. Writes JSON into ./data/ in the current folder.

    python3 ../../lib/pull_account.py <account> [--days 30] [--ledger-days 90] [--chats] [--no-messages]

<account> is acct_..., the OF username, or a name fragment (resolved via listAccounts).

What lands in data/ (names are what analyze_ledger.py and the example builders expect):
  me.json                       profile + sub price + counts
  earn{D}_{type}.json           statements/earnings for total|subscribes|tips|post|messages|stream
  earn{2D}_total.json           the previous window for a like-for-like comparison
  visitors{D}.json              statistics/reach/profile-visitors (visits + topCountries)
  subs_new{D}.json              subscribers/statistics type=new
  transactions{L}.json          full ledger back L days (every sale, tip, sub; status + net + user)
  mass{D}.json                  every mass message in the window (sentCount, viewedCount, purchasedCount, price, rawText)
  direct{D}.json                every paid/unpaid personal DM sent in the window (toUserId, price, purchasedCount)
  fans_top{D}_total.json        fans/top for the window
  fans_topall_total.json        fans/top lifetime
  fans_active_spent100.json     active subscribers who spent >= $100 lifetime (paginated)
  fans_expired_spent100.json    expired fans who spent >= $100 lifetime (win-back pool)
  mass_overview.json, top_message.json
  chats.json                    (only with --chats) recent chat list; note: order=recent is useless right after blasts

Cost: roughly 40 to 120 credits for a normal account, mostly the ledger and the fan lists.
"""
import sys, os, argparse, datetime as dt, urllib.parse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ofapi import get, raw, walk, rows, save, find_account, BASE, FMT, DAY

ap = argparse.ArgumentParser()
ap.add_argument("account")
ap.add_argument("--days", type=int, default=30, help="analysis window (default 30)")
ap.add_argument("--ledger-days", type=int, default=90, help="how far back to pull the transaction ledger (default 90)")
ap.add_argument("--chats", action="store_true", help="also pull the chat list (10 per page, slow)")
ap.add_argument("--no-messages", action="store_true", help="skip mass + direct message pulls")
ap.add_argument("--now", help="freeze 'now' as YYYY-MM-DD (so a re-run reproduces the same window)")
a = ap.parse_args()

acc = find_account(a.account); ACCT = acc["id"]
print(f"account {ACCT} @{acc.get('onlyfans_username') or acc.get('username')}")
NOW = (dt.datetime.fromisoformat(a.now).replace(hour=23, minute=59) if a.now
       else dt.datetime.now(dt.timezone.utc).replace(tzinfo=None))
D = a.days; S = NOW - dt.timedelta(days=D); S2 = NOW - dt.timedelta(days=2 * D); L = NOW - dt.timedelta(days=a.ledger_days)
os.makedirs("data", exist_ok=True)
open("data/_window.json", "w").write(f'{{"account":"{ACCT}","now":"{FMT(NOW)}","days":{D},"ledger_days":{a.ledger_days}}}')

save("me", get(f"{ACCT}/me"))
for t in ["total", "subscribes", "tips", "post", "messages", "stream"]:
    save(f"earn{D}_{t}", get(f"{ACCT}/statistics/statements/earnings", start_date=FMT(S), end_date=FMT(NOW), type=t))
save(f"earn{2*D}_total", get(f"{ACCT}/statistics/statements/earnings", start_date=FMT(S2), end_date=FMT(NOW), type="total"))
save(f"earn{D}_prev_total", get(f"{ACCT}/statistics/statements/earnings", start_date=FMT(S2), end_date=FMT(S), type="total"))
save(f"visitors{D}", get(f"{ACCT}/statistics/reach/profile-visitors", start_date=FMT(S), end_date=FMT(NOW)))
save(f"subs_new{D}", get(f"{ACCT}/subscribers/statistics", start_date=FMT(S), end_date=FMT(NOW), type="new"))

tx, n = walk(f"{BASE}/{ACCT}/transactions?" + urllib.parse.urlencode({"limit": 100, "startDate": DAY(L)}), cap=400)
save(f"transactions{a.ledger_days}", tx); print(f"ledger: {len(tx)} transactions in {n} pages, oldest {tx[-1]['createdAt'][:10] if tx else None}")

if not a.no_messages:
    mm, n = walk(f"{BASE}/{ACCT}/engagement/messages/mass-messages?" + urllib.parse.urlencode({"limit": 100, "startDate": FMT(S), "endDate": FMT(NOW)}))
    save(f"mass{D}", mm); print(f"mass messages: {len(mm)}")
    dm, n = walk(f"{BASE}/{ACCT}/engagement/messages/direct-messages?" + urllib.parse.urlencode({"limit": 100, "startDate": FMT(S), "endDate": FMT(NOW)}), cap=600)
    save(f"direct{D}", dm); print(f"direct messages: {len(dm)}")

save(f"fans_top{D}_total", get(f"{ACCT}/fans/top", start_date=FMT(S), end_date=FMT(NOW), by="total"))
save("fans_topall_total", get(f"{ACCT}/fans/top", by="total"))
for name, path in (("fans_active_spent100", "fans/active"), ("fans_expired_spent100", "fans/expired")):
    out, off = [], 0
    while off < 800:
        r = get(f"{ACCT}/{path}", limit=20, offset=off, **{"filter[total_spent]": 100})
        if isinstance(r, dict) and "_error" in r: print(name, "error", r.get("_error"), str(r.get("_body"))[:120]); break
        items = rows(r); out += items
        more = (r.get("data") or {}).get("hasMore") if isinstance(r.get("data"), dict) else None
        if not items or more is False: break
        off += 20
    save(name, out)
save("mass_overview", get(f"{ACCT}/mass-messaging/overview"))
save("top_message", get(f"{ACCT}/engagement/messages/top-message"))

if a.chats:
    ch, off = [], 0
    while off <= 3000:
        r = get(f"{ACCT}/chats", limit=100, offset=off, order="recent")
        if isinstance(r, dict) and "_error" in r: print("chats error", r); break
        b = rows(r); ch += b
        if len(b) < 10: break
        off += len(b)
    save("chats", ch)
print("done. next: python3 ../../lib/analyze_ledger.py")
