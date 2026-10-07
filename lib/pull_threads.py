# -*- coding: utf-8 -*-
"""
Pull full conversation threads (up to 200 latest messages) plus user details for a set of fans.

    python3 ../../lib/pull_threads.py                 # fans from data/cohort.json (analyze_ledger output)
    python3 ../../lib/pull_threads.py 123 456 789     # explicit fan ids
    python3 ../../lib/pull_threads.py --min-net 250 --min-life 2000 --top 40

Writes data/users.json and data/threads/<fanId>.json. Skips threads already on disk, so a
re-run after a credit top-up only fetches what is missing. Two calls per thread plus one
users/list call per ten fans; budget about 2 to 3 credits per fan.
"""
import sys, os, json, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ofapi import get, rows, save

ap = argparse.ArgumentParser()
ap.add_argument("ids", nargs="*", type=int)
ap.add_argument("--min-net", type=float, default=250, help="window net spend threshold from cohort.json")
ap.add_argument("--min-life", type=float, default=2000, help="lifetime spend threshold from cohort.json")
ap.add_argument("--top", type=int, default=60, help="hard cap on number of threads")
ap.add_argument("--account", help="acct_... (default: data/_window.json)")
a = ap.parse_args()

ACCT = a.account or json.load(open("data/_window.json"))["account"]
ids = list(a.ids)
if not ids:
    co = json.load(open("data/cohort.json", encoding="utf-8"))["cohort"]
    ids = [w["id"] for w in co if w.get("net", 0) >= a.min_net or (w.get("life") or 0) >= a.min_life][:a.top]
print(f"threads to pull: {len(ids)}"); sys.stdout.flush()

users = json.load(open("data/users.json", encoding="utf-8")) if os.path.exists("data/users.json") else {}
need = [i for i in ids if str(i) not in users]
for i in range(0, len(need), 10):
    r = get(f"{ACCT}/users/list", ids=",".join(str(x) for x in need[i:i + 10]))
    d = r.get("data") if isinstance(r, dict) else None
    items = d if isinstance(d, list) else (list(d.values()) if isinstance(d, dict) else [])
    for u in items:
        if isinstance(u, dict) and u.get("id"): users[str(u["id"])] = u
save("users", users)

os.makedirs("data/threads", exist_ok=True)
done = 0
for k in ids:
    path = f"data/threads/{k}.json"
    if os.path.exists(path): continue
    msgs = rows(get(f"{ACCT}/chats/{k}/messages", limit=100, skip_users="all"))
    if len(msgs) == 100:
        oldest = min(msgs, key=lambda m: m["createdAt"])
        more = rows(get(f"{ACCT}/chats/{k}/messages", limit=100, skip_users="all", first_id=oldest["id"]))
        seen = {m["id"] for m in msgs}; msgs += [m for m in more if m["id"] not in seen]
    json.dump(msgs, open(path, "w", encoding="utf-8"), ensure_ascii=False)
    done += 1
    if done % 10 == 0: print(f"  {done} threads"); sys.stdout.flush()
print(f"threads on disk: {len(os.listdir('data/threads'))}. next: python3 ../../lib/analyze_threads.py")
