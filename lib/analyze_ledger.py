# -*- coding: utf-8 -*-
"""
Ledger analysis for one account, from the files pull_account.py wrote into ./data/.

    python3 ../../lib/analyze_ledger.py [--whale 500] [--life 1000] [--tz -4]

Output: data/cohort.json
  summary   totals for the window and the ledger, buyer counts, undo/refund count
  period    window vs previous window: net, per day, by type, buyers, median ticket
  daily     net per day by type (for charts)
  hour_rev  revenue by hour of day in the chosen timezone (default US Eastern, -4)
  dow_rev   revenue by weekday
  cohort    the fans worth writing about: window net >= --whale OR lifetime >= --life, each with
            net by sub-window, sessions (90-minute gaps), best session, max/median ticket,
            top hours and weekdays, days since last buy, subscription status from the fan lists
  fans      every paying fan in the ledger with the same per-fan numbers (lighter)
  mass / dm message stats for the window when mass{D}.json / direct{D}.json exist

Everything downstream (threads, builders) reads this file. Re-run after any new pull.
Money is NET to the creator unless a key says gross. Platform figures are directional:
Infloww (or the agency's own statement) stays the financial record for splits and settlements.
"""
import json, collections, datetime as dt, re, os, glob, argparse, statistics as st

ap = argparse.ArgumentParser()
ap.add_argument("--whale", type=float, default=500, help="window net that makes a fan part of the cohort")
ap.add_argument("--life", type=float, default=1000, help="lifetime spend that makes a fan part of the cohort")
ap.add_argument("--tz", type=float, default=-4, help="hours offset from UTC for hour/weekday stats (US Eastern summer = -4)")
a = ap.parse_args()

L = lambda n: json.load(open(f"data/{n}.json", encoding="utf-8"))
def rows(d):
    if isinstance(d, list): return d
    x = d.get("data", d) if isinstance(d, dict) else []
    if isinstance(x, list): return x
    if isinstance(x, dict):
        for k in ("list", "items", "users", "data"):
            if isinstance(x.get(k), list): return x[k]
    return []

W = L("_window"); D = W["days"]; LD = W["ledger_days"]
NOW = dt.datetime.fromisoformat(W["now"]).replace(tzinfo=dt.timezone.utc)
TZ = dt.timezone(dt.timedelta(hours=a.tz))
def ts(s): return dt.datetime.fromisoformat(s)
def age(t): return (NOW - ts(t["createdAt"])).total_seconds() / 86400
ledger_file = sorted(glob.glob("data/transactions*.json"))[-1]
allx = json.load(open(ledger_file, encoding="utf-8"))
tx = [t for t in allx if t.get("status") not in ("undo", "pending_return")]
undo = [t for t in allx if t.get("status") in ("undo", "pending_return")]

def blank(k, u):
    return {"id": k, "name": re.sub(r"\s+", " ", (u.get("name") or "")).strip(), "user": u.get("username") or "",
            "net": 0, "net_w": 0, "net_prev": 0, "net_older": 0, "net7": 0, "msg": 0, "tip": 0, "sub": 0,
            "n": 0, "n_msg": 0, "n_tip": 0, "tickets": [], "times": []}
fans = {}
per = {"w": collections.Counter(), "p": collections.Counter()}; buyers = {"w": set(), "p": set()}
daily = collections.defaultdict(collections.Counter); hour_rev = collections.Counter(); dow_rev = collections.Counter()
tickets_w, tickets_p = [], []
for t in tx:
    u = t.get("user") or {}; k = u.get("id")
    if k is None: continue
    f = fans.setdefault(k, blank(k, u))
    ag = age(t); n = float(t.get("net") or 0); amt = float(t.get("amount") or 0); ty = t.get("type") or ""
    f["net"] += n; f["n"] += 1
    if ag < 7: f["net7"] += n
    if ag < D: f["net_w"] += n
    elif ag < 2 * D: f["net_prev"] += n
    else: f["net_older"] += n
    if ty == "message": f["msg"] += n; f["n_msg"] += 1; f["tickets"].append(amt)
    elif ty == "tip": f["tip"] += n; f["n_tip"] += 1; f["tickets"].append(amt)
    else: f["sub"] += n
    if ty in ("message", "tip"): f["times"].append((t["createdAt"], amt, ty))
    p = "w" if ag < D else ("p" if ag < 2 * D else None)
    if p:
        per[p]["net"] += n; per[p][ty] += n; per[p]["n_" + ty] += 1
        if ty in ("message", "tip"):
            buyers[p].add(k); (tickets_w if p == "w" else tickets_p).append(amt)
    if ag < D:
        d = ts(t["createdAt"]).astimezone(TZ)
        daily[d.strftime("%Y-%m-%d")][ty] += n; daily[d.strftime("%Y-%m-%d")]["net"] += n
        if ty in ("message", "tip"): hour_rev[d.hour] += n; dow_rev[d.strftime("%a")] += n

