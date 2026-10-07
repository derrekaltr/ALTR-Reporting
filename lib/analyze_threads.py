# -*- coding: utf-8 -*-
"""
Thread analysis for every data/threads/<fanId>.json. Output: data/threads_analysis.json

Per fan: message counts (fan / personal / blast), whether the fan's last message is unanswered and
for how many hours, days since our last personal message, PPV sent vs still unbought, median reply
time in minutes, the trailing run of blasts at the end of the thread, and the recent texts on both
sides so a writer can quote accurately. The summary block has reply-time percentiles across all
threads and the list of fans left unanswered, biggest first.

Known data limits (do not "fix" these in the report, state them):
  isOpened on messages is unreliable (a handful of true values on hundreds of personal messages).
  Chat list order=recent is meaningless right after a mass send: every chat shows the blast time.
  Some long-time whales show no history before the most recent blasts; the API returned nothing older.
"""
import json, glob, os, re, datetime as dt, statistics as st

W = json.load(open("data/_window.json")); NOW = dt.datetime.fromisoformat(W["now"]).replace(tzinfo=dt.timezone.utc)
co = {w["id"]: w for w in json.load(open("data/cohort.json", encoding="utf-8"))["cohort"]}
users = json.load(open("data/users.json", encoding="utf-8")) if os.path.exists("data/users.json") else {}
def ts(s): return dt.datetime.fromisoformat(s)
def days(s): return round((NOW - ts(s)).total_seconds() / 86400, 1)
def clean(s): return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s or "")).strip()

out, all_rt = {}, []
for f in glob.glob("data/threads/*.json"):
    k = int(os.path.basename(f)[:-5]); d = json.load(open(f, encoding="utf-8"))
    rows = d if isinstance(d, list) else (d.get("data", {}).get("list") if isinstance(d.get("data"), dict) else d.get("data")) or []
    if isinstance(d, dict) and "_error" in d: out[k] = {"error": d["_error"]}; continue
    rows = sorted(rows, key=lambda m: m["createdAt"])
    fan = [m for m in rows if (m.get("fromUser") or {}).get("id") == k]
    mine = [m for m in rows if m not in fan]
    blasts = [m for m in mine if m.get("isFromQueue")]
    personal = [m for m in mine if not m.get("isFromQueue")]
    ppv = [m for m in mine if (m.get("price") or 0) > 0]
    last = rows[-1] if rows else None; last_fan = fan[-1] if fan else None; last_personal = personal[-1] if personal else None
    trail = 0
    for m in reversed(rows):
        if m in blasts: trail += 1
        else: break
    unanswered = bool(last_fan and (not last_personal or last_fan["createdAt"] > last_personal["createdAt"]))
    rts = []
    for i, m in enumerate(rows):
        if m in fan and (i == 0 or rows[i - 1] not in fan):
            nxt = next((x for x in rows[i + 1:] if x in personal), None)
            if nxt: rts.append((ts(nxt["createdAt"]) - ts(m["createdAt"])).total_seconds() / 60)
    rts.sort(); all_rt += rts
    u = users.get(str(k)) or {}
    out[k] = {"name": (co.get(k) or {}).get("name") or clean(u.get("name")), "user": (co.get(k) or {}).get("user") or u.get("username"),
              "n": len(rows), "span_from": rows[0]["createdAt"] if rows else None,
              "n_fan": len(fan), "n_personal": len(personal), "n_blast": len(blasts),
              "ppv_sent": len(ppv), "ppv_prices": [m["price"] for m in ppv], "ppv_unbought": sum(1 for m in ppv if m.get("canPurchase")),
              "last_at": last["createdAt"] if last else None, "last_by": ("fan" if last in fan else ("blast" if last in blasts else "us")) if last else None,
              "trail_blasts": trail, "last_fan_at": last_fan["createdAt"] if last_fan else None, "days_since_fan": days(last_fan["createdAt"]) if last_fan else None,
              "last_personal_at": last_personal["createdAt"] if last_personal else None, "days_since_personal": days(last_personal["createdAt"]) if last_personal else None,
              "unanswered": unanswered, "unanswered_hours": round((NOW - ts(last_fan["createdAt"])).total_seconds() / 3600, 1) if unanswered else 0,
              "med_rt_min": round(rts[len(rts) // 2]) if rts else None, "rt_within_15": round(sum(1 for r in rts if r <= 15) / len(rts) * 100) if rts else None,
              "last_fan_text": clean(last_fan.get("text"))[:220] if last_fan else "", "last_personal_text": clean(last_personal.get("text"))[:220] if last_personal else "",
              "last_blast_text": clean(blasts[-1].get("text"))[:120] if blasts else "",
              "fan_recent": [(m["createdAt"][:16], clean(m.get("text"))[:200]) for m in fan[-10:]],
              "us_recent": [(m["createdAt"][:16], clean(m.get("text"))[:200], m.get("price"), bool(m.get("isFromQueue"))) for m in mine[-10:]],
              "sub_active": (u.get("subscribedOnData") or {}).get("expiredAt") is None if u else None}
summary = {"threads": len(out), "reply": {"n": len(all_rt), "median_min": round(st.median(all_rt)) if all_rt else None,
                                           "p75_min": round(sorted(all_rt)[int(len(all_rt) * .75)]) if all_rt else None,
                                           "within_15_pct": round(sum(1 for r in all_rt if r <= 15) / len(all_rt) * 100) if all_rt else None},
           "unanswered": sorted([{"id": k, "name": t["name"], "hours": t["unanswered_hours"], "net_w": (co.get(k) or {}).get("net_w"), "life": (co.get(k) or {}).get("life")}
                                 for k, t in out.items() if t.get("unanswered")], key=lambda x: -(x["life"] or 0)),
           "quiet": sorted([{"id": k, "name": t["name"], "days_since_personal": t["days_since_personal"], "trail_blasts": t["trail_blasts"], "life": (co.get(k) or {}).get("life")}
                            for k, t in out.items() if (t.get("days_since_personal") or 0) >= 10 or (t.get("days_since_personal") is None and "error" not in t)], key=lambda x: -(x["life"] or 0))}
json.dump({"summary": summary, "threads": {str(k): v for k, v in out.items()}}, open("data/threads_analysis.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps(summary["reply"]), "\nunanswered:", len(summary["unanswered"]), "quiet 10d+:", len(summary["quiet"]))
for k, t in sorted(out.items(), key=lambda x: -((co.get(x[0]) or {}).get("life") or 0)):
    if "error" in t: continue
    w = co.get(k, {})
    print(f"\n=== {t['name']} ({k}) life ${w.get('life', 0):.0f} window ${w.get('net_w', 0):.0f} lastbuy {w.get('days_since_buy')}d")
    print({x: t[x] for x in ["n", "n_fan", "n_personal", "n_blast", "ppv_sent", "ppv_unbought", "last_by", "trail_blasts", "days_since_fan", "days_since_personal", "unanswered", "unanswered_hours", "med_rt_min"]})
    for a in t["fan_recent"][-4:]: print("  FAN", a)
    for a in t["us_recent"][-4:]: print("  US ", a)
print("\nwritten data/threads_analysis.json")