# lifetime + subscription status from the fan lists
life = {}
def take(x, active_default):
    s = x.get("subscribedOnData") or {}
    return {"life": float(s.get("totalSumm") or 0), "life_msg": float(s.get("messagesSumm") or 0),
            "life_tip": float(s.get("tipsSumm") or 0), "duration": s.get("duration"),
            "sub_active": (bool(x.get("subscribedOn")) if "subscribedOn" in x else active_default) and not x.get("subscribedOnExpiredNow"),
            "expiredAt": s.get("expiredAt"), "renewedAt": s.get("renewedAt"), "subscribeAt": s.get("subscribeAt"),
            "lastSeen": x.get("lastSeen"), "name_l": x.get("name"), "user_l": x.get("username"), "price": s.get("price")}
for src, active in (("fans_active_spent100", True), ("fans_expired_spent100", False)):
    if os.path.exists(f"data/{src}.json"):
        for x in rows(L(src)): life[x["id"]] = take(x, active)
if os.path.exists("data/fans_topall_total.json"):
    for x in rows(L("fans_topall_total")): life.setdefault(x["id"], {}).update(take(x, False))

def sessions(times, gap_min=90):
    ev = sorted(times); out, cur = [], []
    for e in ev:
        if cur and (ts(e[0]) - ts(cur[-1][0])).total_seconds() > gap_min * 60: out.append(cur); cur = []
        cur.append(e)
    if cur: out.append(cur)
    return [{"start": s[0][0], "end": s[-1][0], "n": len(s), "gross": round(sum(x[1] for x in s), 2),
             "tickets": [x[1] for x in s], "tips": sum(1 for x in s if x[2] == "tip")} for s in out]

def enrich(f):
    f = dict(f); f.update(life.get(f["id"], {}))
    if not f.get("name"): f["name"] = f.get("name_l") or f.get("user") or f"u{f['id']}"
    if not f.get("user"): f["user"] = f.get("user_l") or f"u{f['id']}"
    last = max((x[0] for x in f["times"]), default=None); first = min((x[0] for x in f["times"]), default=None)
    f["last_buy"], f["first_buy"] = last, first
    f["days_since_buy"] = round((NOW - ts(last)).total_seconds() / 86400, 1) if last else None
    ss = sessions(f["times"]); f["sessions"] = ss; f["n_sessions"] = len(ss)
    f["best_session"] = max(ss, key=lambda s: s["gross"]) if ss else None
    tk = sorted(f["tickets"]); f["max_ticket"] = tk[-1] if tk else 0; f["median_ticket"] = tk[len(tk) // 2] if tk else 0
    f["top_hours"] = collections.Counter(ts(x[0]).astimezone(TZ).hour for x in f["times"]).most_common(3)
    f["top_dows"] = collections.Counter(ts(x[0]).astimezone(TZ).strftime("%a") for x in f["times"]).most_common(3)
    for k in ("net", "net_w", "net_prev", "net_older", "net7", "msg", "tip", "sub"): f[k] = round(f[k], 2)
    del f["times"]; del f["tickets"]
    return f

ids = set(k for k, f in fans.items() if f["net_w"] >= a.whale or f["net"] >= a.whale * 2) | set(k for k, l in life.items() if l.get("life", 0) >= a.life)
cohort = sorted((enrich(fans.get(k) or blank(k, {"name": life[k].get("name_l"), "username": life[k].get("user_l")})) for k in ids),
                key=lambda f: -(f["net_w"] * 2 + f["net"]))
fan_rows = sorted((enrich(f) for f in fans.values()), key=lambda f: -f["net_w"])
for f in fan_rows: f.pop("sessions", None)

def pstats(p, tk):
    c = per[p]; days = D
    return {"days": days, "net": round(c["net"]), "net_day": round(c["net"] / days), "msg": round(c["message"]), "tips": round(c["tip"]),
            "subs": round(c["new_subscription"] + c["recurring_subscription"]), "n_msg": c["n_message"], "n_tip": c["n_tip"],
            "n_new_subs": c["n_new_subscription"], "n_rebills": c["n_recurring_subscription"],
            "buyers": len(buyers[p]), "median_ticket": st.median(tk) if tk else 0, "avg_ticket": round(st.mean(tk), 2) if tk else 0}
R = {"account": W["account"], "now": W["now"], "days": D, "ledger_days": LD, "tz": a.tz,
     "summary": {"ledger_net": round(sum(f["net"] for f in fans.values())), "window_net": round(per["w"]["net"]), "prev_net": round(per["p"]["net"]),
                 "change_pct": round((per["w"]["net"] - per["p"]["net"]) / per["p"]["net"] * 100, 1) if per["p"]["net"] else None,
                 "paying_fans_ledger": len(fans), "paying_fans_window": len(buyers["w"]),
                 "undo_n": len(undo), "undo_net": round(sum(float(t.get("net") or 0) for t in undo)),
                 "cohort_n": len(cohort), "cohort_net_window": round(sum(f["net_w"] for f in cohort)), "cohort_net_ledger": round(sum(f["net"] for f in cohort)),
                 "top10_share_window": round(sum(f["net_w"] for f in fan_rows[:10]) / per["w"]["net"] * 100, 1) if per["w"]["net"] else 0},
     "period": {"window": pstats("w", tickets_w), "previous": pstats("p", tickets_p)},
     "daily": {k: {kk: round(vv) for kk, vv in v.items()} for k, v in sorted(daily.items())},
     "hour_rev": {h: round(hour_rev[h]) for h in range(24)}, "dow_rev": {d: round(dow_rev[d]) for d in ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]},
     "cohort": cohort, "fans": fan_rows}

# optional: message stats
def pr(x): return float(x.get("price") or 0)
if os.path.exists(f"data/mass{D}.json"):
    mm = L(f"mass{D}"); paid = [m for m in mm if pr(m) > 0]; sent = sum(m.get("sentCount") or 0 for m in mm); views = sum(m.get("viewedCount") or 0 for m in mm)
    R["mass"] = {"n": len(mm), "per_day": round(len(mm) / D, 1), "paid": len(paid), "sends": sent, "views": views,
                 "view_rate": round(views / sent * 100, 2) if sent else 0, "purchases": sum(m.get("purchasedCount") or 0 for m in paid),
                 "gross": round(sum(pr(m) * (m.get("purchasedCount") or 0) for m in paid)),
                 "best": sorted(({"date": m.get("date", "")[:16], "price": pr(m), "purch": m.get("purchasedCount") or 0, "views": m.get("viewedCount") or 0,
                                   "sent": m.get("sentCount") or 0, "text": re.sub(r"\s+", " ", m.get("rawText") or "")[:120]} for m in mm),
                                 key=lambda m: -(m["price"] * m["purch"]))[:10]}
if os.path.exists(f"data/direct{D}.json"):
    dma = L(f"direct{D}"); dm = [x for x in dma if not x.get("isCanceled") and "toUserId" in x]; bought = [x for x in dm if x.get("purchasedCount")]
    bands = [(0, 20), (20, 40), (40, 70), (70, 100), (100, 150), (150, 10 ** 6)]
    def band(lo, hi):
        xs = [x for x in dm if lo <= pr(x) < hi]; b = [x for x in xs if x.get("purchasedCount")]
        return {"band": f"${lo} to {hi - 1}" if hi < 10 ** 6 else f"${lo}+", "sent": len(xs), "bought": len(b), "rate": round(len(b) / len(xs) * 100, 1) if xs else 0, "gross": round(sum(pr(x) for x in b))}
    R["dm"] = {"sent": len(dm), "per_day": round(len(dm) / D, 1), "bought": len(bought), "rate": round(len(bought) / len(dm) * 100, 1) if dm else 0,
               "gross": round(sum(pr(x) for x in bought)), "median_price": st.median([pr(x) for x in dm]) if dm else 0,
               "fans_reached": len({x["toUserId"] for x in dm}), "unsent": len(dma) - len(dm), "bands": [band(lo, hi) for lo, hi in bands],
               "hour_sent": dict(collections.Counter(dt.datetime.fromisoformat(x["date"]).astimezone(TZ).hour for x in dm if x.get("date")))}

json.dump(R, open("data/cohort.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
print(json.dumps(R["summary"], indent=1)); print("window", R["period"]["window"]); print("previous", R["period"]["previous"])
if "mass" in R: print("mass", {k: v for k, v in R["mass"].items() if k != "best"})
if "dm" in R: print("dm", {k: v for k, v in R["dm"].items() if k not in ("bands", "hour_sent")})
print(f"\ncohort ({len(cohort)}):")
for f in cohort[:40]:
    print(f'{f["id"]:>10} {f["name"][:18]:18} life={f.get("life", 0):>7.0f} ledger={f["net"]:>6.0f} win={f["net_w"]:>5.0f} prev={f["net_prev"]:>5.0f} '
          f'last={f["days_since_buy"]}d sub={f.get("sub_active")} max={f["max_ticket"]} sess={f["n_sessions"]}')
print("\nwritten data/cohort.json. next: python3 ../../lib/pull_threads.py (then analyze_threads.py)")
